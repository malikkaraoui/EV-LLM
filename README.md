# 🧠🐜 EV-LLM

**A public research log on a "post-transformer" cognitive architecture: a system that learns a *procedure* from a handful of examples, transfers it, and assembles it with others.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Type](https://img.shields.io/badge/type-research%20log-8A2BE2)
![Experiments](https://img.shields.io/badge/experiments%20%26%20amendments-21-informational)
![Compute](https://img.shields.io/badge/compute-1%C3%97%20Mac%20M1%2016%20GB-lightgrey)

Not a product, not a model to download: a lab notebook, **failures published on the same footing as successes**. Each failure spares someone else a cycle.

> **Status — 28/09/2026.** 21 experiments or amendments, run from 25 to 27/09. Four have been reviewed and merged into `main`; the others live on their own branch (linked below).

---

## TL;DR

| | What we found | Evidence |
|---|---|---|
| ✅ | **Computing is easy with almost nothing.** Once the digits are aligned, a tiny network (1,196 parameters, two state numbers) or an evolved circuit with a single carry unit is exact up to 1,000 digits. | E011 · E012 · E013 |
| 🧱 | **The wall is locating, aligning, wiring.** Whenever the system must find on its own which digit to read, no seed reaches 90 % at 16 digits, from ~1,900 to ~3.2 M parameters — except 1 seed out of 5 with a curriculum (E014 R0b). | E008 · E009-bis · E010 · E013 I2 · E014 R0 |
| 🔌 | **What got over the wall: a symbolic interface between frozen skills.** They compose without retraining — but the interface or the wiring was still given by us. | E014 · E015 ECH0 · E016 DONNÉ |
| 🙈 | **Misplaced confidence is blind.** Errors are often "confident" when confidence bears on the wrong step. | E005 · E006 · E008 · E010 · E014 · E015 |
| ❓ | **Open:** an intermediate signal the machine gives itself. *[HYPOTHESIS] — not tested.* | — |

---

## Contents

1. [Results at a glance](#results-at-a-glance)
2. [Method](#method)
3. [Experiment log (details)](#experiment-log)
4. [What we believe we know today](#what-we-believe-we-know-today)
5. [Dead ends, and why they are useful](#dead-ends-and-why-they-are-useful)
6. [Open leads](#open-leads)
7. [Reproduce](#reproduce)
8. [Repository layout](#repository-layout)
9. [How the project is run](#how-the-project-is-run)
10. [License and citation](#license-and-citation)

---

## Results at a glance

Legend — verdict: ✅ success · ◐ partial / mixed · ❌ negative · ⏹ stopped. Review: **GO** = reviewed and merged into `main` · **Reservation** = reviewed, not merged · **—** = not yet reviewed (**—\*** = figures cross-checked by the orchestrator, which is not an independent review).

| # | Experiment | Key result | Verdict | Review |
|---|---|---|---|---|
| | **Part 1 — Does Jev know when it is wrong?** | | | |
| 1 | [E001](research/experiments/E001-jev-sonde/) · first probe of Jev | 0 "wrong and confident" out of 13 calls on common mistakes and their controls | ◐ probe OK, question open | GO |
| 2 | [E003](https://github.com/malikkaraoui/EV-LLM/tree/exp/e003-etalon-llm/research/experiments/E003-etalon-llm) · LLM baseline | Compliance: Jev 10/10, `gpt-4.1-mini` 9/10, `gemini-2.5-flash` 10/10 | ◐ backend not controlled | Reservation |
| 3 | [E005](research/experiments/E005-jev-hors-distribution/) · Jev out of distribution | 9 "wrong and confident" evaluations out of 42, over 6 questions | ❌ calibration | GO |
| 4 | [E006](https://github.com/malikkaraoui/EV-LLM/tree/exp/e006-replication-frontiere/research/experiments/E006-replication-frontiere) · replication and boundary | 5 uncontested "wrong and confident", reproduced 5/5; a single distractor is enough | ✅ replicated | Reservation |
| 5 | [E007](https://github.com/malikkaraoui/EV-LLM/tree/exp/e007-regles/research/experiments/E007-regles) · does Jev read written rules? | A written rule corrects 3/3 pairs; an absent rule changes almost nothing | ◐ partially | — |
| | **Part 2 — Acquiring hidden rules** | | | |
| 6 | [E002](research/experiments/E002-relations-opaques/) · opaque-relations bench | Even the baseline that *knows*: mean R −0.003, positive in 8/20 worlds | ❌ measure | GO |
| 7 | [E002-bis](research/experiments/E002bis-mesure/) · repaired measure | R > 0 in 20/20 worlds | ✅ | GO |
| 8 | [A0](https://github.com/malikkaraoui/EV-LLM/tree/exp/a0-candidat/research/candidats/A0) · first "acquire" candidate | Speed-up in 1/4 families (3 required); trigger never verified (0 queries) | ❌ | Reservation |
| 9 | [A0-bis](https://github.com/malikkaraoui/EV-LLM/tree/exp/a0bis-candidat/research/candidats/A0bis) · corrected candidate | 0/4 families | ❌ | Reservation |
| 10 | [A0-ter](https://github.com/malikkaraoui/EV-LLM/tree/exp/a0ter-candidat/research/candidats/A0ter) · oracle | Even a perfect acquirer: 2/4 families | ◐ criterion did not measure acquisition | — |
| | **Part 3 — Learning a procedure: addition** | | | |
| 11 | [E008](https://github.com/malikkaraoui/EV-LLM/tree/exp/e008-addition/research/experiments/E008-addition) · transformer baseline | ~3.2 M params: 98–100 % in distribution, 0.0 % from 6 digits | ✅ baseline set | Reservation |
| 12 | [E009](https://github.com/malikkaraoui/EV-LLM/tree/exp/e009-procedure-apprise/research/experiments/E009-procedure-apprise) · architecture alone | ≤ 3 % even in distribution | ◐ not measured (budget too short) | — |
| 13 | [E009-bis](https://github.com/malikkaraoui/EV-LLM/tree/exp/e009bis-procedure-apprise/research/experiments/E009bis-procedure-apprise) · same, sufficient budget | 1/5 runs learns; 0 % beyond 6 digits | ❌ | — |
| 14 | [E010](https://github.com/malikkaraoui/EV-LLM/tree/exp/e010-enseignement/research/experiments/E010-enseignement) · column scratchpad | 99.9 % with 10,000 examples (≥ 25× fewer); 0 % from 7 digits | ◐ efficiency ✅ length ❌ | — |
| 15 | [E011](https://github.com/malikkaraoui/EV-LLM/tree/exp/e011-objectif-mdl/research/experiments/E011-objectif-mdl) · does the objective break the rule? | Cross-entropy keeps the rule 5/5; L2 λ = 1: 0/5 | ✅ | — |
| 16 | [E012](https://github.com/malikkaraoui/EV-LLM/tree/exp/e012-evolution/research/experiments/E012-evolution) · evolution guided by MDL | Aligned decimal 4/5 with 1,000 examples, exact up to 1,000 digits; binary 0/5 | ✅ alignment given | — |
| 17 | [E013](https://github.com/malikkaraoui/EV-LLM/tree/exp/e013-insecte/research/experiments/E013-insecte) · "the insect" 🐜 | Single-number state (1,131 params): 99.3 % at 1,000 digits; two state numbers: 100 % at 1,000 digits, 5/5 seeds | ✅ alignment given | Reservation |
| 18 | [E014](https://github.com/malikkaraoui/EV-LLM/tree/exp/e014-reperage/research/experiments/E014-reperage) · learning where to read | Frozen reader + frozen accumulator: exact at 16 and 100 digits, 4/5 seeds; end to end 0/5 | ✅ composition | —\* |
| | **Part 4 — Without an interface written by us** | | | |
| 19 | [E015](https://github.com/malikkaraoui/EV-LLM/tree/exp/e015-ecosysteme/research/experiments/E015-ecosysteme) · ecosystem | Free assembly 0/5; wiring given, interface invented: 2/5 | ❌ | —\* |
| 20 | [E016](https://github.com/malikkaraoui/EV-LLM/tree/exp/e016-mouches/research/experiments/E016-mouches) · "flies", common language | No common language; collective rule 0/5 seeds | ❌ | —\* |
| 21 | [E016-A2](https://github.com/malikkaraoui/EV-LLM/tree/exp/e016-a2/research/experiments/E016-mouches) · denser signal | 1 pair out of 9 in both guard pilots | ⏹ stopped at guard pilot | —\* |

---

## Method

This is the part that matters most; the results follow from it.

1. **Prior art first.** Before each experiment, we look for what is published: sources read, verdict written into the mandate ("done", "partially done", "not found"). A 10–20 min scan at first; since the evening of 27/09, an in-depth search by dedicated agents before any launch.
2. **Never redo published work to reach the same result.** If it exists, we look for the variant or the opposite tack. A known building block (MAP-Elites, MDL, REINFORCE…) is only a tool; the question tested must be new.
3. **Preregistration before code.** Hypotheses, numerical predictions and success thresholds are committed and pushed on their own, before the first line of code. A deviation found afterwards is a result: reported, not quietly corrected. Any change goes through a dated amendment.
4. **Measurement safeguards** (tightened on 27/09 after a hostile review):
   - pilot on seed 0, excluded from the results; at least 5 seeds (2 to 3 for the first experiments, stated each time);
   - out-of-distribution validation (6–8 digits) kept separate from the final test (10–1,000 digits), read **only once**;
   - validity controls: an oracle must score 100 %, a "memorising" system 0 %;
   - adversarial tests: cascading carries, numbers full of zeros, asymmetric lengths;
   - **structure budget**: what is given by hand (alignment, reading direction, number of steps…) is written down, separately from what is actually learned.
5. **Independent review ("doublage") before any merge.** Another agent replays, recomputes and rereads. Verdicts: GO, RESERVATION or BROKEN. Only GO merges; "mergeable with reservation" does not merge.
6. **Fast iteration, small compute.** One Mac M1 16 GB (Python, numpy, MLX). 3 minutes to 4 hours per experiment. Models from 22 parameters (a hand-built recurrent network) to ~3.2 million (a small transformer). Each experiment README gives its compute time.

Labels: **[VERIFIED]** = checked against a source in the repository · **[HYPOTHESIS]** = interpretation not established. No general conclusion is drawn: samples range from 7 cases to a few hundred thousand items, on a single task at a time.

**Starting point.** The hypothesis is in [`architecture_cognitive_post_transformer.md`](architecture_cognitive_post_transformer.md) (in French). In short: intelligence would be less the amount of training undergone than the ability to do a lot with almost nothing; knowing a rule is not having acquired it; what is missing is the loop that turns an explicit rule into a reliable reflex, and a reflex into a rule. It is an exploration, not an adopted architecture. The path taken day by day, mistakes included, is in [`GENESE.md`](GENESE.md) (up to 26/09), continued in [`vault/notes/2026-09-27-genese-suite.md`](vault/notes/2026-09-27-genese-suite.md).

---

## Experiment log

Each entry: question, prior art, what we changed, numerical result, verdict, takeaway, review status. Figures are copied from the experiment's README, at the tip of its branch. Click a part to expand it.

<details>
<summary><b>Part 1 — An external trigger: does Jev know when it is wrong? (25–26/09)</b> · E001, E003, E005, E006, E007</summary>

<br>

The idea: to know *when* to verify, one needs honest confidence, especially on "invisible" errors (wrong but fluent). Jev (TypeSafe AI) presents itself as a model that returns typed decisions with a calibrated probability. We probed it through its API.

#### 1. First probe of Jev (E001) — [folder](research/experiments/E001-jev-sonde/) · reviewed GO (R001), merged
- **Question:** on 7 preregistered cases (logic with a given rule, fluent French spelling mistakes), is Jev "wrong and confident"?
- **Prior art:** the vendor's announcement (15/09/2026); its figures are not independently verified.
- **Result:** 1st launch, 21 calls out of 21 refused (HTTP 403, credit card required). Then logic: 6 questions compliant out of 6; contradiction and indeterminacy distinguished 3 times out of 3. Common mistakes ("il a manger", "ils sont tombé"): 4/4 compliant, 13 calls out of 13, 0 "wrong and confident".
- **Verdict:** successful as a probe, but the question is not settled: these common mistakes fooled no one.
- **Takeaway:** a service announced as "free" may require a card; test real access with a dry-run call before launching.

#### 2. LLM baseline on the same cases (E003) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e003-etalon-llm/research/experiments/E003-etalon-llm) · reviewed with reservation (R005), fixes not yet reviewed
- **Question:** do two generative LLMs (`gpt-4.1-mini`, `gemini-2.5-flash`) do better or worse than Jev?
- **Result:** compliance Jev 10/10, `gpt-4.1-mini` 9/10, `gemini-2.5-flash` 10/10. The only "wrong and confident": `gpt-4.1-mini` denies E > D 3 times out of 3, with a verbalised confidence of 0.9 to 1.
- **Verdict:** measured, but backend not controlled: the gateway provider was neither enforced nor logged. The planned replay was cancelled when the Jev tests were stopped.
- **Takeaway:** a verbalised confidence is not a probability ([HYPOTHESIS]); enforce and log the provider of any baseline model.

#### 3. Jev out of distribution (E005) — [folder](research/experiments/E005-jev-hors-distribution/) · reviewed BROKEN (R004, wrong HTTP total), fixed, then reviewed GO (R007), merged
- **Question:** on rare rules (learned agreement rules, homophones, logic with distractors or 4 steps), is Jev confidently wrong?
- **Changed:** 32 cases as minimal pairs, preregistered and pushed before the first call.
- **Result:** 151 calls, 34 usable responses. **9 "wrong and confident" evaluations out of 42, covering 6 questions.** The 13 evaluations of correct sentences are all conforming (13/13); on the incorrect sentences, 7 evaluations out of 13 judge an erroneous sentence correct. Above a probability of 0.8, Jev is compliant 19 times out of 28.
- **Verdict:** negative for calibration on this corpus.
- **Takeaway:** [HYPOTHESIS] Jev would judge surface plausibility rather than the rule.

#### 4. Replication and boundary (E006) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e006-replication-frontiere/research/experiments/E006-replication-frontiere) · reviewed with reservation (R008), fix not yet reviewed
- **Question:** do the "wrong and confident" cases of E005 reproduce? Where is the boundary?
- **Result:** 103 calls, all served. **5 uncontested "wrong and confident", reproduced 5 times out of 5**, plus 1 response reclassified as "contested" (ambiguous question, R008). Logical chain of 2 to 6 steps: P between 0.85 and 0.97, no slope. Distractors: P(contradiction) 0.73 → 0.34 → 0.14 → 0.08 for 0 to 3 distractors. Contamination by an unrelated contradiction: mean difference −0.005, not observed.
- **Verdict:** replication successful; chain length is not the boundary, a single distractor is enough.
- **Takeaway:** "can X be deduced" is ambiguous when a rule forbids X; specify the meaning of "deduce" in corpora.

#### 5. Does Jev read written rules? (E007) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e007-regles/research/experiments/E007-regles) · not yet reviewed
- **Result:** writing the agreement rule into the prompt corrects all 3 pairs (erroneous form from 0.84–0.86 to 0.05–0.09). Inverting a rule is followed (0.77 → 0.34; 0.95 → 0.28). Removing it changes almost nothing (0.70; 0.90): Jev fills in with the usual meaning of the symbols.
- **Verdict:** "partially", in the sense of the preregistered criterion.
- **Takeaway:** [HYPOTHESIS] Jev starts from a prior; a written rule that contradicts it moves it, an absent rule does not stop it.

**End of this part (26/09, 18:17).** Malik's decision: stop the Jev tests and work on small models we train ourselves.

</details>

<details>
<summary><b>Part 2 — Acquiring hidden rules: the opaque-relations chamber (26/09)</b> · E002, E002-bis, A0, A0-bis, A0-ter</summary>

<br>

#### 6. The bench and three baselines (E002) — [folder](research/experiments/E002-relations-opaques/) · reviewed GO (R002), merged
- **Question:** does a bench where the properties of relations are hidden, noisy (5 to 10 %) and trapped separate "knowing", "naive acquisition" and chance? Gain measured in bits saved (R).
- **Prior art:** not documented in the README.
- **Result:** even the baseline that **knows** the properties has a mean R of −0.003, positive in only 8 worlds out of 20. The ratio to this ceiling is therefore undefined in 12 worlds out of 20. Without noise, its R is +0.016, positive everywhere.
- **Verdict:** negative on the measure, deviation reported and not corrected.
- **Takeaway:** deducing correctly from a false observation propagates the error.

#### 7. Repairing the measure (E002-bis) — [folder](research/experiments/E002bis-mesure/) · reviewed GO (R003), merged
- **Changed:** a ceiling that checks its premises with the world before concluding; measure as a difference (R − R_ceiling).
- **Result:** R > 0 in **20 worlds out of 20** (mean +0.0122, minimum +0.0067), at the cost of 28 to 45 queries per world.
- **Verdict:** successful (measure repaired, for this bench and these parameters).

#### 8. First "acquire" candidate (A0) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/a0-candidat/research/candidats/A0) · reviewed with reservation (R009)
- **Question:** do a memory across worlds, a calibrated trigger and a self-diagnosis make world n+1 solved faster than world n?
- **Result:** speed-up in 1 family out of 4 (3 were required). Best system without given properties (gap to ceiling −0.0110), but its trigger **never** verified: 0 queries over 20 worlds, verification cost badly specified.
- **Verdict:** negative, cause identified.

#### 9. Corrected candidate (A0-bis) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/a0bis-candidat/research/candidats/A0bis) · reviewed with reservation (R009: reading depends on a single seed)
- **Result:** marginal cost, verifications become active (22.6 queries per world), but 0 families out of 4. The "no estimated noise" ablation does better than the full system (−0.0076 versus −0.0105), but this gap comes from a single world (seed 19); without it, the full system does better (−0.0074 versus −0.0078) (R009).
- **Verdict:** negative.

#### 10. Was the criterion reachable? (A0-ter, oracle) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/a0ter-candidat/research/candidats/A0ter) · not yet reviewed
- **Changed:** a "perfect acquirer", which receives the exact knowledge of each family after its first world.
- **Result:** **2 families out of 4**. Even perfect acquisition fails the criterion. The threshold mostly measured how badly the first world went.
- **Verdict:** the criterion did not measure acquisition. The failures of A0 and A0-bis therefore say nothing about those candidates.
- **Takeaway, applied to every experiment since:** prove that a test can be passed by an oracle before judging a candidate on it.

</details>

<details>
<summary><b>Part 3 — Learning a procedure: addition (26–27/09)</b> · E008 → E014</summary>

<br>

The target is redefined: learn addition on numbers of 1 to 5 digits, then succeed on much longer numbers. Every experiment in this part starts from E008 and reuses its evaluator.

#### 11. Is the test sound, and where does a transformer break? (E008) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e008-addition/research/experiments/E008-addition) · reviewed with reservation (R010–R012, reservation concerning E013, reviewed together), not merged
- **Prior art:** the literature predicts collapse beyond seen lengths; "NoPE + reversed output" is a known fix.
- **Result:** valid test (oracle 100 %, memorisation 0 %). Transformer of ~3.2 M parameters, 3 M examples: 98–100 % in distribution, **0.0 % from 6 digits on** (3 seeds). With the fix: 91.2 % at 6 digits, 7.9 % at 7, 0.1 % at 8. 65 to 68 % of its errors at 6–7 digits have a confidence ≥ 0.8. Compute: 2 h 11.
- **Verdict:** baseline established. The known fix pushes the boundary out by one digit.

#### 12. Architecture alone (E009) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e009-procedure-apprise/research/experiments/E009-procedure-apprise) · not yet reviewed
- **Prior art:** Neural GPU, Deep Thinking, Looped Transformer (scan of 27/09, note [`vault/notes/2026-09-27-veille-procedure.md`](vault/notes/2026-09-27-veille-procedure.md)).
- **Result:** 5 architectures of 50 to 110 k parameters, 512,000 examples: ≤ 3 % even in distribution.
- **Verdict:** not measured. Budget too short, and a GPU shared by four windows (an orchestration error, acknowledged).
- **Takeaway:** a pilot must check that the model learns the distribution, not only the compute speed.

#### 13. Architecture alone, with a sufficient budget (E009-bis) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e009bis-procedure-apprise/research/experiments/E009bis-procedure-apprise) · not yet reviewed
- **Result:** curriculum, width 128, up to 10,000 steps: **1 run out of 5** learns the distribution (96.8 %), then 17.3 % at 6 digits and 0 % beyond.
- **Verdict:** negative at this budget. Compute: ≈ 3 h 52.

#### 14. Teaching as at school: the column scratchpad (E010) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e010-enseignement/research/experiments/E010-enseignement) · not yet reviewed
- **Changed:** the model writes each column (digits, incoming carry, written digit, outgoing carry) before the sum.
- **Result:** **10,000 examples** are enough for 99.9 % in distribution; without a scratchpad, never 95 % with up to 256,000, i.e. at least 25 times fewer examples. Stating the rule in one sentence brings nothing. Out of distribution: 33.1 % at 6 digits, **0 % from 7 on**.
- **Verdict:** successful for efficiency, negative for length.
- **Takeaway:** the carry is computed correctly, the failure comes from **locating** (which digit to read, when to stop). And a confidence taken on the final copy is blind: 606 errors out of 669 are "confident".

#### 15. Does the training objective break the rule? (E011) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e011-objectif-mdl/research/experiments/E011-objectif-mdl) · not yet reviewed
- **Prior art:** Lan et al. (TACL 2022) obtain exact binary addition with an MDL objective; arXiv 2505.13398 reports that regularisation drifts away from the perfect solution (on other tasks). Two figures relayed by the scan were wrong; the experiment corrected them.
- **Changed:** we start from a 22-parameter network, exact by construction, and train it.
- **Result:** cross-entropy alone, rule kept **5/5** up to 1,000 bits. L2 penalty λ = 1: 0/5; L1 λ = 1: 2/5. Discrete MDL: 5/5, and the network compresses (206 → 204 bits). Our differentiable approximation of MDL: 4/5. Compute: ~4 min on CPU.
- **Verdict:** successful (question settled for this network and this task).
- **Takeaway:** the objective is not the hidden ceiling; strong weight penalties are.

#### 16. Does evolution discover the circuit? (E012) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e012-evolution/research/experiments/E012-evolution) · not yet reviewed
- **Changed:** evolutionary search guided by MDL, with less than 0.6 % of the budget of Lan et al.
- **Result:** binary 0/5; aligned decimal 2/5 with 100 examples, **4/5 with 1,000**, exact up to 1,000 digits; flat input 0/5. The shortest circuit found is the school algorithm, with a single unit that is the carry: `h(t) = step(a + b + h(t−1) − 9)`, `output = a + b + h(t−1) − 10·h(t)`. It is proven exact for any length. Compute: ~204 min.
- **Verdict:** successful when the alignment is given.
- **Takeaway:** in the failures, the exact circuit has a much lower MDL than the one returned. It is the **search** that fails, not the objective.

#### 17. A tiny accumulator, "the insect" 🐜 (E013) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e013-insecte/research/experiments/E013-insecte) · reviewed with reservation (R010, R011, R012), not merged
- **Prior art:** path integration in the bee (Stone et al. 2017), a small state updated at each step. The analogy is ours, not the authors'.
- **Structure budget:** digit alignment, direction (least significant first) and number of steps are given.
- **Result:** **1,131 parameters**, a single-number state: 100 % from 16 to 100 digits (5/5 seeds), 99.3 % at 1,000. With two state numbers: **100 % at 1,000 digits**, 5/5 seeds, on all adversarial sets. With 1,000 examples, long numbers pass (98.6 % at 1,000 digits) but pure carry propagation drops to 52.9 % on average (± 40.5) at 1,000 digits, with 1 seed out of 5 above 90 %; with 10,000, 100 % everywhere. Without given alignment: 0/5. Compute: 65 min.
- **Verdict:** successful, alignment given. The project's first length success.
- **Takeaway:** with a single state number, the network is wrong "with confidence" on sparse numbers (28 % of its errors): nothing in the short data forces "no carry" to remain stable.
- **Reservation:** the README's synthesis was contested three times in a row (example threshold restated without a source). It must be redesigned before merging.

#### 18. Learning WHERE to read, then composing (E014) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e014-reperage/research/experiments/E014-reperage) · not yet reviewed (cross-checked by the orchestrator)
- **Prior art:** not documented in the README. The orchestrator notes after the fact that a discrete interface shared between modules is known (stitching, shared symbols).
- **Changed:** a reader trained alone to "set out in columns", with no addition at all in its loss, then plugged in **frozen** in front of the **frozen** accumulator of E013, with no joint training.
- **Result:** exact addition at 16 and 100 digits on **4 seeds out of 5**; 1/5 at 1,000 digits. Trained end to end, the same reader fails: 0/5, 1/5 with curriculum, 0/5 with hard pointers. By abstaining below a confidence threshold, it rejects 77 % of its errors for 1.4 % of its correct answers.
- **Verdict:** successful for composition without retraining.
- **Takeaway:** composition loses nothing as long as the reading is correct; at 1,000 digits, it is the reading that breaks. But **someone defined the intermediate task** and the interface between the two modules.

</details>

<details>
<summary><b>Part 4 — Without an interface written by us (27/09, evening)</b> · E015, E016, E016-A2</summary>

<br>

Malik's instruction at 20:35: stop redoing known work, take the opposite tack.

#### 19. Ecosystem: do skills assemble on their own? (E015) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e015-ecosysteme/research/experiments/E015-ecosysteme) · not yet reviewed (cross-checked by the orchestrator)
- **Prior art (15 min scan):** PathNet, modular meta-learning, NPI, model stitching. None requires at once discovering which frozen modules to chain, the order of operations **and** the symbol-to-symbol interface, with a final judge as the only signal.
- **Result:** free assembly **0/5** on three new tasks. Wiring given, interface to be invented: **2/5**, exact up to 1,000 digits, with an interface we would not have written. With a single instruction missing from the wiring: 0/5. Reusing a winning interface on another task: no gain. Compute: ≈ 1 h.
- **Verdict:** negative.
- **Takeaway:** the known solution scores 1.100 with the judge, the returned programs between 0.004 and 0.45. Again it is the search that fails: a needle-in-a-haystack landscape, where no partial wiring scores better than "copy a". Some wrong interfaces divert a subtraction circuit into an adder without carry.

#### 20. "Flies": a common language through social pressure? (E016) — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e016-mouches/research/experiments/E016-mouches) · not yet reviewed (cross-checked by the orchestrator)
- **Malik's idea:** 3 "reader" agents and 3 frozen "adder" agents, with incompatible private codes, a free channel and a common goal. All-or-nothing collective reward; if one agent is wrong, everyone starts over.
- **Prior art:** already partly done. Heterogeneous frozen networks build a common protocol (Mahaut et al., arXiv 2302.08913). New part aimed at: procedural skills, a computation split in two by the channel, judging up to 1,000 digits.
- **Result:** no common language (0 symbols shared by the three senders, 25 runs out of 25). Collective rule: 0/5 seeds, 1 or 2 pairs out of 9 per seed. Each seed produces one or two pair **idiolects**, perfect ones. The 13 learned pairs stay ≥ 90 % at 100 digits (13/13).
- **Verdict:** negative for the common language.
- **Takeaway:** collective all-or-nothing **cuts the signal** (0.0 to 0.1 % of team rounds succeed); replay divides by 3.5 the number of fresh problems seen.

#### 21. E016, amendment A2: is a denser signal enough? — [branch](https://github.com/malikkaraoui/EV-LLM/tree/exp/e016-a2/research/experiments/E016-mouches) (A2 section of the README) · not yet reviewed (cross-checked by the orchestrator)
- **Prior art (in-depth search, verdict "partially done"):** Tieleman 2019 and Michel et al. 2023 (the latter not read), where random partner swapping already reduces idiolects; Mahaut et al.; Marincat 2026.
- **Changed:** reward = fraction of correct columns, or a 1-digit curriculum. Guard pilot preregistered before any run.
- **Result:** **1 pair out of 9** in both cases. Senders freeze even faster (entropy 0.002 nat for the dense-signal pilot, 0.018 for the curriculum one, against 0.03–0.16 for IND in E016). The planned conditions were not launched. Compute: ≈ 3 min.
- **Verdict:** clean stop at the guard pilot.
- **Takeaway:** "a dense signal is missing" is refuted in this form (scalar per-item credit). [HYPOTHESIS] The bottleneck would be credit assignment and exploration.

</details>

---

## What we believe we know today

- [VERIFIED — E011, E012, E013] **Computing is easy with almost nothing.** Once the digits are aligned, the carry is discovered by evolution (E012: one hidden unit; 2/5 seeds with 100 examples, 4/5 with 1,000) or learned (E013: 1,131 parameters), stays stable under cross-entropy (E011), and holds up to 1,000 digits (E013: 100 % with two state numbers, or with 10,000 examples).
- [VERIFIED — E008, E009-bis, E010, E013 I2, E014 R0] **The wall is locating, aligning, wiring.** Whenever the system must find on its own which digit to read, no seed reaches 90 % at 16 digits, whatever its size (from ~1,900 parameters to ~3.2 million), except one seed out of five with a curriculum (E014 R0b, 1/5 at 16 and 100 digits); the known fix (E008 B-REF) holds only one digit beyond (91.2 % at 6).
- [VERIFIED — E014, E015 ECH0, E016 DONNÉ] **What got over the wall: a symbolic interface between frozen skills.** Two frozen skills compose without retraining: at least 90 % exact at 16 and 100 digits on 4/5 seeds when the interface is given (E014 R1G, which passes probabilities), 100 % on 2/5 seeds when the wiring is given and the interface must be invented (E015 ECH0), and on 9/9 pairs × 5/5 seeds when the interface is given (E016 DONNÉ, 100 % at 100 digits). At 1,000 digits: 1/5 (E014) and 71.7 % (DONNÉ), limited by reading; ECH0 keeps its 2/5, its limit being the champion on pure carry propagation.
- [VERIFIED — E012 X3, E015, E016, E016-A2] **What did not get over it:** blind evolution without alignment, free assembly, all-or-nothing social pressure, a dense scalar signal.
- [VERIFIED — E005, E006, E008, E010, E014, E015] **Misplaced confidence is blind.** Errors are often "confident" when confidence bears on the wrong step: the copy, the computation without the reading, the champions without the interface. A confidence taken at each step, reading included, separates much better (E014, post hoc).
- [HYPOTHESIS] The missing lever would be an **intermediate signal the machine gives itself** (consistency between modules, prediction of its own flows), rather than the final verdict alone. None of this has been tested.

---

## Dead ends, and why they are useful

So that these cycles need not be repeated.

| # | Dead end | Where | What happened · what we do now |
|---|---|---|---|
| 1 | Unreachable criterion | A0, A0-bis, A0-ter | Even an oracle failed: the criterion rewarded continuous progress and depended on the luck of the first world. → Oracle at 100 % and "memorising" at 0 % before any measurement. |
| 2 | Ratio to a ceiling under noise | E002 | A ratio to a negative ceiling is undefined. → Measure a difference to a ceiling that checks its premises (E002-bis). |
| 3 | Inert trigger | A0 | A verification cost in absolute bits, while R is a ratio, made every verification unprofitable. |
| 4 | Under-budget and shared GPU | E009 | No learning even in distribution: the question was not settled, it was not asked. → A pilot that checks the distribution is being learned. |
| 5 | Architecture alone without alignment | E009-bis | One run out of five learns, and it does not generalise. |
| 6 | Rule stated in one sentence | E010 | A model that does not read language gets nothing from it. |
| 7 | Confidence on the wrong step | E010, E014, E015 | See [What we believe we know today](#what-we-believe-we-know-today). |
| 8 | Approximate differentiable MDL | E011 | Behaves like a weight penalty and breaks one seed: not to be reused as is. |
| 9 | Evolution in binary | E012 | All seeds fall into a "hesitant" trap that could only be left through more costly steps; truncation selection forbids it. |
| 10 | Single-number state | E013 | Perfect in distribution, wrong and confident on sparse numbers; a second state number is enough here. |
| 11 | Learned hard pointers | E014 R2 | 0 even in distribution. [HYPOTHESIS] Optimisation instability, not evidence against pointers. |
| 12 | Free assembly | E015 | Needle-in-a-haystack landscape: more trials (400,000 in the pilot) do not change the "copy a" attractor. |
| 13 | Collective all-or-nothing with replay | E016 | Freezes the team instead of building a bridge. |
| 14 | Dense scalar signal and short curriculum | E016-A2 | Harder lock-in (lower sender entropy), no take-off. |
| 15 | API access | E001, E003 | Credit card required despite "free", 5 requests per minute for the account, models closed at the free tier, provider not enforced. |
| 16 | Tooling incidents | E002-bis, E013, 26/09 | Iteration order depending on `PYTHONHASHSEED` (E002-bis). Stale `.pyc` after a same-size mutation restored within the same second (E013 → `PYTHONDONTWRITEBYTECODE=1`). Shared state file overwritten by a window (26/09). |

---

## Open leads

*Not launched, no promises.*

- **Redesign the E013 synthesis**, one source per figure, then have it reviewed. E008 and E013 can then be merged.
- **Per-column credit** (E016). The reward of column t only pushes the choices of column t; other variants are named in the E016 README (entropy floor, alternating frozen partner).
- **E015-A2: the interface as a first-class object.** A co-evolved archive of interfaces, judged on their reuse, frozen, on never-seen tasks. A prior-art list is being prepared with its mandate (M0033), not yet in the repository. The neighbouring lead, an intermediate signal the machine gives itself (co-evolving problems with solvers being its counter-tack), was the subject of an orchestrator search on 27/09 (novelty search, MCC by Brant & Stanley, PowerPlay, DreamCoder, HOUDINI, CRL); its verdict, "every building block exists, the assembly does not", is recorded with its sources in [`vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md`](vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md) [VERIFIED — sources listed in the note].
- **ACQUIRE criterion v2** (A0-ter): contrast with an amnesic twin, threshold calibrated on noise, validated first on the oracle.

---

## Reproduce

**Machine used:** Apple M1 Mac (16 GB), Python 3, MLX 0.29.3, numpy 2.0.2.
**Network:** E001 to E007 call a paid API through the Vercel gateway and need a key in a `.env` file (template: [`.env.example`](.env.example)), never versioned. All other experiments run offline.

**Environment** (from the E008 README; `requirements.txt` is on the `exp/e008-addition` branch):

```bash
python3 -m venv $HOME/.venvs/ev-llm-e008
$HOME/.venvs/ev-llm-e008/bin/pip install -r research/experiments/E008-addition/requirements.txt
```

**Running an experiment on a branch:** `git checkout <branch>`, then the test command below from the repository root. Only the **test** commands are listed; full commands (training, evaluation, analysis) are in each experiment's README.

<details>
<summary><b>Test commands, per experiment</b></summary>

<br>

| experiment | branch | tests (command from the README) |
|---|---|---|
| E001 | `main` | `cd research/experiments/E001-jev-sonde && python3 -m unittest test_aggregate` |
| E002 | `main` | `cd research/experiments/E002-relations-opaques && python3 -m unittest discover` |
| E002-bis | `main` | `cd research/experiments/E002bis-mesure && python3 -m unittest discover` |
| E003 | `exp/e003-etalon-llm` | `cd research/experiments/E003-etalon-llm && python3 -m unittest -v test_run_llm` |
| E006 | `exp/e006-replication-frontiere` | `cd research/experiments/E006-replication-frontiere && python3 -m unittest test_run_paced` |
| E007 | `exp/e007-regles` | `cd research/experiments/E007-regles && python3 -m unittest test_run_e007` |
| A0 | `exp/a0-candidat` | `cd research/candidats/A0 && python3 -m unittest discover` |
| A0-bis | `exp/a0bis-candidat` | `cd research/candidats/A0bis && python3 -m unittest discover` |
| A0-ter | `exp/a0ter-candidat` | `cd research/candidats/A0ter/oracle && python3 -m unittest discover` |
| E008 | `exp/e008-addition` | `cd research/experiments/E008-addition && $PY -m unittest -v test_e008` |
| E009 | `exp/e009-procedure-apprise` | `cd research/experiments/E009-procedure-apprise && $PY -m unittest -v test_e009` |
| E010 | `exp/e010-enseignement` | `cd research/experiments/E010-enseignement && $PY -m unittest -v test_e010` |
| E011 | `exp/e011-objectif-mdl` | `cd research/experiments/E011-objectif-mdl && $PY -m unittest -v test_e011` |
| E012 | `exp/e012-evolution` | `cd research/experiments/E012-evolution && $PY -m unittest -v test_e012` |
| E013 | `exp/e013-insecte` | `cd research/experiments/E013-insecte && $PY -m unittest -v test_e013` |

`$PY` stands for `$HOME/.venvs/ev-llm-e008/bin/python`. For E013, the READMEs also require `export PYTHONDONTWRITEBYTECODE=1`.

Commands given as is by their README, without `cd`:
- E005 (`main`): no test command of its own; replay goes through its scripts and through E001's `run.py` / `aggregate.py` (see its README).
- E009-bis: `python -m unittest test_e009bis` (in its folder).
- E014: `python -m unittest test_e014`.
- E015: `python -m unittest test_e015`.
- E016: `source $HOME/.venvs/ev-llm-e008/bin/activate`, `cd research/experiments/E016-mouches`, `python test_e016.py`.
- E016-A2: the README cites `test_e016a2.py` (4 tests) without a command; none is therefore given here.

</details>

**Determinism.** The MLX GPU is not bit-for-bit reproducible: a replay gives very close figures, not necessarily identical ones. The numpy experiments on CPU (E011, E012) and the E002 / A0 benches are deterministic, with seeds or `PYTHONHASHSEED` fixed.

---

## Repository layout

```text
EV-LLM/
├── README.md                                   ← you are here
├── LICENSE                                     MIT
├── architecture_cognitive_post_transformer.md  starting hypothesis (FR, v2)
├── GENESE.md                                   day-by-day path, mistakes included (FR)
├── docs/archive/                               superseded documents (architecture v1)
├── research/experiments/                       one folder per experiment (reviewed ones on main)
├── vault/                                      the orchestration record
│   ├── echanges/                               mandates and reports
│   ├── revues/                                 independent reviews (R0xx)
│   ├── reprise/                                dashboard and index
│   ├── notes/ · decisions/ · lecons/           notes, decisions, lessons learned
│   └── runtime/                                supervisor doctrine (state files are git-ignored)
├── config/harnais.json                         orchestration settings
├── scripts/harnais-hooks/                      git hooks (index size limit, signature, review gate on main)
└── .claude/skills/orchestration-bureau/        orchestration convention
```

Experiments not yet merged live on their `exp/*` branch (and candidates A0–A0-ter under `research/candidats/`); the table above links to each one.

---

## How the project is run

An orchestration window, which writes no code, writes autonomous mandates. A deterministic supervisor launches each working window, and every deliverable goes through an independent review before any merge. The repository is public; no secret is versioned (the API key stays in a git-ignored `.env`). Mandates, reports, reviews and dashboard live in [`vault/`](vault/) — index: [`vault/reprise/00_INDEX.md`](vault/reprise/00_INDEX.md), reviews: [`vault/revues/`](vault/revues/).

---

## License and citation

MIT License — see [`LICENSE`](LICENSE). Code, experiment reports and this log are all under MIT.

To cite an experiment, point to the README of its folder and the SHA of the commit read: the figures there are tied to their result files.

<sub>The README is maintained in English. A French version exists in git history (commit `99ccc79`).</sub>
