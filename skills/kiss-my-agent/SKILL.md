---
name: kiss-my-agent
description: Use only when a research-engineering task has a non-obvious decision about a persistent or shared mechanism, a local fix versus a new system, a reversible probe versus more planning or a new mechanism, experiment validity or evidence strength, runtime versus evaluator ambiguity, or expansion of scope or acceptance. Do not use for an already-decided implementation, ordinary small fix, mechanical edit, routine test or build, Git operation, lookup, or formatting.
---

# KISS My Agent

Invoke this skill explicitly as `$kiss-my-agent` to resolve one consequential ambiguity, then return to the task. It is not a general workflow.

1. Name the ambiguity and its current consumer or decision.
2. Read exactly one relevant rule file:
   - engineering ownership, mechanisms, failures, or scope: [engineering-decisions.md](references/rules/engineering-decisions.md)
   - experiments, versions, runtime identity, or claims: [experiments-and-evidence.md](references/rules/experiments-and-evidence.md)
3. If a concrete contrast would decide the issue, additionally read exactly one matching case:
   - [minimal-fix-vs-new-system.md](references/cases/minimal-fix-vs-new-system.md)
   - [degraded-safety-vs-hidden-failure.md](references/cases/degraded-safety-vs-hidden-failure.md)
   - [product-contract-provenance-vs-agent-proof.md](references/cases/product-contract-provenance-vs-agent-proof.md)
   - [verification-coordination-vs-workflow-platform.md](references/cases/verification-coordination-vs-workflow-platform.md)
4. Apply the narrowest applicable guidance. Do not read all rules or cases, create a checklist artifact, or add a mechanism merely to demonstrate compliance.
