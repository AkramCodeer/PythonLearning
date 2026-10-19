# Port `chat-test.html` features into the Replit `pallet-iq` app (React Native / Expo)

## Context

`src/main/resources/static/chat-test.html` is the reference "dev console" for the PalletNow
Agent. It exercises **every** capability of the agent SSE backend (streaming answer, tool
status pills, thinking box, inline charts, file download, suggestions, token HUD, chat
history, sessions, deep mode, file upload, stop). The Replit **Pallet (Mobile app) / pallet-iq**
already consumes the agent via its existing **`/iq-chat-stream`** SSE endpoint and renders
basic token streaming + suggestion chips + quick-action cards (confirmed in screenshots).

Goal: bring the mobile app to **full feature parity** with `chat-test.html`, shipped as
independent phases. The mobile app is **React Native (Expo)** and must keep using its existing
`/iq-chat-stream` proxy wiring — each phase only maps additional SSE event types and adds UI.

This file is the planning artifact. Each phase below contains a **ready-to-paste prompt for the
Replit Agent**. Hand them to Replit one at a time, in order. Do not skip Phase 0 — it is the
backbone the rest depend on.

---

## The SSE contract (single source of truth — give this to Replit verbatim)

The backend is Spring SSE. Each event is `event:<name>` + `data:<json>`. The mobile app's
`/iq-chat-stream` proxy **must forward every event type below unchanged** — today it likely only
passes `token`/`suggestions`. Events the app must handle:

| event | data JSON | meaning / UI |
|-------|-----------|--------------|
| `session` | `{ "sessionId": "uuid" }` | persist sessionId for continue/history |
| `status` | `{ "tool": "runQuery", "message": "Running…", "status": "progress"\|"success" }` | tool pill (spinner → check) |
| `reasoning` | `{ "text": "…" }` | append to collapsible "thinking" box; clear live answer buffer |
| `token` | `{ "chunk": "…" }` | append to answer buffer, render as markdown |
| `usage` | `{ "agent","model","inputTokens","outputTokens","cacheReadTokens","thinkingTokens","turnTotalTokens","runningTotalTokens" }` | token-usage HUD ledger |
| `file` | `{ "fileUrl","fileType":"excel"\|"chart","fileName" }` | download card |
| `suggestions` | `{ "items": ["…","…"] }` | follow-up chips (already done) |
| `error` | `{ "message": "…" }` | inline error bubble + toast |
| `complete` | `{ "status": "SUCCESS" }` | seal turn: collapse thinking, derive charts, stop cursor |

**Endpoints** (proxied behind `/iq-chat-stream` today; the proxy must learn the extra params):
- New chat (with optional file): `POST /api/agent/chat-stream` — multipart fields
  `prompt, userId, orgId, locationId, file?(xlsx/csv/png/jpg/pdf), deepMode?`
- Continue session: `GET /api/agent/chat-stream/continue?prompt&userId&orgId&locationId&sessionId?&deepMode?`
- List sessions: `GET /api/agent/chat/sessions?userId&orgId&locationId&page=0&size=30`
  → `[{ sessionId,title,messageCount,totalTokens,totalCostUsd,createdAt,lastMessageAt }]`
- Transcript: `GET /api/agent/chat/sessions/{sessionId}/messages`
  → `[{ seq,role:"USER"|"ASSISTANT",content,fileName,fileType,totalTokens,createdAt }]`

**Token-stream quirks the app must respect** (already handled by chat-test.html):
- Strip inline `[[chart:TYPE]]` markers from displayed text (they drive chart derivation).
- Strip any `SUGGESTIONS:[...]` trailer from displayed text.
- On a `reasoning` event, the text that just streamed live was narration — **move it into the
  thinking box and clear the live answer area** (chat-test.html sets `rawText=''`).

---

## Recommended Expo libraries (name these in the prompts)
- Markdown: **`react-native-markdown-display`**
- Charts: **`react-native-gifted-charts`** (line/bar/pie; pure-RN, no WebView). Chart.js will NOT work.
- File download/open: **`expo-file-system`** + **`expo-sharing`**
- File pick: **`expo-document-picker`** (xlsx/csv/pdf) + **`expo-image-picker`** (png/jpg)
- SSE: reuse the app's **existing stream reader** (Expo's `expo/fetch` streaming or `react-native-sse`). Do not rewrite it.

---

## Phases (each is independently shippable)

> Status legend: ✅ already in app · ⬜ to build

- ✅ Token streaming, suggestion chips, quick-action empty-state cards
- ⬜ **Phase 0** — SSE event router + proxy passthrough (backbone)
- ⬜ **Phase 1** — Tool status pills (`status`)
- ⬜ **Phase 2** — Thinking / reasoning box (`reasoning`)
- ⬜ **Phase 3** — Rich markdown (tables/code/lists) for `token`
- ⬜ **Phase 4** — Inline charts from tables (`[[chart:TYPE]]` + heuristics)
- ⬜ **Phase 5** — File download cards (`file`)
- ⬜ **Phase 6** — File attachment / upload (multipart `POST /chat-stream`)
- ⬜ **Phase 7** — Token-usage HUD (`usage`)
- ⬜ **Phase 8** — Chat history (sessions list + transcript)
- ⬜ **Phase 9** — Session + New/Continue mode
- ⬜ **Phase 10** — Deep Analysis mode toggle
- ⬜ **Phase 11** — Stop / abort streaming
- ⬜ **Phase 12** — Error bubbles + toasts

---

### PHASE 0 — SSE event router + proxy passthrough  *(do first)*

```
Refactor the existing agent chat streaming so a SINGLE parser handles every Server-Sent Event
type, not just token/suggestions.

1. Backend proxy (/iq-chat-stream): forward EVERY upstream SSE event verbatim — event names AND
   data payloads — for these types: session, status, reasoning, token, usage, file, suggestions,
   error, complete. Do not drop or rename any. Also forward these new request params downstream:
   sessionId, deepMode, and (for POST) a multipart file. Keep the existing auth/userId/orgId/
   locationId wiring exactly as is.

2. Frontend: create one dispatcher that reads the SSE stream and routes by event name to handler
   callbacks: onSession, onStatus, onReasoning, onToken, onUsage, onFile, onSuggestions, onError,
   onComplete. Keep using the app's current stream reader — do not replace it.

3. Per assistant turn keep this state: answerBuffer (string), thinkingText, toolPills (keyed by
   tool name), usageRows, files, suggestions, sessionId, isStreaming.

4. token handler: append chunk to answerBuffer; before rendering, STRIP inline [[chart:TYPE]]
   markers and any "SUGGESTIONS:[...]" trailer from the displayed text.
   reasoning handler: append text to thinkingText AND clear answerBuffer (the live text so far
   was narration that belongs in the thinking box).
   complete handler: stop the typing cursor and mark the turn sealed.

Do not add visible UI yet beyond what exists — just wire the router so later phases plug in.
Acceptance: existing token streaming + suggestion chips still work unchanged; console-logging
each routed event shows session/status/reasoning/usage/complete arriving for a data question.
```

---

### PHASE 1 — Tool status pills (`status`)

```
Add live "tool" status pills above the streaming answer, like a tool-call progress log.

Consume the `status` SSE event: { tool, message, status } where status is "progress" or
"success". Maintain one pill per distinct `tool` (keyed by tool name) for the current turn.
- progress: pill shows a small spinner + the message (e.g. "Running secure BigQuery SQL…").
- success: same pill flips to a green check + green text/background.
Render pills as a vertical stack of small rounded chips at the top of the assistant message,
above the answer text. Clear pills when a new turn starts. Match the app's existing card styling.
Acceptance: asking "how is my business this month" shows pills for transfer_to_agent,
listDatasets, listTables, getTableSchema, runQuery transitioning spinner → check.
```

---

### PHASE 2 — Thinking / reasoning box (`reasoning`)

```
Add a collapsible "thinking" box to each assistant message.

Consume the `reasoning` SSE event: { text }. Accumulate each reasoning text as a paragraph in a
box rendered ABOVE the answer (below the tool pills). While streaming, header reads "Thinking…"
with a 💭 icon and the box is expanded. On the `complete` event, collapse the box and change the
header to "Thought process" with a ✓ and a chevron; tapping the header expands/collapses it.
Render the reasoning text as markdown. Remember from Phase 0: a reasoning event also clears the
live answer buffer (that narration now lives here, not in the answer).
Acceptance: during a multi-step data question the thinking box fills with the agent's narration,
then auto-collapses to "Thought process" when the answer finishes; tapping re-expands it.
```

---

### PHASE 3 — Rich markdown for the answer (`token`)

```
Render the assistant answer as full GitHub-flavored markdown instead of plain text.

Install and use react-native-markdown-display for the answerBuffer. Must render: headings,
bold/italic, bullet & numbered lists, code blocks + inline code, blockquotes, and especially
GFM TABLES (the agent returns metric tables and currency like ₹93,633.69). Style tables with
header row shading and cell borders. Keep stripping [[chart:TYPE]] markers and the
"SUGGESTIONS:" trailer before rendering. Keep the blinking typing cursor at the end while
streaming. Match app fonts/colors.
Acceptance: the business-summary answer shows proper tables (This Month's Snapshot, Daily Sales
Trend, Order-Type, Top Products) with aligned columns and rupee values.
```

---

### PHASE 4 — Inline charts from tables (`[[chart:TYPE]]`)

```
Auto-render charts from the markdown tables in the answer, mirroring chat-test.html.

The agent embeds a marker line like [[chart:line]], [[chart:pie]], or [[chart:bar]] immediately
AFTER a table to hint its chart type. Logic:
1. While streaming, capture these markers in source order (Nth marker → Nth table). Strip them
   from displayed text (already done in Phase 0).
2. On `complete`, parse each rendered markdown table: first column = labels, numeric columns =
   series. Strip ₹, commas, %, spaces when parsing numbers. A column is numeric if ≥60% of its
   cells parse as numbers. Skip a 2-column "Metric/Value" KPI table UNLESS it has an explicit
   marker.
3. Chart type = the table's marker if present, else heuristic: dates in labels → line, else bar.
   For pie/doughnut use the first numeric column only.
Render each chart in a card below the answer using react-native-gifted-charts (line/bar/pie).
Title the card from the table's preceding heading. Use a fixed palette
(#d97706,#2563eb,#059669,#dc2626,#7c3aed,#db2777,#0891b2,#ca8a04).
Acceptance: the business summary renders a line chart (daily sales), a pie chart (order type),
and a bar chart (top products) under their tables.
```

---

### PHASE 5 — File download cards (`file`)

```
Show a download card whenever the agent generates a file.

Consume the `file` SSE event: { fileUrl, fileType: "excel"|"chart", fileName }. Render a card
below the answer: 📊 icon for excel, 📈 for chart, the fileName, the type, and a Download button.
Tapping Download fetches fileUrl with expo-file-system, saves to the app's document/cache dir,
then opens the OS share/open sheet via expo-sharing (so the user can save/open the .xlsx or .png).
The agent also streams a "[Download Excel](url)" / "[View Chart](url)" markdown link in the
answer — render it as a tappable link too.
Acceptance: "Export last week's sales to Excel" yields a card with a working Download that opens
the .xlsx in another app.
```

---

### PHASE 6 — File attachment / upload (multipart POST)

```
Let the user attach a file to a message; send it as multipart to the agent.

Add an attach button in the composer. Use expo-document-picker for .xlsx/.xls/.csv/.pdf and
expo-image-picker for .png/.jpg. Show a removable preview chip (filename + size) above the input.
When a file is attached, send the message as multipart/form-data POST to the chat-stream endpoint
(via the /iq-chat-stream proxy, which must accept the file param from Phase 0) with fields:
prompt, userId, orgId, locationId, file, deepMode. With no file, keep the current request path.
Clear the attachment after send. The user bubble should show a small file tag when a file was sent.
Acceptance: attaching a spreadsheet image + "make this a chart" returns a chart file card
(Phase 5); attaching nothing behaves exactly as today.
```

---

### PHASE 7 — Token-usage HUD (`usage`)

```
Add a token-usage panel summarizing LLM spend for the current turn.

Consume the `usage` SSE event (one per LLM call): { agent, model, inputTokens, outputTokens,
cacheReadTokens, thinkingTokens, turnTotalTokens, runningTotalTokens }. Maintain a ledger keyed
by agent+model, summing each field. The big total = runningTotalTokens (server-authoritative),
falling back to the sum of row totals. Reset the ledger at the start of each turn.
Expose a header "Tokens" toggle that opens a small panel/bottom-sheet showing: the total
(formatted 1.2k / 3.4M), a "By model" breakdown and a "By agent" breakdown (sorted desc).
Acceptance: after a data question the panel shows a non-zero total broken down by gemini model
and by agent (coordinator, data_analyst_agent, etc.).
```

---

### PHASE 8 — Chat history (sessions + transcript)

```
Add a chat-history drawer listing past conversations and loading their transcripts.

Use GET /api/agent/chat/sessions?userId&orgId&locationId&page=0&size=30 →
[{ sessionId, title, messageCount, totalTokens, lastMessageAt }]. Render a drawer/screen of
cards (title, "{messageCount} msgs · {tokens} tok", relative time), newest first; highlight the
active session. Tapping a card calls GET /api/agent/chat/sessions/{sessionId}/messages →
[{ role:"USER"|"ASSISTANT", content, fileName, fileType }] and renders the transcript: USER →
user bubble (with file tag if fileName), ASSISTANT → markdown answer with charts derived from its
tables (reuse Phase 3/4). Opening a session sets the active sessionId and switches to Continue
mode (Phase 9). Add a "History" entry point in the header/menu.
Acceptance: History drawer lists prior chats; tapping one loads the full conversation with tables
and charts; sending then continues that same session.
```

---

### PHASE 9 — Session + New/Continue mode

```
Track the live session and support continuing it vs starting fresh.

On the `session` SSE event, store sessionId and show a small "Session: <first 8 chars>" badge
(tappable to copy). Add a New/Continue control:
- New: POST /api/agent/chat-stream (multipart), no sessionId — server creates a new session.
- Continue: GET /api/agent/chat-stream/continue?...&sessionId=<current> — multi-turn.
After the first answer in a New chat, auto-switch to Continue so follow-ups stay in the session.
A "New Chat" action clears the screen, session, attachment, and resets to New mode. Suggestion
chips (existing) and history-opened sessions both send in Continue mode.
Acceptance: first question starts a session (badge appears); follow-ups and suggestion chips
continue the same session; "New Chat" starts a fresh one.
```

---

### PHASE 10 — Deep Analysis mode toggle

```
Add a "Deep Analysis" toggle in the composer/options.

When ON, include deepMode=true in the request (query param for GET continue, form field for POST).
Persist the toggle locally (AsyncStorage). Show a subtle "ON"/purple badge when enabled. No other
behavior change — the backend handles the heavier analysis path.
Acceptance: toggling on and asking a question sends deepMode=true; the setting survives app
restart.
```

---

### PHASE 11 — Stop / abort streaming

```
Let the user stop an in-progress response.

While streaming, the send button becomes a Stop button. Tapping it aborts the active SSE
request/reader (AbortController or the reader's cancel), sets isStreaming=false, and seals the
current assistant turn (collapse thinking, derive charts from whatever tables arrived, remove the
cursor). Show a brief "Stream stopped" toast. Re-enable Send afterward.
Acceptance: tapping Stop mid-answer halts streaming immediately and leaves the partial answer
intact and sealed.
```

---

### PHASE 12 — Error bubbles + toasts

```
Add graceful error handling matching the dev console.

On the `error` SSE event or a network/stream failure, render a red inline error bubble inside the
assistant message (warning icon + message) and show a transient toast. If the backend already
streamed a friendly sentence via `token`, keep it and just add the toast. Add a lightweight toast
system (info/success/warning/error) reused by Stop (Phase 11) and copy-session (Phase 9).
Acceptance: a forced backend error shows a red bubble + toast without crashing the stream UI;
subsequent messages work normally.
```

---

## Verification (per phase and end-to-end)

For each phase, in the Replit preview (Simulate on Web or Try on device):
1. Ask **"how is my business going this month"** — exercises session, status, reasoning, token,
   usage, tables, `[[chart:*]]`, suggestions, complete in one turn (matches the screenshot run).
2. Confirm the phase's Acceptance line, and confirm **no regression** to token streaming +
   suggestion chips (the already-working baseline).
3. Network tab: confirm the `/iq-chat-stream` response still shows `event:` lines for the newly
   handled type (e.g. `event:status`, `event:usage`, `event:file`).

End-to-end smoke after Phase 12:
- New chat → tables + charts + tool pills + thinking box + token HUD populated.
- Attach a spreadsheet image → "make a chart" → file card downloads/opens.
- Export to Excel → download card opens the .xlsx.
- Open History → load a past session → continue it.
- Toggle Deep Analysis, send, confirm `deepMode=true` on the wire.
- Stop mid-stream, then send again.

## Reference
- Frontend spec mirror (every behavior above is implemented here):
  `src/main/resources/static/chat-test.html`
- SSE producer + endpoints: `AgentController.java` (`/chat-stream`, `/chat-stream/continue`),
  `AgentChatHistoryController.java` (`/chat/sessions`, `/chat/sessions/{id}/messages`)
