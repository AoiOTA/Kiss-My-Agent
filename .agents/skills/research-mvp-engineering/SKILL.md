---
name: research-mvp-engineering
description: Use only when a research-engineering task has a non-obvious decision about a persistent or shared mechanism, a local fix versus a new system, experiment validity or evidence strength, runtime versus evaluator ambiguity, or expansion of scope or acceptance. Do not use for an already-decided implementation, ordinary small fix, mechanical edit, routine test or build, Git operation, lookup, or formatting.
---

# Research MVP engineering

Use this skill to resolve one consequential ambiguity, then return to the task. It is not a general workflow.

1. Name the ambiguity and its current consumer or decision.
2. Read exactly one relevant rule file:
   - engineering ownership, mechanisms, failures, or scope: `references/rules/engineering-decisions.md`
   - experiments, versions, runtime identity, or claims: `references/rules/experiments-and-evidence.md`
3. If a concrete contrast would decide the issue, additionally read exactly one matching case:
   - `references/cases/minimal-fix-vs-new-system.md`
   - `references/cases/degraded-safety-vs-hidden-failure.md`
   - `references/cases/product-contract-provenance-vs-agent-proof.md`
   - `references/cases/verification-coordination-vs-workflow-platform.md`
4. Apply the narrowest applicable guidance. Do not read all rules or cases, create a checklist artifact, or add a mechanism merely to demonstrate compliance.
