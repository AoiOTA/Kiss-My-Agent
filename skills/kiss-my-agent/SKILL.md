---
name: kiss-my-agent
description: Read at the start of each KMA-managed assignment, then apply when choosing or changing the next action, dividing work, or interpreting research results or execution status. Guide engineering and evidence decisions, including a reversible probe, without waiting for the user to invoke KMA. Already-decided mechanical execution does not require repeated reading or review.
---

# KISS My Agent

At the start of each KMA-managed assignment, each agent reads the current `$kiss-my-agent:kiss-my-agent` entry once before judging which guidance applies; the master's reading does not substitute for a worker's. Before choosing or changing the next action, dividing work, or concluding what research results or execution status mean, use the routing below without first requiring the decision to seem non-obvious or mechanism-related. Reuse already-read guidance while it remains applicable; already-decided mechanical execution needs no repeated reading, extra review, or record.
1. Identify the current decision and the assigned outcome it serves.
2. Read exactly one relevant rule file:
   - engineering ownership, mechanisms, failures, or scope: [engineering-decisions.md](references/rules/engineering-decisions.md)
   - experiments, versions, runtime identity, or claims: [experiments-and-evidence.md](references/rules/experiments-and-evidence.md)
3. When considering an action below, additionally read exactly one matching case before deciding. Match the proposed behavior, not component names:
   - Expanding a local repair into a shared system: [minimal-fix-vs-new-system.md](references/cases/minimal-fix-vs-new-system.md).
   - Reclassifying internal errors as optional degradation, substituting stale/default data or empty success, or continuing after failure: [degraded-safety-vs-hidden-failure.md](references/cases/degraded-safety-vs-hidden-failure.md).
   - Adding fields, copied metadata, identity requirements, or proof checks: [product-contract-provenance-vs-agent-proof.md](references/cases/product-contract-provenance-vs-agent-proof.md).
   - Adding persistent coordination, approvals, or readiness prerequisites for shared verification: [verification-coordination-vs-workflow-platform.md](references/cases/verification-coordination-vs-workflow-platform.md).
4. Apply the narrowest applicable guidance. Do not read all rules or cases, create a checklist artifact, or add a mechanism merely to demonstrate compliance.
