# Generic scheduled-task creation for external services + creator-type field

Companion to `docs/scheduled-tasks-execution-plan.md` (the original scheduled-tasks design doc) — this doc covers a follow-on feature: opening a second, non-conversational creation path so external services can create `ScheduledTask` rows directly via REST, plus a new field recording which channel created a given task.

## Context

Scheduled-task creation today only exists through the conversational path: `ScheduledTaskAgent` → `ScheduledTaskTool.createScheduledTask`/`createScheduledTaskFromTemplate` → `ScheduledTaskService.createTask`. There is no REST route that creates a task — `ScheduledTaskController` only exposes management operations (list/get/pause/resume/cancel/history/trial-run/approve/reject). `ScheduledTaskService.createTask` itself is pure persistence logic with zero LLM/agent dependency, so it's already capable of being called from a non-conversational entry point.

The goal is to open a second, generic creation door for external services to call directly, and to add a simple entity-level field — modeled after existing enum fields like `autonomyMode`/`status` — that records which channel created a given task. This is purely a provenance/audit addition: it does not change ownership (`userId` stays the access-control field) and does not change how a task executes.

Confirmed scope:
- New enum is **creator/source type** only (`AGENT` vs `EXTERNAL_SERVICE`) — not an identity/access-control concept.
- New entry point is a **new route on the existing `ScheduledTaskController`**, not a separate controller.
- **No new auth enforcement** on this route — it inherits the same (currently unauthenticated) trust posture as every other scheduled-tasks endpoint. This is a known, pre-existing gap (`SecurityConfig` has `anyRequest().permitAll()`; the real service-JWT mechanism — `ServiceJwtAuthFilter` + `ServiceTokenProvider`, HS256 signed with `AGENT_JWT_SECRET`, populates `ROLE_SERVICE` — exists but is never enforced anywhere in this codebase today) — out of scope here, flagged as a risk below.
- **NL-instruction replay only** — externally-created tasks use the same `instructionText`-driven execution as agent-created ones. No `taskType`/`handlerRef` (the typed-handler escape hatch) wiring; that path has zero concrete `ScheduledTaskHandler` implementations today and is out of scope.
- **No Java records for new DTOs** — this codebase's own precedent for a scheduled-task request body, `ScheduledTaskTemplateDto.Request` (`src/main/java/com/pallet/agent/dto/ScheduledTaskTemplateDto.java:39-50`), is a plain Lombok `@Data @NoArgsConstructor @AllArgsConstructor` class, not a record. The new request DTO follows that exact pattern.

Phases are ordered so each can be implemented and merged independently — Phase 1 alone is a safe, inert schema change; Phase 2 makes the conversational path creator-type-aware without exposing anything new; Phase 3 is the actual new capability.

---

## Phase 1 — Data model: creator-type field
- [x] Create `src/main/java/com/pallet/agent/entity/ScheduledTaskCreatorType.java` — plain enum, matching the exact house style of `AutonomyMode`/`ScheduledTaskStatus` (no annotations on the enum itself):
  ```java
  package com.pallet.agent.entity;

  /** Which channel created the row — provenance only, never consulted at execution time or for ownership. */
  public enum ScheduledTaskCreatorType {
      AGENT,
      EXTERNAL_SERVICE
  }
  ```
- [x] In `src/main/java/com/pallet/agent/entity/ScheduledTask.java`, add a field after `sourceTemplateId`:
  ```java
  @Enumerated(EnumType.STRING)
  @Column(name = "creator_type", length = 32)
  private ScheduledTaskCreatorType creatorType;
  ```
  Deliberately **no `nullable = false`** — the live `scheduled_task` table already has rows predating this column, and `ddl-auto: update` does not backfill existing rows, so a DB-level `NOT NULL` would break on boot or on old-row reads.
- [x] In the same file's existing `@PrePersist prePersist()` method, add a default (mirroring how `status`/`notificationConfig` are already defaulted there):
  ```java
  if (creatorType == null) creatorType = ScheduledTaskCreatorType.AGENT;
  ```
- [x] Update `src/main/resources/db/migration/V6__scheduled_tasks.sql` (a manually-maintained reference copy — actual schema changes are applied by Hibernate `ddl-auto: update` at boot, not this file) — add, after `source_template_id`:
  ```sql
  creator_type              VARCHAR(32)
      CHECK (creator_type IN ('AGENT', 'EXTERNAL_SERVICE')),
  ```
- [x] Verify: app boots cleanly against the existing dev DB (rows dating back to 2026-08-18), `creator_type` column is added as nullable, no migration failure. Confirmed 2026-08-20: booted against dev DB (10.66.192.3), health check `db: UP`, no schema errors; a fresh insert with `creator_type` populated round-tripped cleanly.

*(Safe to ship alone — this phase only adds a column; nothing yet writes or reads it.)*

## Phase 2 — Thread creator type through the existing (conversational) creation path
- [x] In `src/main/java/com/pallet/agent/service/ScheduledTaskService.java`, add a 14th field to the `CreateTaskCommand` inner class (appended at the end):
  ```java
  private final ScheduledTaskCreatorType creatorType;
  ```
- [x] In `createTask(CreateTaskCommand cmd)`, add one line to the existing `ScheduledTask.builder()` chain:
  ```java
  .creatorType(cmd.getCreatorType())
  ```
- [x] In `src/main/java/com/pallet/agent/tools/ScheduledTaskTool.java`, update the shared private `buildCommand(...)` helper (used by both `createScheduledTask` and `createScheduledTaskFromTemplate`) to pass `ScheduledTaskCreatorType.AGENT` as the new argument, plus the import.
- [x] In `src/test/java/com/pallet/agent/service/ScheduledTaskServiceTest.java`, update all 3 existing `new ScheduledTaskService.CreateTaskCommand(...)` call sites (`recurringCommand` helper ~line 52, `createTask_conditionalWithoutThresholdRejected` ~line 102, `createTask_conditionalWithThresholdSetsApprovalConfig` ~line 113) to append `ScheduledTaskCreatorType.AGENT`, plus the import.
- [x] In `src/main/java/com/pallet/agent/dto/ScheduledTaskDto.java`, add `creatorType` (placed after `sourceTemplateId` to mirror entity field order) to the field list and the `from(...)` factory, so it's visible via `GET /{id}` and `GET ''` (list).
- [x] Verify: run `ScheduledTaskServiceTest` — passes unchanged otherwise. Drive the conversational flow (chat, or `scheduled-tasks-test.html`'s "Ask the Agent" view) to create a task and confirm the resulting row has `creatorType = "AGENT"`. Confirmed 2026-08-20: all 24 `ScheduledTaskServiceTest` tests pass; drove `POST /api/agent/chat-stream` end-to-end (orgId=RET_360) — agent echoed a confirmation summary, then on confirm created `TASK-000024`; `GET /api/agent/scheduled-tasks/TASK-000024` returned `"creatorType":"AGENT"`.

*(Safe to ship alone — the conversational path keeps working exactly as before, now just tagging its own rows.)*

## Phase 3 — New REST endpoint for external-service creation
- [x] Create `src/main/java/com/pallet/agent/dto/ScheduledTaskCreateRequest.java` — a plain Lombok class (no record), matching `ScheduledTaskTemplateDto.Request`'s exact pattern, plus Bean Validation annotations (this codebase's established pattern for a *required-field* request body — see `AgentRequest.java`, used via `@Valid @RequestBody` in `AgentRunController`/`AudienceAgentController`/etc.):
  ```java
  package com.pallet.agent.dto;

  import com.pallet.agent.entity.AutonomyMode;
  import jakarta.validation.constraints.NotBlank;
  import jakarta.validation.constraints.NotNull;
  import lombok.AllArgsConstructor;
  import lombok.Data;
  import lombok.NoArgsConstructor;

  import java.time.LocalDateTime;

  /**
   * Request body for {@code POST /api/agent/scheduled-tasks} — the generic, non-conversational
   * creation path for external services (creatorType is fixed to EXTERNAL_SERVICE by the
   * controller). NL-instruction replay only; mirrors CreateTaskCommand's free-form (non-template)
   * surface — no taskType/handlerRef.
   */
  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public class ScheduledTaskCreateRequest {
      @NotBlank private String orgId;
      private String locationId;
      @NotBlank private String userId;
      @NotBlank private String instructionText;
      private String cronExpression;
      private LocalDateTime runAt;
      private String timezone;
      @NotNull private AutonomyMode autonomyMode;
      private String conditionalThresholdDescription;
      private Integer maxDurationMinutes;
      private String notificationChannel;
      private String notificationRecipient;
  }
  ```
- [x] In `src/main/java/com/pallet/agent/controller/ScheduledTaskController.java`, add:
  ```java
  @PostMapping
  public ResponseEntity<ScheduledTaskDto> create(@Valid @RequestBody ScheduledTaskCreateRequest req) {
      ScheduledTaskService.CreateTaskCommand cmd = new ScheduledTaskService.CreateTaskCommand(
              req.getOrgId(), req.getLocationId(), req.getUserId(), req.getInstructionText(), null,
              req.getCronExpression(), req.getRunAt(), req.getTimezone(), req.getAutonomyMode(),
              req.getConditionalThresholdDescription(), req.getMaxDurationMinutes(),
              req.getNotificationChannel(), req.getNotificationRecipient(),
              ScheduledTaskCreatorType.EXTERNAL_SERVICE);
      ScheduledTask saved = taskService.createTask(cmd);
      return ResponseEntity.created(URI.create("/api/agent/scheduled-tasks/" + saved.getId()))
              .body(ScheduledTaskDto.from(saved));
  }
  ```
  Add imports: `jakarta.validation.Valid`, `com.pallet.agent.dto.ScheduledTaskCreateRequest`, `com.pallet.agent.entity.ScheduledTask`, `com.pallet.agent.entity.ScheduledTaskCreatorType`. `URI` is already imported in this file (used by `runOutput`).
  - Route: bare `POST /api/agent/scheduled-tasks` (pairs with the existing bare `GET ''` list route — the only other truly resource-creating spot in this controller).
  - Response is `201 Created` + `Location` header — deliberately different from this file's other `200 OK` responses, since every other POST here is a state transition on an already-existing row, not a creation.
  - `IllegalArgumentException`s thrown inside `createTask` (invalid cron, CONDITIONAL without threshold, etc.) are already caught globally by `GlobalExceptionHandler.handleIllegalArgument` (`GlobalExceptionHandler.java:89-93`) → rendered as a `400 ProblemDetail`. No extra try/catch needed.
  - No shared mapper/extraction needed between this and `ScheduledTaskTool.buildCommand`: the JSON body carries typed fields (`AutonomyMode`, `LocalDateTime`) so Jackson deserializes them directly with no `blankToNull`/manual-parse logic — that logic exists in the tool layer only because the ADK function-tool schema format is flat strings. The one thing genuinely shared (CONDITIONAL-requires-threshold, exactly-one-of-cron/runAt, cron validation, timezone default) already lives in exactly one place, `ScheduledTaskService.createTask`/`computeInitialNextRunAt`, which both entry points already funnel through.
- [x] Verify:
  - `POST /api/agent/scheduled-tasks` with a JSON body (`orgId`, `userId`, `instructionText`, `cronExpression`, `autonomyMode: "AUTONOMOUS"`) → `201` + `Location` header + `ScheduledTaskDto` body, `nextRunAt` populated, `status: "ACTIVE"`.
  - `GET /api/agent/scheduled-tasks/{id}?userId=...` (or a direct SQL check) confirms `creatorType = "EXTERNAL_SERVICE"`.
  - `POST` with `autonomyMode: "CONDITIONAL"` and no `conditionalThresholdDescription` → `400 ProblemDetail` mentioning CONDITIONAL.
  - Re-run the Phase 2 conversational-path check to confirm it's still unaffected.
  Confirmed 2026-08-20 against dev DB (orgId=RET_360): `POST` created `TASK-000025` — `201`, `Location: /api/agent/scheduled-tasks/TASK-000025`, body had `creatorType:"EXTERNAL_SERVICE"`, `status:"ACTIVE"`, `nextRunAt` populated; `GET` round-tripped the same; CONDITIONAL-without-threshold returned `400` with `"autonomyMode=CONDITIONAL requires a conditionalThresholdDescription (decision #11)."`; conversational `listScheduledTasks` still works and shows both TASK-000024 (AGENT) and TASK-000025 (EXTERNAL_SERVICE).

---

## Risks / explicitly out of scope (not addressed by this plan)

- **No auth on the new endpoint** — carried over from the rest of `ScheduledTaskController`, but this route is now reachable by direct HTTP callers (not just gated behind the LLM tool-call surface), which somewhat raises practical exposure versus today. Worth a follow-up ticket to wire up the existing (currently inert) `ROLE_SERVICE`/`ServiceJwtAuthFilter` mechanism.
- **No "confirm before creating" discipline for external callers** — the conversational path's prompt instructs the model to echo a summary and get explicit confirmation before persisting (itself only prompt-enforced, not code-enforced, per `docs/scheduled-tasks-execution-plan.md`'s own Risks section). A direct API caller has no equivalent step — any caller with network access can create an `AUTONOMOUS` recurring task immediately.
- **Template-based external creation is not included** — `ScheduledTaskCreateRequest` only covers the free-form path; extending to `createScheduledTaskFromTemplate`'s equivalent (templateId + placeholder values) is a natural but separate follow-up.
- **`creator_type` stays nullable** — intentional for existing-row safety; tightening it to `NOT NULL` later requires a coordinated backfill (`UPDATE scheduled_task SET creator_type = 'AGENT' WHERE creator_type IS NULL`) first.
