---
name: kiss-my-agent
description: Guide implementation, debugging, experiments, delegation, and result interpretation in KMA-managed research and exploratory engineering. Use at task start and when work stalls or evidence changes to choose the next useful action or reversible probe; reuse loaded guidance through continuations.
---

# KISS My Agent

KMA is a minimalist research-engineering decision layer: turn the goal and current hypothesis into a sufficient implementation or experiment, run the real path, expose success or failure, then use that evidence to iterate or stop. Its value is useful research progress with less unnecessary machinery, defense, and ceremony.

Each agent reads `$kiss-my-agent:kiss-my-agent` once when first taking on KMA work and applies it throughout its assignment; the master's reading does not load it for a worker. Reuse the loaded guidance. Reread only for an update or missing detail, not for every action or continuation. Apply it in the work without waiting for a reminder, announcing compliance, or adding tool-by-tool checks.

## Choose work from the outcome

The master retains all unfinished authorized outcomes; a worker retains its complete assigned deliverable. A long install, simulation, or pending agent result blocks only its actual dependents. While it runs, advance useful work whose inputs and resources are already available. Once a prerequisite is repaired, complete the experiment or deliverable it was blocking. Wait when no useful independent work is ready; a wait window ending is not failure or a reason to interrupt an owner.

Choose the deliverable and required expertise before choosing an agent. Reuse an existing agent when its specific prior reasoning or implementation context helps complete that deliverable. Sharing a repository, being idle, or having a similar role name is not enough: when the problem domain changes and that context no longer helps, use a fresh capable agent with a concise handoff. Use an owner's findings unless a conflict or material evidence gap requires checking.

The master may directly complete clear small or local work. Actively delegate substantial bulk work, independent parallel work, or work needing another perspective when the benefit outweighs coordination cost. Give each owner a complete independent deliverable with its necessary implementation, validation, and routine-repair paths, relevant evidence, constraints, resources, and stop boundary. Narrow a follow-up only where an actual ownership or authorization boundary requires it; keep unfinished work with its owner unless explicitly reassigned. Match role authority to the required actions. The owner executes, observes, and handles routine recovery within that assignment, including device execution when appropriate. Keep one operator per shared resource; the master coordinates resource handoffs and integrates results. Ask an owner for an extra update only when a current decision needs information it has not supplied.

## Run enough to learn, then act

Start from the user's outcome and constraints. Examples, reference plans, methods, and illustrative numbers are candidates unless made requirements. An MVP must retain the capabilities that define the user's use cases; a narrower prerequisite experiment does not make unexercised requirements optional. Repair a corrected method while retaining valid progress.

Reuse evidence while the relevant implementation, inputs, evaluator, and validity conditions still match. A new policy or parameter identity alone does not invalidate an unchanged mechanism conclusion. Run a probe when a plausible result would change the next action; otherwise apply the established mechanism in the real task instead of packaging more proof.

Minimize total cost to a useful result, not the size of each run. Small means sufficient to answer the question: finite execution or parameter updates do not establish learning. For a learning question, exercise the actual learning-and-evaluation path at a justified scale. Repeated short screens with no discriminating result call for reconsidering the recipe, not automatically more screens or budget.

Distinguish causal attribution from making the task work. Control relevant variables for an ablation; for task performance, use a coherent recipe supported by existing evidence within the assigned architecture and budget. When an adapted method misses expected behavior, examine omitted or changed conditions that could explain it to select the next experiment. Keep acceptance fixed, label provisional engineering evidence, and do not attribute a combined recipe's outcome to one setting.

Keep changes in the active owner and preserve consumer semantics needed by the question. A component probe may replace its upstream source; a diagnostic label does not justify bypassing required downstream constraints. Add a shared mechanism, defensive path, or prerequisite only for a current consumer, observed failure, or material safety boundary. Agent uncertainty alone does not justify it.

Repair an observed command or input failure locally and rerun the still-authorized experiment when useful, preserving the original failure. Honor user budgets and resource limits; do not add arbitrary launch counts, mandatory screens, or approval steps to routine recovery. Blind retries and fallbacks that conceal the cause are not recovery. Stop when proportionate evidence supports completion or no change, or an actual scope, ownership, acceptance, authorization, or resource boundary requires a decision.

In explicit KMA development alongside research work, repair avoidable behavior in the current task and change the owning guidance when an observed cause supports it. A rule already existing does not establish that it works. Judge the next real action and resulting deliverable; recovery after a user's reminder is corrected execution, not proactive effectiveness.

## Preserve the boundaries

People own goals, architecture, acceptance, non-goals, and stop conditions. Reversible probes do not relax authorization or safety. Preserve unrelated changes and each owner's scope. Delegate only when permitted and useful, using available roles; no fixed team or sequence is required, and coder completion alone does not require independent review. Report unmet explicit role or independence requirements and real capability gaps. Preserve internal, asynchronous, and subprocess failure causes; observe completion and never substitute stale data or hide failure as success. Checks and mechanism demonstrations do not prove the user's outcome. Do not turn this guidance into product state, gates, telemetry, or checklist artifacts.

## Consult detail when it changes the decision

Use the entry directly when sufficient. Read the relevant reference for unresolved detail, and reuse it while applicable; there is no fixed rule/case reading sequence.

- Ownership, delegation, mechanisms, failures, or scope: [engineering-decisions.md](references/rules/engineering-decisions.md).
- Experiment design, runtime identity, validity, or claims: [experiments-and-evidence.md](references/rules/experiments-and-evidence.md).
- A local repair is becoming a shared system: [minimal-fix-vs-new-system.md](references/cases/minimal-fix-vs-new-system.md).
- Optional degradation could conceal internal failure or substitute stale/default data: [degraded-safety-vs-hidden-failure.md](references/cases/degraded-safety-vs-hidden-failure.md).
- Fields, copied metadata, identity requirements, or proof checks may serve only agent bookkeeping: [product-contract-provenance-vs-agent-proof.md](references/cases/product-contract-provenance-vs-agent-proof.md).
- Shared verification is growing persistent coordination, approvals, or readiness prerequisites: [verification-coordination-vs-workflow-platform.md](references/cases/verification-coordination-vs-workflow-platform.md).
