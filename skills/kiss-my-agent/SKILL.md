---
name: kiss-my-agent
description: Choose the next useful action in KMA-managed research and engineering. Apply when designing, implementing, debugging, choosing experiments, dividing work, or interpreting results, including before adding mechanisms, checks, or prerequisites. Load once and reuse proactively through the work; do not wait for a stall or user reminder.
---

# KISS My Agent

KMA guides action selection: implement or experiment, run the real path, expose the result, then iterate or stop. Choose work that can change the implementation, resolve the research question, or complete the requested deliverable. Reading this Skill activates guidance; useful subsequent behavior establishes its value.

Each agent reads `$kiss-my-agent:kiss-my-agent` once when first taking on KMA work; the master's reading does not load it for a worker. Reuse it through continuations and corrections, rereading only for an update or missing detail. Apply it without waiting for a reminder, repeated compliance announcements, or tool-by-tool checks.

## Choose the next useful action

Start from the unfinished user outcome, available evidence, and question preventing completion. Choose the smallest sufficient implementation or real experiment that answers it. Minimize cumulative cost to a useful result, including preparation, repeated probes, model input, and analysis. When the question is resolved, use the result and finish the deliverable.

- **Settle the user's outcome first.** Use the user's acceptance and metric priorities. Report task completion, mechanism attribution, and cost separately: success with higher cost remains success with a tradeoff; faster failure is not an efficiency gain. Component non-use does not erase task success, and task success does not establish component or paper contribution.
- **Keep the task's legal capabilities.** An MVP is the smallest complete task chain within the selected scope. Adapters must preserve its native observations, reads, revisits, repeated views, actions, and recovery choices. Enforce actual operation contracts; give estimates and strategy preferences to the decision maker as evidence rather than silently turning them into prohibitions. Identical restrictions in both arms do not establish a valid comparison.
- **Reach an actual consumer.** Follow one real request through information delivery, selection, execution, feedback, and the next action. Repair the first observed break before widening fields or mechanisms. Saved information and passing interface tests do not establish that the deciding agent received or used it. Preserve required downstream semantics in probes.
- **Run enough to answer the question.** Distinguish functional smoke, mechanism validation, task performance, and paper evaluation. Check decisive prerequisites with the shortest real execution. End local diagnosis when its blocking question is resolved and return to the original task; repeated small tests do not replace a justified complete run.
- **Let negative evidence change the next action.** For an untriggered mechanism, distinguish an unreachable consumer, no relevant decision opportunity, and autonomous non-use despite availability. Repair delivery, choose a legally relevant scenario, or retain non-use accordingly. Repeat only with a new discriminating basis or a declared variability question; do not force use or run until success.
- **Complete the research and delivery loop.** After a material repair, decide whether it restored engineering function or tested a distinguishing hypothesis. A valid negative result can support stopping. If a defect invalidates a comparison, stop the affected run, retain failure and cost, repair it, and freeze a separate valid comparison. Deliver the final user-facing step, including the access lifetime needed to use the result.

An added mechanism, check, or prerequisite needs a current consumer, observed failure, or material boundary. Agent uncertainty alone is insufficient. Keep single-caller work local. Reuse applicable evidence and owner findings; refresh only facts made stale by changed inputs, implementation, evaluator, ownership, or instructions. New fields serve current consumers; keep raw evidence traceable without copying development metadata into product or model inputs. After a user correction, replace obsolete current instructions and keep the history separately.

## Give owners complete deliverables

The master retains every unfinished authorized outcome. A worker owns its complete assigned deliverable through execution, completion observation, and routine recovery. Advance ready independent work while a dependency runs; when nothing useful is ready, wait. A wait window ending is not failure, and communication cadence does not require another status read.

Choose the deliverable and expertise before the agent. The master may finish clear small or local work directly. Actively delegate substantial independent or bulk work, or work needing another perspective, when permitted and the benefit outweighs coordination cost. Supply the outcome, relevant context, authority, resources, validation, and stop boundary; no fixed team or review sequence is required. Keep one operator per shared resource. Integrate owner results without redoing their work; extra reads or status requests need a current evidence gap, conflict, or reassignment.

Reuse an agent only when its prior context fits and its model and reasoning effort match the current master choice. Default new children inherit both settings; omit model and effort overrides. After a master setting change, let in-flight work finish, then safely hand off subsequent work to a fresh matching agent rather than reusing a mismatched one. Explicit user overrides remain explicit exceptions. Missing Host diagnostics leave matching unverified, not assumed. Do not add a settings registry or interrupt an operation merely to switch settings.

## Preserve boundaries and finish

People own goals, architecture, acceptance, non-goals, and stop conditions. Preserve unrelated work and each owner's scope. Reversible probes do not relax authorization or safety. Internal, asynchronous, and subprocess failures retain their causes; observe completion and never replace failure with stale data or success. Routine local recovery stays within the assignment; actual ownership, public-interface, resource, authorization, or acceptance boundaries return to the user. Stop at proportionate completion, supported no change, or a real boundary.

In KMA development, correct avoidable execution now and change guidance only where an observed gap supports it. Rules, loading, delegation, and test totals do not prove effectiveness. Judge later real actions, user corrections, invalid work avoided, and usable deliverables; recovery after a reminder is corrected execution. Do not turn KMA into product state, gates, telemetry, or checklist artifacts.

## Consult detail when it changes the decision

Read only the relevant reference and reuse it while applicable; there is no fixed reading sequence.

- Ownership, capability boundaries, failures, or scope: [engineering-decisions.md](references/rules/engineering-decisions.md).
- Experiment design, non-use, validity, or claims: [experiments-and-evidence.md](references/rules/experiments-and-evidence.md).
- Consumer breaks, untriggered mechanisms, success/cost, invalid comparisons, or inaccessible delivery: [research-action-selection.md](references/cases/research-action-selection.md).
- A local repair becoming a shared system: [minimal-fix-vs-new-system.md](references/cases/minimal-fix-vs-new-system.md).
- Optional degradation concealing internal failure: [degraded-safety-vs-hidden-failure.md](references/cases/degraded-safety-vs-hidden-failure.md).
- Fields or proof checks serving only bookkeeping: [product-contract-provenance-vs-agent-proof.md](references/cases/product-contract-provenance-vs-agent-proof.md).
- Verification growing coordination prerequisites: [verification-coordination-vs-workflow-platform.md](references/cases/verification-coordination-vs-workflow-platform.md).
