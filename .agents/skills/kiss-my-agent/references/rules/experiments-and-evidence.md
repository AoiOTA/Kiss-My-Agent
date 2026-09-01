# KISS experiments and evidence

Use this rule when a claim depends on what was actually executed, measured, or evaluated. The permanent evidence boundaries and labels remain authoritative; this file supplies decision methods rather than restating them.

## Design before interpretation

State the research question, primary variable, controlled variables, core metric, and invalid conditions before interpreting results. Add samples only when variance or intermittent behavior affects the decision, and do not move criteria after seeing the outcome.

Classify outcomes by failed precondition, not desirability. Valid negative means the planned inputs, execution, observations, and evaluator were intact but the product outcome was adverse or neutral. Invalid means a required precondition or measurement path failed, so the product hypothesis was not tested. Preserve both records without converting one into the other.

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
