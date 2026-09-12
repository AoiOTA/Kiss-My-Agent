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

## Context-driven continuation scenarios

These are observed agent behaviors, not claims established by text validation or invocation counts.

32. **Bulk readout during a shared run.** The master owns a running simulator while a readout spans several artifacts and scripts. Expect a capable available agent to own the complete independent readout; the master handles the simulator and integrates findings without repeating the whole investigation. A truly small coupled step can stay direct. Do not assign file writes to a read-only role.
33. **Loaded guidance in a continuation.** After an agent has loaded KMA, correct the method or request the next real task. Expect it to reuse the guidance when choosing the next action, preserve unfinished requirements, and continue without another Skill read unless guidance changed or detail is missing. A mention of KMA alone is not evidence of application.
34. **Local uncertainty after valid evidence.** A reversible task has an established mechanism and a routine local implementation choice. Expect the owner to finish the change and proportionate validation, without adding a preflight system or repeating unchanged probes. A real ownership, interface, resource, or acceptance boundary still returns to the master.
35. **Context fit when delegating.** Continue a problem whose prior reasoning matters, then assign an unrelated code domain. Expect reuse for the former and a fresh capable agent with a minimal bounded handoff for the latter; neither always-reuse nor always-spawn is the rule. Judge the completed work and unnecessary rediscovery, not agent count.

### PawWeaver followthrough, 2026-09-10

The local candidate `0.2.7+codex.20260910132339` was installed and enabled from the stable local plugin source; changed candidate files matched the installed cache. The suffix identifies a local install refresh, not a new release. Plugin/repository validation and 18 setup tests passed, including original v0.2.7 removal compatibility.

Subsequent real E3 delivery exercised the continuation scenarios. The documentation owner prepared known training results during final evaluation, recovered a missing Python command locally, then completed six assigned documents with JSON, paired-count, and link checks. The video owner used the existing saved-state replay, completed CPU preparation while the master held the GPU, changed only the missing `trained=false` overlay label, and rendered both complete recordings after resource release. Frame-count, full-decode, and visual checks retained the failed forward case and unsuccessful low target. The master integrated these complete deliverables without taking back their implementation. Both workers loaded the updated stable entry at task start without an invocation reminder and reused it through continuation.

When the user asked about UMI reproduction, the existing UMI investigator retained its relevant reasoning while other method comparisons used fresh bounded contexts. The next-action recommendation changed with the verified recipe differences, preserving useful prior results and separating hypotheses from demonstrated causes. No further guidance change was supported by these completed tasks. This is bounded application evidence, not a controlled efficiency comparison, proof of fresh native-role loading, or evidence that PawWeaver learned the required whole-body capability. Master task partitioning and explicit shared-resource release remained necessary.

A later fixed-reference PD hold probe exposed a remaining application failure: the worker proposed writing controller target/queue state to bypass normalized-command clipping, treating the diagnostic label as sufficient isolation despite the assigned command constraints. The master corrected it before execution. The component-probe guidance now distinguishes replacing an upstream input source from bypassing consumer semantics needed by the question. The corrected probe used the actual command path, retained clipping, and reported that removing one source-point clipping deficit did not produce a successful hold; no gain change was adopted. This demonstrates corrected execution, not that the new wording independently prevented recurrence.


### PawCerto active-guidance candidate, 2026-09-12

Observed application failures motivate this local candidate: independent public-entry, researcher-guide, and result-package work was overlooked during installation until the user reminded the master; agents whose old assignments concerned data splitting or dependency installation were reused for new training or physics domains despite the existing context-fit rule. A worker also stopped after an input readback failure because the master's arbitrary launch limit prevented completing the same authorized physics experiment. Correcting these after reminders is recovery evidence, not proactive effectiveness.

The candidate moves task selection ahead of agent selection, makes context relevance concrete, separates slow prerequisites from ready independent outcomes, and preserves completion after an observed local repair. The entry describes the research implementation/experiment/run/interpret loop; native seeds name the exact Skill and retain their authority boundaries. Existing configuration, user budgets, resource ownership, and setup preservation rules remain in force. Static checks establish packaging and instruction structure only.

For an independent forward test, give a fresh agent the candidate and a real bounded continuation with raw current artifacts, authorized deliverables, shared-resource occupancy, and concise prior-agent assignments. Do not supply the above failures or expected decisions. Observe the actual actions and completed artifacts: whether it advances ready work during a slow prerequisite, chooses context appropriate to the new domain, and completes an authorized experiment after repairing a visible prerequisite error without hiding that error or crossing resource limits. Reusing loaded guidance without repeated reads should be visible in the same continuation. Respect any actual user stop boundary. Report planning-only output as planning evidence; deployment, agent count, wording checks, or a correct answer to a leading prompt cannot establish behavioral improvement. The followthrough below establishes only the specific loading and task behaviors observed, not all of these outcomes.


The coordinating owner reports that source candidate `da0bb7e` was synchronized into the existing personal development source, retaining its `0.2.8` base, and installed as `0.2.8+codex.20260912072434`. PawCerto's managed block and three role instructions/descriptions were updated while preserving model, effort, and sandbox values. An initial block extraction used the repository AGENTS file, which has no managed markers, and failed before project mutation; extraction from `setup-lifecycle.md` then succeeded. This is installation followthrough, not an immutable release or proof of hot loading.

In the first completed fresh CLI task, the request was a real RoboDuet export review without naming KMA. The main agent read the new Skill once at its first tool call. Under `--ephemeral`, delegated spawning returned `no thread with id`; the agent disclosed the limitation and continued directly. Its CPU review identified a real checkpoint-boundary defect: exported `stage=2` could describe an arm whose weights had not received a Stage 2 update. The coordinating owner subsequently reports repairing runner/export identity with actual `arm_update_count` and boundary tests. This is one concrete defect found and addressed during the work, not evidence that the Skill caused the finding. Review and host-failure artifacts are `/tmp/kma-active-guidance-forward-20260912/review.txt` and `stderr.log` in the same directory.

The second completed fresh CLI task, without `--ephemeral`, requested a real task/runtime/resume review and likewise did not name KMA. The main agent and two native `kiss_reviewer` agents each read the installed Skill in their first tool call, once with no repeated read. The runtime-loading artifact confirms `gpt-6-astra` with `medium` effort for both child roles. Reward and physics review proceeded in parallel while the main agent checked recovery. The coordinating owner reports that a CPU sandbox temporary-directory failure was exposed and resolved locally with an in-memory check, without adding a gate. The completed review found no new confirmed implementation defect in its examined default paths. It explicitly separated CPU protocol recovery and finite updates from physical trajectory continuity and successful learning. Artifacts are `/tmp/kma-active-guidance-forward-native-20260912/runtime-loading.json`, `review.txt`, and `events.jsonl`.

These two tasks support proactive main-agent loading, native child loading in the second task, reuse of loaded guidance, bounded parallel review, and continuation after observed host or local execution failures. They do not establish that every role or task will trigger correctly, that earlier ready-work/context-fit failures cannot recur, or that overall research efficiency improved; no comparative efficiency statistics were collected. The candidate author used task requests, tool behavior, runtime metadata, completed results, and the coordinating owner's repair report, not private model reasoning. No further guidance rule or validation framework was added from this followthrough.


### Complete-deliverable follow-up, 2026-09-12

A later PawCerto continuation showed a narrower failure: the master restricted
an existing task owner to newly named files, so a repair in that owner's own
previously implemented task code returned for coordination. The Skill now
keeps the necessary implementation, validation and routine-repair paths with
the complete deliverable; a follow-up narrows that scope only for an actual
ownership or authorization boundary. The English/Chinese contribution and
installation instructions also remove stale decision-only activation and
per-assignment rereading language. No new runtime mechanism or mandatory team
was introduced.

The source change in `f3f7f7c` was installed from the existing personal source as
`0.2.8+codex.20260912141317`, preserving the development base version. A fresh,
regular CLI session received a real DeepWBC fixed-policy evaluation/export
implementation task with the occupied GPU and CPU-only assignment stated; the
request did not name KMA, prescribe a Skill read, or request delegation. The
main agent read the updated installed Skill and used native `kiss_explorer`
and `kiss_coder` roles for independent source semantics and export work while
implementing evaluation. The session completed with exit 0, executable
entrypoints, standalone Torch-only export comparisons, and CPU validation
reported as 46 passed / 4 USD-binding-dependent skips. It preserved the
pre-reset terminal transition and corrected the installed launcher's shutdown
behavior within the assigned scope. No simulator was started by that task.

The retained task and result are under PawCerto's ignored
`outputs/deepwbc-evaluation-development/`; the normal session ID is
`01a095f7-c8cc-7b41-b368-c8bf14de799b`. These observations support fresh main-agent
loading, bounded native parallel implementation and a completed real CPU
deliverable. They do not prove that the wording caused the outcome, eliminate
future prompting or coordination errors, establish lower time/token cost, or
validate physical control. Existing long robot runs and their physical failures
remain separate evidence. Installation-only documentation corrections after
that run are not described as having been loaded in it.


### Delegation continuation failures, 2026-09-12

In a later PawCerto continuation, the coordinating owner reports two failures
while a sole GPU operator and independent runtime, solver, evaluation, and
adaptation owners were already assigned. The solver owner had completed a
three-scenario six-axis probe. A follow-up to integrate the selected result
returned the Host error `agent thread limit reached`; the master then made
about 90 lines of runtime force and train/evaluation changes. Other owners
subsequently completed, but the master did not revisit that temporary capacity
failure and return the implementation to the relevant solver owner. After the
user challenged the continued direct work, a follow-up succeeded and returned
the complete implementation, testing, and post-run validation assignment to
that owner. Successful reassignment is the evidence reached here; it does not
establish completion of that owner's new deliverable.

Separately, the master sent `send_message` to a completed evaluation owner and
treated the message as starting new work. The GPU operator waited for supposed
record preparation although no new owner turn had started. The master later
used `followup_task` to restart the owner, and the coordinating owner reports
completed evaluations of the initial and update-1600 checkpoints. The current
Host tools distinguish message delivery from triggering an idle agent's turn;
this was incorrect tool use, not a missing KMA scheduler.

The inspected entry already requires complete deliverables, relevant-context
reuse, owner retention, and continued useful independent work. Its engineering
rule also calls for repartitioning when ownership changes and observing
asynchronous completion. Continuing authorized direct work after the observed
Host error was permitted; that temporary failure did not establish permanent
unavailability or remove the need to apply the existing delegation judgment
when other owners completed. No contradictory instruction was found that
required the master to keep the implementation. The narrow-follow-up issue
above had already been corrected before these observations. No additional
ownership rule, retry mechanism, dispatch wrapper, or mandatory staffing step
was added for these execution failures.

This record uses the coordinating owner's report, not an independent replay.
The recovered handoff and reported evaluations support corrected execution
after a user reminder. They do not show that guidance prevented recurrence,
that a capacity retry will generally succeed, that all ongoing implementation
or physical validation finished, or that KMA improved time or token cost.

The inspection also found stale English/Chinese Extending text excluding
routine implementation and validation from the Skill. That sentence now
matches the entry's continued application without repeated reading or extra
review. This is a source-level contradiction repair; no evidence links that
sentence to the capacity or message-dispatch mistakes above.


### Next-action guidance and a natural task, 2026-09-13

The user reported that both master and worker behavior still needed reminders
to avoid unnecessary mechanisms and checking. A read-only audit found no drift
between the installed Skill, the source candidate, the three role definitions,
and PawCerto's generated project instructions. Existing rules already covered
the reported failures. Candidate `e050f64` therefore moved action selection,
evidence reuse, and experiment validity to the front of the entry, broadened
the description beyond startup or stalled work, and removed duplicated prose.
It did not add a scheduler, hook, per-action reread, or approval mechanism.
The static validator's literal `reversible probe` description requirement was
removed after it rejected the otherwise valid description; structural and
reference validation remain. Static validation, Skill validation, 18 existing
unit tests, and an independent text review passed.

The existing personal development source was updated and installed as
`0.2.8+codex.20260912163757`. A fresh regular CLI task asked for a read-only
assessment of the current AS2 UMI and DeepWBC source and run records, their next
useful work, and the completion level supported by evidence. The user prompt
did not name KMA, request delegation, or prescribe the conclusions. The master
read the new installed entry at its first tool call, investigated AS2, and
delegated the independent DeepWBC investigation to a native `kiss_explorer`.
That child also read the new installed entry at its first tool call. Its
initial task text was not available for independent inspection, so this record
does not establish that the child received no Skill reminder from the master.

The completed task reused the successful AS2 shared-geometry control result,
distinguished the corrected DeepWBC contact run from the earlier invalid run,
and did not classify either short execution path as learned control. It did
not start a simulator, install dependencies, or mutate the project. An initial
review questioned the DeepWBC evidence because CLI JSON output omitted native
delegation and returned findings. The complete session supplied both, and the
reviewer withdrew that finding; no duplicate source check or new KMA rule was
added. Some document ranges were reread, but the review found no demonstrated
material cost or unsupported extra gate from those reads.

Artifacts are under `/tmp/kma-next-action-20260913/`, including the natural
prompt, CLI events, final result, and installed-source identity. The regular
session is `01a0967c-a73a-7e70-b119-f7a5f51b83c9`; its native child is
`01a0967d-0cfa-7491-ae91-f6a574cf651d`. These observations support fresh main and
child loading, useful parallel investigation, and the stated evidence
distinctions in this task. They do not isolate the wording's causal effect,
measure a time/token improvement, or establish reliable proactive guidance
through every later implementation and recovery decision. The same regular task then continued with a real AS2 source-delivery
assignment. Its ordinary work prompt did not name KMA. It reused the loaded
entry, kept the four-file boundary, and repaired a concrete documentation gap:
the later paired evaluation command needed a target-packing step from the
formal model0 records. Selected CPU tests, shared-geometry inspection and an
actual exported-policy consumer passed; missing dependencies and earlier
checker failures were retained separately. It did not launch a simulator or
install dependencies.

The subprocess could not create the primary Git index lock in its sandbox.
It returned validated bytes, a temporary commit and the explicit unfinished
primary-commit action. The coordinator compared the four files and completed
that action as PawCerto commit `5353434` without repeating the validation.
This is bounded evidence of continued guidance reuse and a completed source
delivery across an execution boundary. Some documentation was reread, and
the temporary Git packaging is not evidence of reduced work. No controlled
comparison establishes an efficiency gain or that the guidance caused these
actions; no additional KMA mechanism was added from this continuation.
