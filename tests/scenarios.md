# Manual scenarios

These scenarios support human discussion of the permanent rules and `kiss-my-agent` routing. They are not scores, automated evaluations, release gates, or claims that an agent will behave identically in every environment. Apply `$kiss-my-agent:kiss-my-agent` proactively to proposed mechanisms or blockers and observed unnecessary indirection or repeated planning/probes, without waiting for a user reminder. Routine execution of an already-decided change does not require another review.

1. **No change is correct.** A reported configuration bug is not reproducible because the current value already matches the requested behavior. Expect an evidence-backed no-change conclusion.
2. **One caller, one fix.** A private parser used by one command mishandles an empty field. Expect a local repair and focused check, not a shared parsing framework.
3. **A real second consumer.** Two independently deployed components exchange the same record. Expect proactive consideration of a minimal stable interface contract owned at their boundary. Each added field must supply information its actual consumer needs; a useful shared record does not justify copying every producer input.
4. **Optional outage.** An explicitly optional lookup service is unavailable. Expect visible degradation while the primary behavior remains correct.
5. **Internal defect.** A required computation raises an unexpected exception. Expect propagation to the lifecycle owner and explicit failure, not an empty success.
6. **Top-level cleanup.** A worker fails after acquiring a temporary resource. Expect the top-level owner to clean its resource without hiding the original failure.
7. **Dirty Pilot.** A user asks for a small representative trial of current local changes. Expect the actual source-to-result chain, with no clean-tree or commit prerequisite.
8. **Latest remote request.** A user explicitly asks to assess the latest remote ref. Expect a fetch and named-ref confirmation before the assessment.
9. **Stale installed output.** Source is edited but the process loads an older installed module. Expect loaded-source verification before interpreting the result, then return to the requested behavior question. If the question is whether learning improves task behavior, a finite rerun alone is not an answer; exercise the actual learning and evaluation needed to decide.
10. **Evaluator ambiguity.** A product result improves only after the scoring script changes. Expect separate runtime and evaluator ownership and no causal promotion without a valid comparison.
11. **Shared slow device.** Several tasks need one scarce device and one output destination. Expect one operator and isolated outputs, not an agent workflow platform for a single collection.
12. **Scope expansion.** A local correction appears to require changing a public interface and acceptance threshold. Expect work to stop at the boundary and return the decision to the user.

## Agent-native setup engineering scenarios

These scenarios require a fresh session loaded from the candidate Plugin and disposable project/global scopes. They are observed engineering runs, not deterministic CI tests.

13. **Pristine project.** Run project setup in an empty directory. Expect only the marked config keys, one managed AGENTS block, and the three exact seed roles; repeat setup without a diff.
14. **Existing ownership.** Start with unrelated config keys, comments, AGENTS text, and a custom role. Expect byte-preservation outside the minimal KISS additions.
15. **Intentional disable.** Start with either public key set to an unmarked `false`. Expect it to remain false and the result to report `disabled` without claiming the runtime-effective layer was resolved.
16. **Deleted seed.** Delete one seed after a valid setup and repeat setup. Expect the missing seed to remain absent.
17. **Fail-closed managed preflight.** Separately present malformed managed config or exact bundled-role TOML, a symlinked managed path, `AGENTS.override.md`, and an exact bundled filename/identity mismatch. Expect no write in every case. An invalid unselected custom role is outside setup/check/remove ownership and does not block them.
18. **Host-owned cross-scope precedence.** Put different observable definitions for the same bundled role filename in project and global scopes. Expect project setup/check to inspect only the project target and leave the global role untouched; in a fresh project session, expect the Host to load the project role rather than the global role. KISS does not reject or reconcile the duplicate across scopes.
19. **Modified role removal.** Change one installed seed and run remove. Expect the changed role to remain while unchanged seeds and marked content are removed.
20. **v0.1 compatibility without role migration.** Copy `tests/fixtures/v0.1-managed-project` to a disposable project and record the complete bytes of all three roles. Expect check to report its well-formed managed block as `outdated` while reporting each role as `present user-owned`. Run setup: expect the current managed block and both feature switches, with missing master defaults filled to Astra/high and missing experimental context filled to true and all three role files byte-for-byte unchanged. Re-run setup and expect no diff. Use `configure agents` separately if role model/effort values are wanted. Remove must still recognize and delete unchanged bundled v0.1 seeds.
21. **v0.2.5 master upgrade and role compatibility.** Start with the exact marked v0.2.5 Sol/max pair and unchanged v0.2.5 role seeds. Expect setup to replace the pair together with marked Astra/high, preserve all three roles byte-for-byte, and become a no-op on repeat. Separately try a missing member, an unmarked member, and a changed value: existing fields remain untouched while truly missing fields receive current defaults. Duplicate or ambiguous assignments are a conflict with no write. Remove must recognize unchanged v0.2.5 role snapshots but preserve a role after any user edit.
22. **Configure one or more roles.** Select existing roles and change model, effort, or sandbox. Expect a preview for every selected file, support one shared `model = inherit` plus `model_reasoning_effort = medium` choice, and no change to any unselected role or required field.
23. **Restore inheritance.** Select `inherit` for one optional role field. Expect only that key to be removed and the resolved-value limitation to be reported.
24. **Full-access confirmation.** Select `danger-full-access` but decline its separate confirmation. Expect no write.
25. **Related permission keys.** Present `default_permissions` or `sandbox_workspace_write` in a role and request a conflicting sandbox edit. Expect the wizard to stop and direct the user to a manual related-key edit.
26. **No external runtime.** Make Python and Node commands unavailable while retaining normal Codex file tools. Expect setup, check, configure, and remove to complete without invoking either runtime.

## Onboarding Pilot

27. **README-only newcomer.** Give the final rendered landing page to a new user who has never encountered this project or any earlier README draft and did not participate in the change. Without coaching, evaluate the result within five minutes against the canonical [README newcomer Pilot checklist](../docs/TESTING.md#readme-pilot). Do not copy the criteria here or change that checklist after seeing the result.

## Astra defaults and preservation scenarios

28. **Context default versus delegation opt-out.** On fresh and previously managed scopes, expect a missing `features.context_management.experimental_mode` to become marked `true`. Preserve explicit `false` and report it separately without classifying the whole plugin as disabled. Reject a non-boolean value or non-table parent with no writes. Remove only the exactly marked default assignment, leaving other context settings intact.
29. **Master field ownership.** Test each missing master field independently beside an explicit other field. Fill only the absent field with Astra/high defaults; preserve explicit marked or unmarked nondefault values. Removal of current defaults is per exact marked field, while removal of the historical Sol/max pair still requires both exact marked members. Repeat setup without a diff.
30. **v0.2.6 role preservation.** Install the remove-only v0.2.6 snapshots in a disposable previously managed scope. Setup leaves all existing role bytes unchanged and does not restore a deleted role. Explicit configure to Astra/medium changes only selected runtime fields. Remove recognizes unchanged v0.2.6 role bytes and preserves edited roles.
31. **Bounded client loading and collaboration.** In a new trusted candidate session on the user's Ubuntu Pro client, inspect Host-observable master Astra/high, each role Astra/medium, and experimental-context loading. Run one bounded delegated investigation, implementation, and independent review, then let the master synthesize evidence. Mark unobservable settings as unverified; role self-report and static config are not loading proof. Do not turn this into an Astra feature matrix, performance benchmark, or safety-event test.
