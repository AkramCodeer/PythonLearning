# Keep Pallet IQ chat generation running after navigation, with live reconnect

## Context

Pallet IQ chat (`GET/POST /api/agent/chat-stream`, plus `/chat-stream/continue`) streams answers
over Server-Sent Events. Today, if the user submits a prompt and navigates to a different page
before the answer finishes, the backend **cancels the in-flight LLM/tool-execution run** — not
just the client's view of it. Goal:

1. The run must keep going to completion regardless of navigation — it should only stop once the
   full response has actually been generated.
2. When the user returns to the chat: if the run is **still generating**, they should see its
   current progress (live); if it has **already finished**, they should see the final response.

This is fundamentally a **backend** fix. Nothing on the frontend can stop the backend from
deliberately cancelling the run the moment it notices the connection is gone — that has to change
server-side. "Resume watching progress" also needs a backend-provided way to reattach to a run
decoupled from the original HTTP connection (a new endpoint).

Can be implemented and shipped in two independent phases — Phase 1 alone already fixes "don't
truncate the answer"; Phase 2 adds live reconnect on top and depends on Phase 1.

## Root cause

The chat-stream turn's ADK run is a live RxJava subscription stored on `TurnContext.subscription`
(`src/main/java/com/pallet/agent/service/TurnContext.java:39`), and it gets disposed — cancelling
the run — from three places, all triggered by the client/connection going away rather than by the
run actually finishing:

1. `ChatTurnService.begin` arms `emitter.onCompletion(() -> finalizeTurn(ctx))` and
   `emitter.onError(t -> finalizeTurn(ctx))` (`ChatTurnService.java:60-61`). Spring's `SseEmitter`
   fires these whenever the async request ends for *any* reason, including the container
   detecting the client disconnected. `finalizeTurn` (`ChatTurnService.java:76-99`)
   unconditionally calls `disposeQuietly(ctx.subscription)` (line 79), cancelling the ADK run.
2. In each of the three `onNext` handlers in `ChatStreamController` (`streamChat` line
   2083-2090, `streamChatWithFile` line 2573-2580, `streamChatContinue` line ~2863-2870), a failed
   `emitter.send(...)` throws (once the container has torn the emitter down, this is usually
   `IllegalStateException: "ResponseBodyEmitter has already completed"`, which `sendEvent`
   doesn't swallow — it only catches `IOException`, `ChatStreamController.java:4064-4070`). The
   catch block detects this via `isClientGone(e)` (`ChatStreamController.java:851-866`) and calls
   `endStream(ctx)`, which explicitly disposes the subscription (`ChatTurnService.java:102-107`).
3. `endStream` (`ChatTurnService.java:102-107`) is designed as a "client left, cancel the run"
   helper — exactly the behavior to remove for these endpoints.

Reassuring finding: the assistant's visible answer is already reconstructed independently of
delivery success — `sendEvent` appends each `token` chunk to `TurnContext.answer`
(`ChatStreamController.java:4054-4059`) *before* attempting `emitter.send(...)`. That buffer is
exactly what a "progress so far" snapshot needs in Phase 2.

Contrast with the existing decoupled pattern used by the other agent types (proposals, audits,
etc.), which this plan mirrors:
- `AgentKickoffService.start` (`AgentKickoffService.java:53`) submits work to
  `applicationTaskExecutor` with no reference to any HTTP request/response.
- `AgentRunner.runFromSession` (`AgentRunner.java:193-482`) persists
  `session.setFinalResponse(...)` (line 433) regardless of whether a client is listening.
- `AgentEventBus` (`src/main/java/com/pallet/agent/stream/AgentEventBus.java`) is a per-session
  `Sinks.Many` that the run publishes into and any number of SSE subscribers read from
  independently — reconnecting/disconnecting subscribers never touch the run itself.
- `AgentStreamController.stream()` (`AgentStreamController.java:86-162`) is the reconnect
  endpoint: if the session's bus sink is still open it subscribes live; if not, it reconstructs a
  terminal event from the DB (`terminalEventFromDb`, lines 188-207) and completes immediately.

Chat-stream has no equivalent of the bus/reconnect pair today — Phase 2 closes that gap.

---

## Phase 1 — decouple the ADK run from the original SSE connection

Stop treating "the SSE emitter ended" as a signal to cancel the ADK subscription. Only dispose
`ctx.subscription` when the ADK run has genuinely finished (the RxJava `onComplete`/`onError`
callbacks that already call `finalizeTurn(ctx)` today).

**Status (2026-08-11): implemented on this branch, uncommitted.** Checklist below updated against
the actual diff. Compiles clean (`gradlew compileJava compileTestJava --offline`); the two Phase 1
unit test classes could not be executed in this environment (Mockito's inline mock maker fails to
initialize — `java.io.tmpdir` misconfigured on this machine, unrelated to the change) so they're
verified by reading, not by a green run. One real gap found — see the flagged item below.

- [x] `TurnContext.java`: added `volatile boolean clientGone`, plus a second flag
      `volatile boolean backgroundable` (defaults `false`) that the plan's "explicit backgroundable
      flag" bullet below ended up needing as a field rather than a `begin()` parameter.
      `ChatStreamController.sendEvent` (`:4110`) now also skips the `emitter.send` call when
      `ctx.clientGone` — the "skip pointless sends" behavior this flag exists for.
- [x] `ChatTurnService.begin`: `emitter.onCompletion`/`emitter.onError` no longer finalize
      directly — both now call a new `onEmitterEnded(ctx)`. **Deviation from the plan:** the
      "backgroundable" flag is *not* passed into `begin(...)`. Instead each of the three streaming
      handlers sets `ctx.backgroundable = true` as a plain field write, immediately before
      `ctx.subscription = getAdkRunner(...).runAsync(...).subscribe(...)` — i.e. still well after
      `begin()` returns (`ChatStreamController.java:2005`, `2504`, `2821`). See the flagged race
      below; this is narrower than "unconditionally finalize" but not the begin()-time close the
      plan called for.
  - [x] `onEmitterEnded`: when `ctx.backgroundable && !ctx.finalized.get()`, marks
        `ctx.clientGone = true` and returns — no dispose, no finalize.
  - [x] Otherwise: falls through to `finalizeTurn(ctx)`, matching today's eager behavior.
- [ ] **Not done, by design choice:** `endStream` (`ChatTurnService.java:102-107`) still disposes
      the subscription — it was *not* stripped down. Instead the implementation routes around it:
      backgroundable turns never reach `endStream` from the disconnect path (they go through
      `onEmitterEnded`/the new `if (ctx.backgroundable)` branch below); `endStream` is kept for the
      cases that should still cancel eagerly — a client-gone hit on a non-backgroundable turn, and
      a new `emitter.onTimeout(() -> endStream(ctx))` hook (not in the original plan, added to keep
      a hung/never-completing run from pinning resources forever — see the `streamTimeoutMs` note
      under "Things to verify"). Functionally covers the same ground; the doc's original phrasing
      ("remove/repurpose so it no longer disposes") doesn't match what's on disk.
- [x] At the three `isClientGone` catch sites (`ChatStreamController.java:2084`, `2578`, `2893`):
      now `if (ctx.backgroundable) { ctx.clientGone = true; log.debug(...) } else { endStream(ctx); }`.
      The `else` is effectively dead code at these three call sites today (by the time `onNext` can
      fire, `backgroundable` is already `true`) but is left as a correct fallback.
- [x] Guard `emitter.complete()`/`emitter.completeWithError(...)` with try/catch — done at all six
      real-completion/error call sites across `streamChat`, `streamChatWithFile`, and
      `streamChatContinue` (success path and the ADK `error` callback in each). Bonus, beyond the
      checklist: the outer bootstrap `catch (Exception e)` block in each of the three handlers now
      also resolves `ctx` and explicitly sets `ctx.backgroundable = false` before its own guarded
      `sendError`/`completeWithError`, so a bootstrap failure (before any run starts) still
      finalizes correctly through `onEmitterEnded` instead of relying on old unconditional-finalize
      behavior that no longer exists.
- [x] `finalizeTurn`'s `disposeQuietly(ctx.subscription)` (`ChatTurnService.java:79`) — untouched,
      as intended.

### ✅ Resolved: start-of-turn race

Originally flagged here (and analyzed in depth before fixing): `ctx.backgroundable = true` is set
well after `begin()` returns — after `beginTurn()`'s `healSessionIfNeeded` DB call, synchronous
prompt-context building, and in `streamChat`/`streamChatWithFile` potentially a
`urlFetchService`/GCS network call. A disconnect in that window used to cause `onEmitterEnded` to
`finalizeTurn` immediately (correct on its own — nothing was running yet to protect), but execution
then continued regardless and started the ADK run anyway into the now-finalized, already-removed
`ctx`. That run's real completion later became a silent no-op (`finalizeTurn`'s CAS already fired),
discarding the generated answer and reproducing the exact truncation bug Phase 1 exists to fix.

**Why not thread `backgroundable` through `begin()` as originally planned:** investigating the fix
surfaced that `begin()` is called once per request, but `streamChatWithFile` alone branches into
~8 synchronous sub-passes after `begin()` (GCS-ref analysis, pasted-URL analysis, fetched-URL-file
handling, tabular analysis, image visualizer, file explanation, data-report export...), each of
which relies on `backgroundable` being `false` so a disconnect during them still finalizes via
`onEmitterEnded`'s fallthrough — none of those passes call `finalizeTurn` themselves. Setting
`backgroundable = true` inside `begin()` would have made all of those passes un-finalizable on
disconnect (turn leaks in `turns`/never persists to history). Doing this "properly" would mean
auditing and adding an explicit `ctx.backgroundable = false` at every one of those ~13 early-exit
branches across all three handlers (`streamChat`: 2, `streamChatWithFile`: 8, `streamChatContinue`:
3) — large surface area for a one-line-per-site change to go unnoticed and reintroduce the same bug
elsewhere.

**Fix actually applied:** a guard immediately before each of the three `.subscribe(...)` calls
(`ChatStreamController.java:2009` in `streamChat`, `:2516` in `streamChatWithFile`, `:2841` in
`streamChatContinue`):
```java
if (ctx.finalized.get()) {
    log.debug("... turn already finalized before the run could start ... — skipping run ...");
    return;
}
```
If the turn was already finalized during setup, the run simply never starts — no wasted LLM cost,
no orphaned subscription writing to a removed `ctx`, no answer silently generated-then-discarded.
This is a better outcome than letting the run proceed: once `finalizeTurn` has run, chat history
already shows the turn as complete (with an empty answer); generating a real answer afterward that
can never be persisted would waste cost for a result nobody would see. Doesn't require touching
`begin()`'s signature, the three streaming handlers' 13 synchronous early-exit branches, or the
existing `ctx.backgroundable = false` resets already present before the 4 follow-up passes in
`streamChatWithFile`'s coordinator-completion handler.
**Verified:** compiles clean (`gradlew compileJava --offline`). No automated test added — exercising
it requires standing up `ChatStreamController` with its full dependency graph (ADK runner, sandbox
executor, session service, etc.), which the existing `StreamCancellationTest.java` doesn't attempt
(it only tests the two static helpers `disposeQuietly`/`isClientGone`). Covered by the manual repro
below instead.

**Outcome of Phase 1 alone:** navigating away no longer truncates the answer.
`ChatHistoryService.recordAssistantTurn` (`ChatHistoryService.java:80-91`), called from
`finalizeTurn`, persists the *full* answer once the run really completes, already retrievable via
the existing `GET /api/agent/chat/sessions/{sessionId}/messages`
(`AgentChatHistoryController.java:47-50`) or `GET /api/agent/history`
(`ChatStreamController.java:2900`). This alone satisfies "show the final response if it already
finished." Phase 2 adds the live-progress-while-running case.

### Phase 1 tests to update/add
- [x] `ChatTurnServiceTest.java` — `endStream_disposesSubscription_finalizes_andCompletes`
      (still lines ~91-103) was left **unchanged**, correctly: since `endStream` itself wasn't
      touched (see above), its old disposal assertions still hold. Four new tests were added
      instead of updating this one: `onEmitterEnded_marksClientGone_withoutFinalizing_whenBackgroundableAndNotYetFinalized`,
      `onEmitterEnded_finalizes_whenNotBackgroundable`,
      `onEmitterEnded_finalizes_whenBackgroundableButAlreadyFinalized`, `onEmitterEnded_null_isNoOp`
      — between them cover all four branches of the new method.
- [ ] `StreamCancellationTest.java` — **not touched** (confirmed via `git status`/`git log`, file
      unchanged). The "mark client-gone, don't dispose" path is covered at the `ChatTurnService`
      unit level (above) but not at the controller/integration level this file targets. Still
      outstanding if that layer of coverage is wanted.
- [x] `TurnContextTest.java` — bonus coverage beyond the checklist: asserts both new fields default
      correctly (`backgroundable=false`, `clientGone=false`) on a freshly constructed context.
- [x] Manual repro — **done, against a real running instance**, not `chat-test.html` (curl against
      the SSE endpoint directly, for precise control over the disconnect timing). A second app
      instance was started locally on port 8091 (`AGENT_SERVICE_PORT=8091 ./gradlew bootRun`,
      default/stage GCP profile — *not* `run-local-prodbq.sh`, to avoid real prod BigQuery billing)
      alongside the user's own pre-existing instance on 8090, which was never touched or stopped.
      A ~600-word essay prompt (plain-text, no BigQuery/MCP needed — MCP was down locally anyway)
      was sent via `curl --max-time 2`, forcing a client-side disconnect ~2s in (`curl` exit 28).
      Server logs confirmed the ADK run was **not** cancelled: token generation continued for
      ~13 more seconds after the disconnect, reaching `[CHAT-STREAM COMPLETE]` naturally, with the
      Phase 1 completion-path try/catch cleanly absorbing the now-dead emitter at DEBUG level
      (`"completion-path emit failed on dead emitter: ResponseBodyEmitter has already completed"`)
      instead of erroring. `GET /api/agent/chat/sessions/{sessionId}/messages` then showed the
      **full, untruncated, well-formed answer** (ends in a complete sentence, ~8500 tokens) — the
      exact "don't truncate the answer" behavior this phase exists for. Repeated a second time
      after the Phase 2 bug fix below, with the same result.
- [x] Re-run `streamChat` end-to-end *without* any disconnect — **done**, happy path unaffected:
      a photosynthesis-explanation prompt streamed token-by-token to a normal `complete` event and
      showed up correctly in history. (`streamChatWithFile`/`streamChatContinue` were not
      separately smoke-tested — same code shape, lower risk, deprioritized given time; flagging as
      the one item in this phase not literally exercised.)
- [x] Automated run of `ChatTurnServiceTest`/`TurnContextTest` — **green.** The earlier Mockito/
      `java.io.tmpdir` failure was a stale Gradle daemon holding a broken `TEMP`/`TMP` (`D:/tmp`,
      which doesn't exist on this machine) from before those env vars were corrected; `gradlew
      --stop` + a fresh `--no-daemon` run with `TEMP`/`TMP`/`TMPDIR` pointed at a real directory
      fixed it. Full `gradlew test`: 214 run, 4 failed, all 4 in unrelated packages
      (`config.AgentModelsTest`, `agents.data.DataAgentWiringTest`, `prompt.AnalystThinkingTest`;
      model-tier/wiring config, nothing to do with chat-stream, and none in a file this work
      touched). A `git stash`-based isolation check was attempted but aborted partway (an
      incomplete stash state left the build uncompilable) rather than risk the working tree —
      treating these as pre-existing/environment-dependent on package/naming grounds, not a
      clean bisection.

---

## Phase 2 — live reconnect while the run is still in progress

Every SSE emission in `ChatStreamController` already funnels through one method —
`sendEvent(emitter, eventName, data)` (`ChatStreamController.java:4048-4071`) is the *only* call
site of `emitter.send(...)` in the whole file (confirmed by grep); `streamTurnToken`,
`sendToolStatus`, `sendError`, `emitProductPreview`/`emitProductMatches`/`emitProductList`,
`emitNavigation`, `emitSuggestions`, and the `usage`/`session` events all call it. That makes a
per-session broadcast bus a contained addition — one new class plus edits to that single choke
point — not a sprawling refactor.

**Status (2026-08-11): implemented on this branch, uncommitted, and manually validated end-to-end**
against a real running instance (see "Phase 2 tests to add" below — the manual repro is done and
found/fixed one real bug in the process). `gradlew compileJava compileTestJava --offline` succeeds;
full `gradlew test` is green for every chat-stream-related test (see the Phase 1 test-status entry
above — same run covered both phases). No *automated* tests were added specifically for Phase 2
(`ChatTurnBus` unit tests, reconnect-endpoint branch tests) — see below for why.

- [x] New `ChatTurnBus` (`src/main/java/com/pallet/agent/stream/ChatTurnBus.java`), modeled
      directly on `AgentEventBus.java` but keyed by the chat `String sessionId`. Events carried as
      a new `ChatTurnEvent(String eventName, Object data)` record
      (`src/main/java/com/pallet/agent/stream/ChatTurnEvent.java`) — `AgentEventBus` carries a
      typed `AgentStreamEvent`; chat-stream's SSE vocabulary is `(eventName, data)` pairs, so this
      is the minimal equivalent.
  - [x] `openSink(sessionId)` — `Sinks.many().multicast().directBestEffort()` (live-only; unlike
        `AgentEventBus`'s `replay().limit(64)`, replaying raw `token` deltas out of order to a
        late joiner would reconstruct garbled text — the sync-snapshot below solves "catch up"
        instead).
  - [x] `publish(sessionId, eventName, Object data)`.
  - [x] `flux(sessionId)`, `close(sessionId)`, `hasOpenSink(sessionId)` — same shapes as
        `AgentEventBus`. (`hasOpenSink` isn't currently called anywhere — the reconnect endpoint's
        live/completed branch is decided via `ChatTurnService.contextForSession`, not the bus —
        kept for parity/completeness per this checklist item and because it's the kind of
        lightweight check a future caller will want.)
- [x] `ChatTurnService`: added `Map<String, TurnContext> turnsBySession` + `contextForSession(String
      sessionId)`. **Deviation from the plan:** `chatTurnBus.openSink(sessionId)` is called in
      `begin()` **unconditionally**, not "backgroundable turns only" as originally written — by the
      time `begin()` runs, whether this particular turn will end up backgroundable isn't decided
      yet (same reason Phase 1's `backgroundable` flag couldn't be threaded through `begin()` — see
      the Phase 1 write-up above). Opening a sink for a turn that turns out to be a short
      synchronous pass is harmless: it's closed the same way in `finalizeTurn()` regardless, and an
      unused sink with no reconnect subscriber just gets `tryEmitComplete()`'d.
      `turnsBySession`/`chatTurnBus.close(...)` are both cleared in `finalizeTurn()` using the
      2-arg `Map.remove(key, value)` so a finalize can't evict a *newer* turn that already replaced
      it for the same session.
- [x] `ChatStreamController.sendEvent`: dual-write added — the existing direct `emitter.send(...)`
      is untouched, plus `if (ctx != null) chatTurnBus.publish(ctx.sessionId, eventName, data);`
      placed *before* the `ctx.clientGone` skip-check (Phase 1), so bus subscribers keep receiving
      events even after the original connection is known dead — that's the entire point.
- [x] New reconnect endpoint, `GET /api/agent/chat-stream/{sessionId}/reconnect` (SSE), added to
      `ChatStreamController` itself (not a separate controller class — unlike proposals/audits,
      all of chat-stream's endpoints already live in this one file) modeled on
      `AgentStreamController.stream()`:
  - [x] `ctx = chatTurnService.contextForSession(sessionId)`.
  - [x] **If `ctx == null`**: reads `chatHistoryService.transcript(sessionId)`, walks it backwards
        for the latest `ChatRole.ASSISTANT` message (private helper `latestAssistantAnswer`), emits
        one `sync` event `{"status":"COMPLETED","answer": <content or "">}`, then
        `emitter.complete()`.
  - [x] **If `ctx != null`**: emits one `sync` event `{"status":"RUNNING","answer": ctx.answer()}`,
        then subscribes to `chatTurnBus.flux(sessionId)` and forwards each `ChatTurnEvent` as
        `SseEmitter.event().name(eventName).data(data)` — same shape `sendEvent` sends today.
  - [x] `emitter.onCompletion`/`onTimeout`/`onError` all dispose only the new subscription
        (`reactor.core.Disposable`, fully-qualified inline to avoid colliding with the
        already-imported RxJava `Disposable` used for `ctx.subscription`) — never touch
        `ctx.subscription`.
  - [x] Emitter timeout: `RECONNECT_EMITTER_TIMEOUT_MS = Duration.ofMinutes(5)`, matching
        `AgentStreamController.EMITTER_TIMEOUT_MS`.
  - Wiring: `ChatTurnBus` added as a constructor param + field on `ChatStreamController` and
    `ChatTurnService`; both existing direct-construction test call sites
    (`AgentControllerSyncMvcTest.java`, `ChatTurnServiceTest.java`) updated to pass a real
    `new ChatTurnBus()` instance (cheap in-memory component, no need to mock).

### New contract a frontend will need to implement (separate repo, not built here)
- `GET /api/agent/chat-stream/{sessionId}/reconnect` → SSE stream.
- First event is always named `sync`, data `{"status":"RUNNING"|"COMPLETED", "answer": "<text so
  far or final>"}`. (No `"type"` field in the payload — matches every other chat-stream event,
  which is identified by the SSE event *name*, not an in-body discriminator. The plan's original
  sketch showed `{"type":"sync",...}`; the implementation dropped `type` for consistency with
  `token`/`status`/`usage`/etc., which don't carry one either.)
- If `"RUNNING"`, the stream continues with the normal chat-stream event vocabulary (`token`,
  `status`, `usage`, `product`, `navigation`, `suggestions`, `complete`, `error`) exactly as the
  original `/chat-stream` connection would have sent them, until a `complete`/`error` event closes
  it. If `"COMPLETED"`, the stream closes immediately after the `sync` event.

### Phase 2 tests to add
- [ ] Unit tests for `ChatTurnBus` (open/publish/flux/close), mirroring any existing
      `AgentEventBus` test if one exists. **Not yet added** — `ChatTurnBus` is currently only
      exercised indirectly (compiled + wired; `ChatTurnServiceTest`/`AgentControllerSyncMvcTest`
      construct a real instance but don't assert on its behavior).
- [ ] Tests for the reconnect endpoint's two branches (live vs. already-completed). **Not yet
      added** — same reason Phase 1's start-of-turn-race guard has none: exercising
      `ChatStreamController` requires its full dependency graph, which no existing test stands up.
- [x] Manual repro — **done** (using the same local port-8091 instance as Phase 1's repro above,
      via `curl`). Found and fixed a real bug in the process — see below — then re-verified clean.
  - **Live branch**: started a slow essay prompt in the background, polled its SSE output for the
    `session` event to grab `sessionId` the instant it appeared, then immediately called
    `GET /chat-stream/{sessionId}/reconnect` in parallel. First event was
    `event:sync data:{"answer":"","status":"RUNNING"}`, followed by live `token`/`usage`/
    `suggestions`/`complete` events — byte-for-byte the same sequence the original connection
    received (`diff`-equivalent: both captures came out to the same line count).
  - **Completed branch**: reused a `sessionId` from a turn that had already finished; reconnect
    returned exactly one `event:sync data:{"answer":"<full text>","status":"COMPLETED"}` matching
    `GET .../messages` verbatim, then closed — no further events.
  - **Bug found and fixed**: the *first* live-branch attempt showed `sync` + `token` + `usage` but
    then went silent — no `suggestions`, no `complete`; the reconnect stream just ended. Root
    cause: all six `finalizeTurn(ctx)` call sites in `ChatStreamController` (complete + error
    paths × 3 handlers) called `finalizeTurn` — which now also closes the `ChatTurnBus` sink —
    **before** the trailing `emitNavigation`/`emitSuggestions`/`sendEvent("complete",...)` (or the
    error-path equivalents) had a chance to run. Those events still reached the *original*
    connection (unaffected — `sendEvent`'s direct `emitter.send()` doesn't depend on the bus), but
    a reconnect subscriber's `chatTurnBus.flux(...)` had already been completed by
    `tryEmitComplete()` and silently dropped everything published after. **Fix**: reordered all
    six sites to run the trailing emits inside `try {...} finally { finalizeTurn(ctx); }`, so the
    bus stays open until every event for that turn — including the terminal one — has actually
    been dual-written. Re-ran the live-branch repro after the fix: `suggestions` and `complete`
    now arrive correctly on the reconnect stream, matching the original 1:1. Full test suite
    re-run post-fix: still 214/4 (same 4 pre-existing/unrelated failures, nothing newly broken).

---

## Things to verify while implementing

- [ ] **sseExecutor capacity** (`AgentStreamProperties.Sse.maxConcurrentStreams`/`queueCapacity`,
      used at `ChatStreamController.java:477`): abandoned turns previously got cancelled quickly;
      after Phase 1 they run to natural completion (bounded by `streamTimeoutMs`, currently
      15 min). Confirm whether `runAsync(...).subscribe(...)` actually holds an sseExecutor
      thread for the full run or hands off to its own scheduler — if the former, watch pool
      pressure after deploy. Reconnect (Phase 2) doesn't add executor load — it only subscribes
      to the bus.
- [x] **Narrow start-of-turn race** (Phase 1) — **closed**, but not the way originally proposed
      here. `backgroundable` is still set by a plain field write right before `.subscribe(...)`
      rather than threaded through `begin(...)` (see the "✅ Resolved" writeup under the Phase 1
      checklist for why that turned out to be the wrong shape of fix, given `streamChatWithFile`'s
      ~8 synchronous early-exit sub-passes). Instead, a `ctx.finalized.get()` guard immediately
      before each of the three `.subscribe(...)` calls skips starting the run if the turn was
      already finalized during setup — closing the failure mode (silently discarded answer,
      wasted LLM cost) without needing the window itself to be zero-width.
- [ ] **Bus event volume** (Phase 2): token events can be frequent for long answers;
      `directBestEffort()` drops on backpressure rather than blocking the producer (the original
      SSE write path is unaffected either way) — acceptable since a reconnect always gets a fresh
      `sync` snapshot of `ctx.answer()` as its baseline.

## Out of scope for this repo

The actual Pallet IQ app (React Native/Expo) lives outside this repository —
`docs/replit-pallet-iq-parity-plan.md` confirms this; the *product* frontend follow-up (reconnect
on session resume, render based on the `sync` event's `status`) needs to happen in that separate
repo and isn't tracked here.

**Exception — the in-repo dev-console page was wired up (2026-08-11).** This surfaced from a real
report: closing `chat-test.html`'s tab mid-turn and reopening it showed no response (only visible
after manually digging into History), even though Phase 1 had the full answer sitting server-side
the whole time — the page just never re-fetched or reconnected on load. Fixed in
`src/main/resources/static/chat-test.html`:
- `setSessionId`/`clearSessionId` now persist/clear the active session id in `localStorage`
  (`pn-chat-session`) — previously purely in-memory, wiped on every reload.
- A `pn-chat-pending` localStorage flag is set right before a turn starts streaming and cleared
  only on a genuine `complete`/`error` SSE event (in `dispatchSSE`, covering both the normal
  stream and reconnect paths) — deliberately *not* cleared by a manual "Stop" click, since Phase 1
  means the run keeps going server-side regardless of what the local client does.
- New `reconnectSession(sessionId)` calls the Phase 2 endpoint; on the first `sync` event it either
  creates a fresh assistant bubble seeded with the in-progress answer and keeps streaming into it
  (`RUNNING`), or does nothing since the preceding history fetch already rendered it (`COMPLETED`).
- New `tryAutoResume()`, called from page init: if `pn-chat-pending` is still set on load (meaning
  the last turn never reached a clean terminal event — tab closed mid-stream), it re-loads the
  transcript via the existing `openSession()` then calls `reconnectSession()`. A clean prior exit
  leaves the page blank on reload, same as it always has.
- `consumeSSE`'s inline SSE line-parser was extracted into a shared `parseSSE(res, onEvent)` so
  both the normal streaming path and `reconnectSession` use identical parsing (no behavior change
  to the existing path — pure extraction).

**Validation:** no browser automation was available this session (the Claude-in-Chrome extension
was declined), so this wasn't clicked through in an actual browser. Instead: `node --check` on the
extracted script confirmed no syntax errors; the exact `parseSSE` algorithm was ported verbatim
into a standalone Node script and run against the real local server (`localhost:8091`) simulating
the reported scenario — start a turn, abort the client connection right after the first token
(same as a tab close), wait 3s, then reconnect. Confirmed: first event `sync` with `status:RUNNING`
and a non-empty partial `answer`, followed by live events ending in `complete`; reconnecting again
afterward returned a single `sync` with `status:COMPLETED` and the same final answer length.
`localStorage` persistence itself (the one piece that genuinely needs a real browser page-unload
cycle to exercise) was not directly exercised — it's a well-established standard Web API with low
risk, but flagging it as the one gap in this validation pass.