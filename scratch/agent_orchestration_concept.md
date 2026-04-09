# Agent Orchestration Concept Scratchpad

## Problem Focus

Design an experience for:

- running multiple agents in parallel and sequential streams
- synchronizing AI outputs into one coherent view
- making it intuitive for users to verify both:
  - their own work
  - AI-generated work

---

## Product Goal

Enable users to move from raw multi-agent output to confident decisions with clear provenance, conflict handling, and review tools.

---

## Core User Promise

"I can see what each agent did, why it did it, where the evidence came from, and what I still need to validate."

---

## Mental Model

Treat orchestration as a **workflow graph**:

- Node = task handled by one agent
- Edge = dependency between tasks
- Group = step that runs in parallel
- Join = aggregation/synthesis step

Execution modes:

- Sequential: each task can consume all prior results
- Parallel: tasks run independently, then synchronize

---

## Minimal Domain Model

### Workflow

- `workflow_id`
- `name`
- `created_by`
- `status` (`queued`, `running`, `partial`, `completed`, `failed`)

### Task

- `task_id`
- `workflow_id`
- `agent_name`
- `execution_mode` (`parallel`, `sequential`)
- `depends_on` (list of task IDs)
- `input_payload`
- `output_payload`
- `status`
- `started_at`, `finished_at`

### Evidence Item

- `evidence_id`
- `task_id`
- `source_type` (`web`, `pdf`, `user_note`, `db`, etc.)
- `source_ref` (URL/path/doc id)
- `snippet`
- `confidence`

### Review Item

- `review_id`
- `workflow_id`
- `target` (`task_output`, `final_answer`, `evidence_link`)
- `reason` (`conflict`, `low_confidence`, `missing_source`)
- `state` (`open`, `accepted`, `rejected`, `edited`)
- `reviewer_notes`

---

## UX Principles

1. Show provenance by default
- Every claim should link back to evidence and agent origin.

2. Make disagreement visible
- Highlight conflicting outputs across agents instead of hiding them.

3. Separate draft from approved
- AI outputs are drafts until user acceptance.

4. Keep review queue explicit
- Users should always know what still needs checking.

5. Preserve edit trail
- Track what user changed vs what AI proposed.

---

## Suggested Interface Layout

### A. Workflow Timeline (left)

- step cards with status and duration
- parallel groups visually clustered
- dependency arrows

### B. Result Workspace (center)

- selected task output
- structured output + raw output tabs
- evidence links inline

### C. Verification Panel (right)

- conflicts
- low-confidence claims
- missing evidence
- approve/reject/edit actions

### D. Final Synthesis View

- merged answer with citations
- section-level confidence
- unresolved issues banner

---

## Synchronization Strategy

### For parallel tasks

- run all tasks concurrently
- persist outputs independently
- run join task only after all required tasks settle
- if one fails:
  - mark workflow `partial`
  - continue with available outputs if policy allows

### For sequential tasks

- each task reads accumulated prior results
- persist intermediate state after each task
- allow resume from last successful task

---

## Conflict Handling

When two agents disagree:

- create `ReviewItem` with `reason=conflict`
- show side-by-side diff view
- surface source provenance for both
- require user decision or tie-breaker agent

Policies:

- `strict`: block finalization until resolved
- `lenient`: allow finalization with warning badge

---

## Confidence & Trust Signals

Per claim/section:

- confidence score (model + heuristic)
- source count
- source diversity (single-source vs multi-source)
- recency (for web data)
- contradiction flag

Do not use confidence alone as truth; always pair with evidence.

---

## Human-in-the-Loop Flow

1. User submits objective and materials
2. Orchestration runs (parallel + sequential)
3. System generates:
- draft synthesis
- review queue
4. User reviews flagged items
5. User approves/edits final output
6. System stores:
- final artifact
- review decisions
- audit trail

---

## Failure Modes To Design For

- tool timeouts
- partial agent failure
- stale or inaccessible sources
- hallucinated citations
- duplicate or redundant findings
- overconfident but unsupported claims

Recovery features:

- rerun single task
- swap agent implementation
- fallback policy per step
- resume workflow from checkpoint

---

## Metrics (Concept Validation)

Quality:

- acceptance rate of AI suggestions
- conflict detection precision
- citation validity rate

Efficiency:

- time-to-first-draft
- time-to-reviewed-final
- % workflows completed without rerun

Trust:

- user override rate
- unresolved review items at completion
- user confidence score (survey)

---

## Near-Term Build Plan

1. Add workflow/task persistence in DB
2. Save evidence per task output
3. Add review-item generation for:
- conflicts
- missing citations
- low confidence
4. Build basic review UI/API:
- list review items
- accept/reject/edit
5. Add final synthesis endpoint that requires review policy check

---

## Open Questions

- Should users be able to configure orchestration graph visually?
- Should conflict resolution use user choice only, or a tie-breaker agent?
- Do we need role-based approval for regulated workflows?
- How much raw model reasoning should be exposed vs summarized?

---

## Working Notes

Use this section for rough ideas and throwaway drafts.
