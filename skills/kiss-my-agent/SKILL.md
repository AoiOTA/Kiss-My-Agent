---
name: kiss-my-agent
description: Apply proactively when research-engineering work proposes adding or expanding a persistent or shared mechanism or a blocking condition, changes failure or degradation handling, exposes unnecessary indirection or repeated planning/probes, or needs a decision about a reversible probe, experiment validity, evidence strength, runtime versus evaluator behavior, or scope and acceptance. Do not use for mechanical implementation of an already-decided change, routine tests or builds, Git operations, lookups, or formatting.
---

# KISS My Agent

Apply `$kiss-my-agent:kiss-my-agent` proactively to the current mechanism, failure-handling, or evidence decision without waiting for the user to name it, then return to the task. Each agent applies this routing to new decisions arising in its own execution; the master's reading does not substitute for the worker's. Mechanical implementation of an already-decided change does not require another review. It is not a general workflow.

1. Name the mechanism, blocking condition, failure-handling, or evidence decision and its current consumer.
2. Read exactly one relevant rule file:
   - engineering ownership, mechanisms, failures, or scope: [engineering-decisions.md](references/rules/engineering-decisions.md)
   - experiments, versions, runtime identity, or claims: [experiments-and-evidence.md](references/rules/experiments-and-evidence.md)
3. When considering an action below, additionally read exactly one matching case before deciding. Match the proposed behavior, not component names:
   - Expanding a local repair into a shared system: [minimal-fix-vs-new-system.md](references/cases/minimal-fix-vs-new-system.md).
   - Reclassifying internal errors as optional degradation, substituting stale/default data or empty success, or continuing after failure: [degraded-safety-vs-hidden-failure.md](references/cases/degraded-safety-vs-hidden-failure.md).
   - Adding fields, copied metadata, identity requirements, or proof checks: [product-contract-provenance-vs-agent-proof.md](references/cases/product-contract-provenance-vs-agent-proof.md).
   - Adding persistent coordination, approvals, or readiness prerequisites for shared verification: [verification-coordination-vs-workflow-platform.md](references/cases/verification-coordination-vs-workflow-platform.md).
4. Apply the narrowest applicable guidance. Do not read all rules or cases, create a checklist artifact, or add a mechanism merely to demonstrate compliance.
