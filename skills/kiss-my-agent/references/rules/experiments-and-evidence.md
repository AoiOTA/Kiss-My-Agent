# KISS experiments and evidence

Use this rule when a claim depends on what was actually executed, measured, or evaluated. The permanent evidence boundaries and labels remain authoritative; this file supplies decision methods rather than restating them.

## Design before interpretation

State the research question, core metric, and invalid conditions before interpreting results. For causal attribution, identify the primary variable and relevant controls. For task performance, a coherent recipe may change coupled settings together when supported by existing evidence and within the assigned architecture and budget; evaluate the recipe without attributing its effect to one setting. Choose training duration to test the question at a justified scale; add samples when variance or intermittent behavior affects the decision, and do not move criteria after seeing the outcome.

Preserve a diagnostic comparison’s original criterion and failed result; a self-imposed criterion does not automatically become a prerequisite for later experiments. Judge its relevance to the next experiment’s claim while preserving the user’s acceptance criteria; require exact trace equality only when that claim depends on it.

Choose a probe only when its result can change the next action toward the user's requested outcome. If the uncertainty is whether learning improves task behavior, finite execution or parameter updates do not answer it; run enough of the actual learning-and-evaluation path to test that question. Use the minimum valid run for the question. Fixed-input probes still exercise the actual consumer path when its limits, delays, or state transitions affect the hypothesis: supply fixed commands through that path and report any clipping, rather than writing internal state to bypass it. An unconstrained component test answers a different question and cannot replace that comparison. Preserve actual outputs and failure causes, and use the result to iterate or stop.

When a behavior question does not require public distribution, use a mutable disposable candidate before creating an immutable release tag, and create the tag only after those pre-tag questions pass. After tagging, run only the shortest checks that genuinely depend on the public distribution or tag; reserve a patch release in this flow for a product defect first exposed by those public-only checks, while harness or environment failures are repaired in their owning path and the same tag is retested; do not use a tag as a disposable test fixture. This sequencing preserves rather than replaces real public-path validation.

Classify outcomes by failed precondition, not desirability. Valid negative means the planned inputs, execution, observations, and evaluator were intact but the product outcome was adverse or neutral. Invalid means a required precondition or measurement path failed, so the product hypothesis was not tested. Preserve both records without converting one into the other.

## Match the experiment to the decision

Use the user's metric priorities rather than treating fewer calls, actions, or elapsed seconds as the default objective. Report the complete task outcome before interpreting component hypotheses when completion is the user's primary goal. Success with more cost establishes that success and its tradeoff; a cheaper failure does not establish improved complete-task efficiency. Keep task success, action success, process exit, mechanism contribution, and paper novelty separate. Causal caution should lead to a bounded claim and a useful next decision, not erase a supported positive result.

Functional smoke tests whether an entry works; mechanism validation tests availability or behavioral effect; task comparison measures complete outcomes and costs; paper evaluation tests the stated general claim with appropriate coverage and uncertainty. Choose the smallest experiment sufficient for the current question, rather than the fewest runs. Check decisive prerequisites early using a short real execution: whether the evaluator accepts the native completion action, the changed scene actually contradicts the tested use, and the mechanism can reach the deciding consumer. These are question-dependent checks, not mandatory launch gates. Once a blocking local issue is resolved, return to the complete authorized task.

Before another mechanism run, identify a legal decision opportunity and the observable difference that could distinguish the explanations. If the mechanism was not triggered, choose the next action from the cause:

- Unreachable input or action: repair the actual consumer or adapter path.
- No relevant decision opportunity: select a scenario containing that opportunity within the authorized scope.
- Available but autonomously unused: retain the non-use result and examine competing explanations or the original task outcome; do not force selection to manufacture evidence.

One untriggered success remains task evidence but does not establish mechanism benefit. More repetitions need a new discriminating basis or an explicit variability question. Include setup, prior screens, model input, repeated analysis, failures, and unfinished outcomes in the relevant cost denominator; a sequence of cheap probes may cost more than one sufficient task run.

After a material repair, decide whether it merely restores expected engineering function or tests a hypothesis distinct from existing alternatives. Prefer the next action that distinguishes those explanations when the user's question requires attribution. Valid negative evidence supports narrowing or stopping. When an adapter or evaluator defect breaks required comparison conditions, stop affected work and preserve the invalid result, cause, and cost. Repair and freeze a separate valid comparison rather than finishing the invalid run for the sake of a frozen version. Do not silently pool invalid runs with valid ones or discard their incurred cost.

## Discriminating the active evidence

Stale-artifact discrimination starts at the first place source and execution can diverge: inspect the loaded module or executable identity, affected output identity, configuration binding, and a behavior or symbol changed by the candidate. Timestamps and file existence are hints, not proof. Rebuild only the affected closure and repeat the shortest probe that distinguishes old from current behavior.

To resolve runtime ambiguity, hold the evaluator fixed while comparing runtime outputs, then replay the same captured output through evaluator variants. A documentation edit cannot change either measurement. If the comparison cannot hold the relevant side fixed, report the ambiguity instead of assigning cause.

Record version identity when freezing evidence for reproduction, delivery, compatibility, or attribution. Capture the smallest sufficient source, dependency, configuration, data, and evaluator identities at the point they become fixed; avoid unrelated repository snapshots.

## Reuse, replay, and collection

Reuse existing evidence when its question, implementation, configuration, data, evaluator, and validity conditions still match. Replay when preserved inputs contain every signal needed for a deterministic evaluator or interpretation question. Recollect when runtime interaction, missing signals, changed behavior, timing, or causal attribution is material.

For a shared experiment or publication target, assign one writer/operator and, when needed, a separate finalizer who verifies completeness before publishing the outcome. Others may inspect immutable inputs or prepare isolated work. Retries require a plausible transient cause or a new discriminating hypothesis, remain bounded and observable, and preserve the decisive failure. Stop repeating when information gain is exhausted.

## Where evidence belongs

Keep implementation, interfaces, necessary configuration, small deterministic fixtures, and concise reproduction instructions in Git. Keep only current handoff facts in state documentation. Put large datasets, generated outputs, complete logs, models, media, and experimental results in the designated artifact store. Store an index only when a later consumer must locate them.

Use the evidence labels defined in `AGENTS.md`; name the lowest level actually reached, map each claim to its supporting observation, and state the missing evidence without inventing a new promotion gate.
