# Manual scenarios

These scenarios support human discussion of the permanent rules and `$kiss-my-agent` routing. They are not scores, automated evaluations, release gates, or claims that an agent will behave identically in every environment. Invoke the skill only for the non-obvious mechanism or evidence decisions below, not for routine execution.

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
