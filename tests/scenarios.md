# Manual scenarios

These scenarios support human discussion of the permanent rules and `kiss-my-agent` routing. They are not scores, automated evaluations, release gates, or claims that an agent will behave identically in every environment. Invoke `$kiss-my-agent:kiss-my-agent` only for the non-obvious mechanism or evidence decisions below, not for routine execution.

1. **No change is correct.** A reported configuration bug is not reproducible because the current value already matches the requested behavior. Expect an evidence-backed no-change conclusion.
2. **One caller, one fix.** A private parser used by one command mishandles an empty field. Expect a local repair and focused check, not a shared parsing framework.
3. **A real second consumer.** Two independently deployed components exchange the same record. Expect consideration of a minimal stable interface contract owned at their boundary.
4. **Optional outage.** An explicitly optional lookup service is unavailable. Expect visible degradation while the primary behavior remains correct.
5. **Internal defect.** A required computation raises an unexpected exception. Expect propagation to the lifecycle owner and explicit failure, not an empty success.
6. **Top-level cleanup.** A worker fails after acquiring a temporary resource. Expect the top-level owner to clean its resource without hiding the original failure.
7. **Dirty Pilot.** A user asks for a small representative trial of current local changes. Expect the actual source-to-result chain, with no clean-tree or commit prerequisite.
8. **Latest remote request.** A user explicitly asks to assess the latest remote ref. Expect a fetch and named-ref confirmation before the assessment.
9. **Stale installed output.** Source is edited but the process loads an older installed module. Expect loaded-source verification before interpreting the result.
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
20. **v0.1 compatibility without role migration.** Copy `tests/fixtures/v0.1-managed-project` to a disposable project and record the complete bytes of all three roles. Expect check to report its well-formed managed block as `outdated` while reporting each role as `present user-owned`. Run setup: expect the current managed block and the missing marked master model/effort defaults, while all three role files remain byte-for-byte unchanged. Re-run setup and expect no diff. Use `configure agents` separately if current model/effort values are wanted. Remove must still recognize and delete unchanged bundled v0.1 seeds.
21. **Configure one role.** Select one existing role and change model, effort, or sandbox. Expect a preview, confirmation, and no change to any unselected role or required field.
22. **Restore inheritance.** Select `inherit` for one optional role field. Expect only that key to be removed and the resolved-value limitation to be reported.
23. **Full-access confirmation.** Select `danger-full-access` but decline its separate confirmation. Expect no write.
24. **Related permission keys.** Present `default_permissions` or `sandbox_workspace_write` in a role and request a conflicting sandbox edit. Expect the wizard to stop and direct the user to a manual related-key edit.
25. **No external runtime.** Make Python and Node commands unavailable while retaining normal Codex file tools. Expect setup, check, configure, and remove to complete without invoking either runtime.

## Onboarding Pilot

26. **README-only newcomer.** Give the final rendered landing page to a new user who has never encountered this project or any earlier README draft and did not participate in the change. Without coaching, evaluate the result within five minutes against the canonical [README newcomer Pilot checklist](../docs/TESTING.md#readme-pilot). Do not copy the criteria here or change that checklist after seeing the result.
