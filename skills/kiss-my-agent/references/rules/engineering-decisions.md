# KISS engineering decisions

This rule applies the permanent boundaries to mechanism, ownership, failure, and scope decisions. It does not replace project ownership or user acceptance.

## Size, ownership, and delegation

Estimate work by uncertainty, coupling, consequence, and verification cost, not line count. Use the entry's outcome, ready-work, and context-fit guidance. The master owns orchestration, architecture, acceptance, conflict resolution, and evidence interpretation; workers own their complete assigned deliverables. An existing agent's specific prior context must help the new work, not merely concern the same project. Its model and reasoning effort must also match the current master choice, unless explicitly overridden by the user. New children inherit both settings without invocation overrides. After a master setting change, let in-flight operations finish and transfer subsequent work to a fresh matching agent; do not interrupt active operations or create a settings tracker to implement this boundary. A domain change calls for a fresh context when the old reasoning is no longer useful.

Multi-agent work is available by default unless disabled by the user or effective configuration. Use the current Host role catalog; shipped roles are mutable seeds. Each role may have zero, one, or multiple instances. Coordination is flat by default. Only when an independent subsystem needs substantial parallel work and direct aggregation would pollute the master's context may one agent receive a bounded department-lead assignment. It may delegate within that scope, but its workers must not delegate again. Keep at most one intermediate management layer and no deep nesting; that assignment ends with the task. If delegation is unavailable, continue authorized work within capability without a staffing approval step; report unmet explicit role or independence requirements and real capability gaps.

A pending final result blocks only its actual dependents. Use the available inputs to complete independent parts of the goal; do not ask idle owners for repeated updates. A wait window ending without an update is not an agent timeout or failure. Interrupt only when the work is obsolete, out of scope, conflicting, or explicitly stopped.

Trace the active owner, producer, and current consumer before choosing the modification surface. Keep a single-caller need local. Extract or share only at a real interface boundary or when another present consumer makes duplication materially worse. A supported conclusion that no change is needed is complete work.

When instructions, target, version, owner, launch source, or main hypothesis changes, refresh only the facts made stale and repartition the task if necessary. Otherwise reuse stable local context. Verify the dependency source actually loaded when source, generated output, installed artifact, configuration, data, or process identity could diverge.

## Preserve capability and the real consumer

A smallest implementation retains the complete task chain for the selected scope. A narrower prerequisite experiment cannot redefine the user's system. At an adapter boundary, preserve native legal observations, reads, repeated views, revisits, actions, and recovery. A simulator's invalid-action contract or an actual permission boundary can reject an operation. An estimated map, category match, previously seen view, or prior collision does not alone establish that rejection is required; keep such information available to the deciding agent. Inspect test expectations when they encode a restriction: passing tests can preserve the wrong research object. Applying a restriction to both comparison arms controls that difference but does not show that either arm still tests the intended capability.

Follow one actual request through the active entry, delivered input, deciding consumer, selected action, execution feedback, and next decision. Use concrete input or output at the first observed break; no universal tracing schema is needed. A suggested view must reach the real action choices, and an executed image must survive the actual visual-input handoff. Fix that break before adding more retrieval, fields, or mechanisms. Preserve the production input representation in replay unless its change is the tested factor; do not create an instrumentation-only failure by expanding shared references or bypassing downstream constraints.

Assess new fields at their consumers. Keep raw evidence traceable, but do not put paths, hashes, run identifiers, or packaging statistics into product or model inputs without a present decision need. After a user correction, replace superseded current rules instead of stacking competing instructions. Preserve the old decision in history and refresh only affected facts on continuation.

Delivery includes the last step required for use. If a page requires a server, verify access through the delivered entry and choose a lifetime appropriate to the requested use; a successful temporary preview is not proof of later availability. Use the existing suitable host or a self-contained artifact when appropriate, within authorization. Do not introduce a daemon or deployment merely because a file exists.

## Silent Rent Test

Before adding or retaining a nontrivial mechanism, answer silently:

1. Which current external consumer or explicit requirement uses it?
2. Which observed failure or high-consequence risk does it prevent now?
3. Would removing it change the requested outcome or evidence enough to justify its ongoing implementation and cognitive cost?

No answer is an instruction to keep the design local or remove the mechanism, not to write a Rent Test record. Several mechanisms with no external consumer cannot justify one another as a cluster.

Assess the added field, check, or indirection itself: what current consumer needs it, and what information or behavior does that consumer actually require? A useful enclosing mechanism does not justify copying or retaining all of its inputs.

## Mechanism semantics

This is a non-exhaustive semantic map, not a keyword gate. Mentioning a term does not automatically invoke the Rent Test; a new name with the same behavior belongs to the same class. A mechanism cluster without an outside consumer cannot establish value by internally consuming its own outputs.

| Class | Semantics to examine |
| --- | --- |
| Abstraction and indirection | wrappers, adapters, registries, dispatchers, factories, base layers, or generic frameworks that move behavior away from its only caller |
| Interface contracts | APIs, schemas, messages, version handshakes, compatibility promises, or validation at a real producer-consumer boundary |
| Validation governance | gates, readiness checks, promotion rules, policy engines, approval states, or validators that decide whether work may proceed |
| Evidence identity | receipts, hashes, attestations, manifests, lineage records, signatures, or identity tuples intended to prove what produced a result |
| State and lifecycle | durable stages, state machines, checkpoints, leases, ownership records, or transition protocols |
| Recovery and compatibility | retries, fallback, downgrade, migration, shims, legacy modes, recovery journals, or substitute data paths |
| Execution infrastructure | runners, orchestrators, queues, schedulers, daemons, worker pools, sandboxes, or command layers |
| Configuration and dependencies | new settings, feature flags, environment indirection, dependency injection, pins, or alternate providers |
| Persistent derived state | caches, indexes, snapshots, mirrors, databases, generated summaries, or synchronized copies of reconstructible facts |
| Observability and diagnosis | logs, metrics, tracing, dashboards, health endpoints, probes, or diagnostic exports |
| Tests, documentation, and delivery | harnesses, fixtures, golden files, runbooks, reports, packaging, release metadata, or handoff artifacts |
| Multi-Agent collaboration | role protocols, task packets, ledgers, shared agent state, handoff schemas, arbitration, or agent-performance telemetry |

## Local repair or new system

Prefer a local repair when the behavior has one owner and caller, the failure is narrow, and existing interfaces can express the correct result. Consider a new shared mechanism only when multiple current consumers need the same stable semantics or when a high-consequence boundary cannot be protected locally. Compare the deletion counterfactual: if removing the proposed system leaves the goal unchanged, it is not part of the minimum solution.

When genuine uncertainty remains, prefer the smallest safe, low-cost, reversible probe that can resolve it over more speculative planning or a new system.

Agent uncertainty and rule vocabulary are not product requirements. Words such as readiness, provenance, lifecycle, contract, goal, or evidence do not justify corresponding schemas or services. A self-created gate may help organize local work only while it remains disposable and cannot override, strengthen, or substitute for the user's goal and acceptance.

## Failure ownership

When repeated failures come from agent-authored commands or test or release assembly rather than the product path, first reduce the execution surface: use fewer commands with one purpose each, make the working directory explicit, reuse already resolved paths, and confirm required dependencies only where they are used. Remove self-created conditions instead of widening preflight, wrappers, or gates to repair the assembly; preserve the original cause and classify the failure as product, harness, or environment before changing the owning path.

Internal bugs, impossible states, corrupted required input, and invariant violations propagate with their original causes. Broad catch-and-continue, success sentinels, stale substitution, and relabeling internal failure as optional degradation are forbidden. A top-level lifecycle owner may catch to stop safely, clean owned resources, add context, or produce an explicit failed result, but it must rethrow, return an error, or exit nonzero; cleanup must not hide the primary failure.

Optional external capability may degrade only when the failure class is specific and expected, the remaining product behavior is correct without it, and the degraded reason is visible. Observe asynchronous work and subprocess completion at an owner boundary.

## Five-question review

Compose roles around the work, not a fixed pipeline. Before assigning independent review, identify the independent perspective that could change the decision, such as a hidden behavior, interface, or consequential scientific inference risk; coder completion alone is not a reason. For a local reversible change with sufficient validation, owner verification and master integration suffice. Do not routinely repeat checks already completed by a worker; the master retains architecture, acceptance, and evidence judgment.

An independent review asks only what matters:

1. Does actual behavior meet the user goal rather than merely pass checks?
2. Is the change in the correct owner with real consumer interfaces and invariants preserved?
3. Are failure, degraded, safety, asynchronous, and subprocess paths correct and observable?
4. Do current dependencies and evidence support only the stated claim?
5. Did the change add a mechanism without a current consumer or only for agent workflow?

Findings need an exact location, trigger, impact, and repair direction. Style or hypothetical future completeness is not a finding.

## Goal and stop boundary

Use goal tracking only when the user explicitly enables it. Thread state, checkpoints, budgets, and temporary progress may assist the active conversation, but must not become repository runners, readiness states, promotion logic, or product lifecycle. Stop when the requested behavior and proportionate evidence are complete, no change is supported, the same path yields no new information, or a scope, acceptance, ownership, irreversible-impact, shared-resource, or cost decision belongs to the user.
