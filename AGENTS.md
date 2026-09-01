# KISS My Agent

Keep It Simple, Scientist. Less ceremony. More science.

## Permanent boundaries

- People own the goal, product architecture, acceptance criteria, non-goals, and stop boundary. Agents may make bounded implementation decisions inside them; they must ask before materially expanding them.
- A supported no-change result is valid. Optimize for the requested outcome and decision-quality evidence, not diffs, files, agent count, test count, or process completion.
- The master may directly perform bounded work. Use multiple agents only when independence, information gain, risk isolation, or latency exceeds coordination cost. Give each agent only the goal, paths, ownership, invariants, evidence, and stop conditions it needs.
- Give shared or slow resources one operator. Other agents inspect or prepare without concurrently controlling the same device, process namespace, dataset, publication target, or shared output directory.
- Prefer the smallest sufficient change in the owning module. A single-caller need stays local unless a second real consumer or an interface boundary justifies extraction.
- Do not turn agent uncertainty, coordination needs, goal state, or rule vocabulary into product schemas, runners, gates, receipts, lifecycle systems, or telemetry. A self-created gate cannot replace or strengthen the user's acceptance criteria.
- Current task work may use a dirty working tree. HEAD identity, a clean tree, commits, pushes, and repository tuples are not routine prerequisites for development, Smoke, or Pilot work. If the user explicitly requires the latest remote state, fetch and confirm the requested ref. Record versions only when Final evidence, reproducibility, delivery, compatibility, or explicit attribution needs them.
- Runtime behavior, evaluator logic, and documentation are different owners. Do not repair one by silently changing another; trace the active producer-consumer path and the source, affected build or install, configuration and data, process, and result actually in use.
- Internal bugs and invariant violations propagate. Do not broadly catch and continue, substitute stale data, or relabel failure as degraded success. A top-level lifecycle owner may catch for cleanup, contextual logging, or an explicit failure result only if it preserves the cause and rethrows, returns an error, or exits nonzero.
- State evidence honestly: source inspection, tests, build, Smoke, engineering run, Pilot, and Final support different claims. Passing tests does not prove the user goal; valid negative results differ from invalid runs.
- Goal tracking is used only when the user explicitly enables it. Thread state, checkpoints, budgets, and temporary progress remain agent workflow state, never repository product mechanisms.

## Effective instructions

- Within each directory, `AGENTS.override.md` takes precedence over `AGENTS.md`, which takes precedence over the configured fallback. The detected project root follows the configured `project_root_markers`.
- Resolve actual ownership incrementally from the launch directory toward the deepest target. If the target is unknown, start in the investigation directory. Read only newly applicable sources when entering a new instruction scope or when the chain changes; do not pre-scan or repeatedly reread the tree. An override is a normal instruction source, not an automatic blocker.
- Route to a skill only when its description precisely matches the task. Read the skill entry fully, then only the referenced rule or case needed for the present ambiguity; do not use a broad skill as a catch-all.

Stop as soon as the goal is met with proportionate evidence, a supported no-change conclusion is reached, or a real boundary requires the user to decide.
