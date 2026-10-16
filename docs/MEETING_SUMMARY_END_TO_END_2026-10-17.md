# Supervisor Meeting Summary — End-to-End Research Outcome

**Date:** 17 October 2026  
**Project:** CAPC Simulator — MSc Research  
**Topic:** End-to-End Research Progress, Main Experimental Outcome, Interpretation, and Next Direction

> **How to use this file:** এই document-টা meeting-এ script হিসেবে পড়ার মতো করে লেখা হয়েছে। Bangla explanation-এর সাথে প্রয়োজনীয় English technical terms রাখা হয়েছে, যাতে discussion natural থাকে এবং research terminology precise থাকে।

---

## 1. Opening / Meeting শুরু করার জন্য

**Script:**

আজকে আমি আমার research-এর **end-to-end progress and outcome** short but complete way-তে explain করতে চাই।

আমার research-এর main problem হচ্ছে **blockchain-based IoT systems-এ cross-shard transaction coordination-এর latency**, especially যখন workload bursty হয় এবং একই সময়ে multiple transactions overlapping shards access করতে চায়।

আমার original idea ছিল **Contention-Aware Priority Coordination, বা CAPC**, যেখানে scheduler শুধু FIFO order follow না করে **contention, urgency, waiting age, dependency burden, এবং recent shard-lock pressure** consider করে transaction service order decide করবে।

Research-এর main question ছিল: **এই ধরনের contention-aware priority scheduling কি atomic cross-shard semantics preserve করে p99 tail latency কমাতে পারে?**

আমি এখন full implementation, verification, 5,400-run main experiment, audit, statistical analysis, এবং thesis-level interpretation complete করেছি। সবচেয়ে important point হচ্ছে—**original CAPC formulation expected p99 improvement দেয়নি**। কিন্তু এই negative result থেকে বেশ কিছু strong and interesting system-level finding পাওয়া গেছে।

---

## 2. Research Scope — আমি আসলে কী design করেছি

**Script:**

প্রথমে scope clear করা important। CAPC কোনো full blockchain protocol না, consensus algorithm না, এবং sharding architecture redesign-ও না।

এটা একটা **scheduling-layer intervention**। Logical flow হচ্ছে:

```text
Cross-shard coordination queue
        ↓
Scheduler
        ↓
Atomic coordination service
```

Matched atomic schedulers-এর ক্ষেত্রে সবকিছু same রাখা হয়েছে—same workload trace, same shard requirements, same service times, same worker capacity, same all-or-nothing shard locking, এবং same non-preemptive service semantics।

তাই treatment difference মূলত **service order**-এ সীমাবদ্ধ। এর ফলে scheduling effect isolate করা যায়।

Primary matched baseline হচ্ছে **Static Atomic FIFO**। Diagnostic FIFO descriptive reference হিসেবে আছে, কিন্তু এটা primary matched causal comparison-এর অংশ না, কারণ এর atomic eligibility semantics একই না।

Repository overview এবং scope README-তে documented আছে: [README.md](../README.md).

---

## 3. CAPC-v1 Design — Algorithm কীভাবে কাজ করেছে

**Script:**

CAPC প্রথমে transaction eligibility check করে। অর্থাৎ কোনো transaction service-এ যেতে হলে worker available হতে হবে এবং তার required সব logical shard একই সময়ে available হতে হবে। Waiting transaction partial lock ধরে রাখে না।

Eligible transactions-এর মধ্যে CAPC score calculate করা হয়। Conceptually score-এর components ছিল:

- **Urgency / Priority**
- **Waiting Age**
- **Shard Dependency Burden**
- **Recent Required-Shard Lock Pressure**
- এবং global **Contention Score** দ্বারা dependency/lock-pressure terms amplify করা হয়।

Frozen CAPC score ছিল:

```text
S_i(t) = w_U U_i + w_A A_i(t)
         + [1 + gamma C(t)]
           [w_D (1 - D_i) + w_H (1 - H_i(t))]
```

Frozen ranking weights ছিল:

- urgency = `0.35`
- aging = `0.30`
- dependency = `0.20`
- recent lock pressure = `0.15`

Global contention score চারটি normalized signal use করেছে:

- recent arrival pressure,
- coordination queue length,
- mean dependency pressure,
- active shard-lock proportion.

সব parameter labelled main result দেখার আগে freeze করা হয়েছিল। Main result দেখার পরে CAPC-v1 retune করা হয়নি।

---

## 4. Simulation Design — Experiment কীভাবে setup করেছি

**Script:**

Evaluation-এর জন্য আমি Python-based **discrete-event simulation** use করেছি। Workload-এর burst behaviour represent করার জন্য two-state **Markov-Modulated Poisson Process, MMPP** use করেছি।

NORMAL state arrival rate ছিল `20 tx/s`, আর BURST state ছিল `60 tx/s`।

Main system factors ছিল:

- shard count: `4, 8, 16`
- cross-shard ratio: `10%, 30%, 50%`
- coordination workers: `2, 4`

এতে total fixed system condition হয়েছে:

```text
3 shard levels × 3 cross-shard ratios × 2 worker levels = 18 conditions
```

প্রতিটি condition-এর জন্য `60` paired seeds use করেছি। পাঁচটি scheduler treatment ছিল:

1. Diagnostic FIFO
2. Static Atomic FIFO
3. Full CAPC
4. CAPC-No-Contention
5. CAPC-No-Priority

তাই full primary matrix:

```text
18 conditions × 60 seeds × 5 schedulers = 5,400 runs
```

Primary performance metric ছিল **per-run p99 cross-shard end-to-end latency**। p95 supportive metric ছিল। এছাড়া mean latency, waiting time, queue behaviour, throughput, Jain fairness, starvation এবং priority-wise waiting behaviour measure করেছি।

---

## 5. Research Integrity and Reproducibility

**Script:**

এই research-এর একটা strong part হচ্ছে execution integrity। Main comparative experiment-এর code এবং configuration আগে freeze করেছি।

Frozen execution revision:

```text
00d4e2ebd7af24bd6abf35578a2d40296fb4ddc6
```

Frozen primary YAML raw SHA-256:

```text
be25b6dc8c89c3a49b891ea4c69e1c1dfe38b6e117d577bd8026c2d0094ba875
```

Final audit-এ:

- planned runs: `5,400`
- completed canonical runs: `5,400`
- missing runs: `0`
- unexpected runs: `0`
- paired condition-seed groups: `1,080/1,080`
- unequal trace hashes: `0`
- all five expected schedulers present in every paired group
- no seed replacement
- no post-result CAPC-v1 retuning

Raw transaction evidence অনেক বড় ছিল—transaction CSV input প্রায় `50.34 GB`, আর full result directory readiness check-এর সময় প্রায় `126 GB` ছিল। এজন্য post-processing memory-safe streaming approach-এ করা হয়েছে, কিন্তু reported primary analysis-এর জন্য sampling করা হয়নি।

Full post-main evidence ledger এখানে আছে: [EXPERIMENT_EVIDENCE_LOG_POST_MAIN_2026-10-16.md](EXPERIMENT_EVIDENCE_LOG_POST_MAIN_2026-10-16.md).

---

## 6. Verification — Implementation ঠিকভাবে কাজ করছে কি না

**Script:**

Performance result interpret করার আগে implementation verify করেছি।

Automated test suite-এ `31 tests PASS` করেছে। Chapter-level deterministic verification-এর `V1–V12` checks-ও PASS করেছে।

Verification-এর purpose ছিল prove করা যে:

- workload deterministic,
- paired trace same,
- lock semantics correct,
- scheduler behaviour expected,
- CAPC score calculation reproducible,
- aging monotonic,
- event accounting consistent,
- metric generation correct.

অর্থাৎ negative performance result implementation failure ধরে নেওয়ার আগে basic semantic correctness verify করা হয়েছে।

---

# 7. Research Findings

## 7.1 RQ1 — BURST workload contention-এর impact

**Script:**

RQ1-এর জন্য আমি CAPC use করিনি; শুধু matched **Static Atomic FIFO** baseline use করেছি, যাতে workload contention effect scheduler treatment দ্বারা confound না হয়।

Result খুব clear ছিল:

**BURST p99 latency NORMAL p99-এর চেয়ে 18-এর 18 condition-এই বেশি ছিল।**

এবং 18-এর 18 condition-এই paired-bootstrap 95% confidence interval zero-এর উপরে ছিল।

Cross-shard ratio বাড়ার সাথে burst amplification খুব strongly বেড়েছে।

Example হিসেবে:

- `4 shards, 50% cross-shard` condition-এ p99 increase প্রায় **+574%**।
- `8 shards, 50%, 2 workers` condition-এ প্রায় **+148%**।
- `16 shards, 50%, 2 workers` condition-এ প্রায় **+140%**।

4-shard 50% case-এ descriptive absolute value:

- NORMAL p99 ≈ `0.277 s`
- BURST p99 ≈ `1.813 s`

So RQ1 থেকে strong evidence পাওয়া গেছে যে **burst-driven contention cross-shard tail latency substantially amplify করে**। More shards এবং কিছু condition-এ more workers amplification reduce করতে পারে, যদি additional concurrency actually exploit করা যায়।

এই result thesis-এর problem motivation-কে strong empirical support দেয়।

---

## 7.2 RQ2 — Queue-entry indicators কি later waiting-এর সাথে associated?

**Script:**

RQ2-তে আমি Static Atomic FIFO-এর full transaction data use করেছি। Sampling করিনি।

Data size ছিল:

- Static runs: `1,080`
- measurement-window cross-shard observations: `13,856,346`
- complete-case rows: `13,856,346`
- missing predictor drop: `0`

Outcome ছিল:

```text
log(1 + coordination waiting time)
```

Main predictors ছিল:

- arrival rate at queue entry,
- queue length at entry,
- shard dependency degree,
- active lock conflict count at entry.

সব চারটি predictor-এর association positive ছিল। Approximate coefficients:

- arrival rate: `+0.000095`
- queue length: `+0.019729`
- dependency degree: `+0.011498`
- active lock conflicts: `+0.029507`

Native-scale interpretation roughly:

- queue-তে 1 transaction increase হলে `(1 + wait)` প্রায় `1.99%` multiply হয়,
- 1 additional active conflict প্রায় `3.0%`,
- dependency degree +1 প্রায় `1.16%`,
- arrival rate +10 tx/s প্রায় `0.095%`।

Important limitation হচ্ছে এগুলো **associations, causal effects না**। আর predictors-এর scales different, তাই raw coefficient দেখে “which predictor is most important” বলা যাবে না।

So RQ2-এর core finding হচ্ছে: **queue-entry system state future coordination waiting-এর সাথে measurably associated**।

---

## 7.3 RQ3 — CAPC design question

**Script:**

RQ3 performance question না; এটা design question। এখানে contribution ছিল atomicity-preserving scheduler design এবং verified implementation।

CAPC design-এর important properties:

- atomic eligibility filtering,
- urgency awareness,
- aging,
- dependency awareness,
- recent lock-pressure awareness,
- global contention amplification,
- deterministic tie-breaking,
- non-preemptive service,
- all-or-nothing shard locks,
- no online retuning.

So RQ3-এর answer হচ্ছে: এমন একটা CAPC mechanism successfully design এবং implement করা গেছে যেটা common atomic service semantics change না করে service order adapt করতে পারে।

কিন্তু design verification performance success prove করে না—performance answer RQ4-এ এসেছে।

---

## 7.4 RQ4 — CAPC কি p99 latency improve করেছে?

**Script:**

এখানে সবচেয়ে important এবং unexpected result এসেছে।

Primary comparison ছিল **CAPC versus Static Atomic FIFO**, 18 condition-এর প্রতিটিতে 60 paired seeds use করে।

Predeclared primary model ছিল log-p99 mixed-effects model। আমি modelটা run করেছি, কিন্তু inferentially usable ছিল না, কারণ random-effect covariance singular হয়েছে, group variance zero estimate হয়েছে, likelihood/AIC/BIC degenerate হয়েছে, Hessian non-positive-definite হয়েছে। তাই ওই failed model-এর coefficients use করিনি।

Protocol অনুযায়ী predeclared fallback use করেছি:

- paired Wilcoxon within each condition,
- Holm correction across 18 conditions,
- plus paired bootstrap uncertainty.

Final confirmatory count:

- **significant harm: 14/18**
- **significant benefit: 2/18**
- **not significant: 1/18**
- **significant distribution shift with zero median: 1/18**
- practical success, অর্থাৎ >=10% p99 reduction with beneficial uncertainty: **0/18**
- medium/high-contention conditions: **12/12 significant harm**

So original CAPC-v1-এর intended global p99 reduction hypothesis **supported হয়নি**।

যে 2টা beneficial low-contention case ছিল, সেখানে improvement মাত্র প্রায় `0.3%`, তাই predeclared 10% practical threshold-এর অনেক নিচে।

সবচেয়ে severe example ছিল:

```text
4 shards, 50% cross-shard, 2 workers
```

Static mean p99 ≈ `1.521 s`  
CAPC mean p99 ≈ `13.875 s`

Ratio of condition means অনুযায়ী CAPC প্রায় `9.12×` Static value হয়েছে।

এই result intentionally unchanged রেখেছি। Positive result দেখানোর জন্য কোনো post-hoc parameter tuning CAPC-v1-এর উপর করা হয়নি।

Detailed frozen primary results এখানে আছে: [PRIMARY_RESULTS_2026-10-16.md](PRIMARY_RESULTS_2026-10-16.md).

---

# 8. Negative Result-এর মধ্যে Interesting Finding কী পেলাম

## 8.1 Throughput collapse হয়নি

**Script:**

প্রথমে আমার suspicion ছিল CAPC হয়তো capacity reduce করছে। কিন্তু evidence সেটা fully support করে না।

Across 1,080 CAPC-vs-Static paired seed units:

- throughput preservation criterion pass করেছে **100%**,
- Jain completion-ratio preservationও **100%**।

Worker utilisation-ও অনেক condition-এ প্রায় unchanged ছিল।

So এটা simple throughput collapse বা obvious resource under-utilisation story না।

---

## 8.2 p95 ভালো/স্থির থেকেও extreme tail খারাপ হয়েছে

**Script:**

সবচেয়ে interesting pattern হচ্ছে কিছু 8-shard এবং 16-shard high-contention condition-এ **p95 waiting improve বা stable হয়েছে**, কিন্তু **p99, p99.5 এবং maximum waiting worsen করেছে**।

এর মানে scheduler হয়তো majority transactions-এর waiting কিছুটা improve করছে, কিন্তু small subset-এর delay extreme tail-এ push করছে।

এই pattern-কে আমি **tail redistribution / tail polarization** হিসেবে interpret করছি—carefully, as an observed mechanism-consistent pattern, not as a proven universal causal mechanism।

---

## 8.3 Priority-wise delay redistribution

**Script:**

4-shard, 50% high-contention case-এ pattern আরও clear।

CAPC versus Static-এর selected waiting-tail diagnostics:

- overall p95 waiting ≈ `+52%`
- p99 waiting ≈ `+840%`
- p99.5 waiting ≈ `+1160%`
- maximum waiting ≈ `+1800%`

Priority breakdown-এ:

- HIGH-priority p99 waiting ≈ **-42%**, অর্থাৎ improve করেছে,
- MEDIUM-priority p99 ≈ **+488%**,
- LOW-priority p99 ≈ **+1698%**,
- LOW-priority maximum ≈ **+1865%**।

So evidence strongly suggests যে urgency-aware reordering কিছু urgent transactions help করতে পারে, কিন্তু extreme delay lower-priority traffic-এর দিকে redistribute হতে পারে।

তবে আমি **priority is the sole cause** বলছি না। কারণ No-Priority ablation-ও অনেক condition-এ harmful ছিল।

---

## 8.4 Ablation থেকে কী শিখেছি

**Script:**

Full CAPC, CAPC-No-Contention, এবং CAPC-No-Priority—তিনটারই harmful confidence interval `14/18` condition-এ ছিল।

Component effect regime-dependent ছিল। তাই:

- শুধু priority remove করলে problem solve হয়নি,
- শুধু contention amplification remove করলেও solve হয়নি,
- কোনো single component universal culprit হিসেবে identify করা যায়নি।

এই result suggests interaction between **priority, aging, lock eligibility, dependency, এবং contention-sensitive ordering** গুরুত্বপূর্ণ হতে পারে।

Double-ablation করা হয়নি, তাই unique interaction mechanism claim করছি না।

---

# 9. আমার Research Contribution এখন কীভাবে Position করছি

**Script:**

Original expectation ছিল CAPC p99 latency reduce করবে। সেটা হয়নি। তাই contribution wording আমি change করেছি—result hide না করে।

আমার current contribution পাঁচটা অংশে explain করা যায়:

**First**, burst-driven IoT workload cross-shard tail latency কীভাবে amplify করে সেটা systematicভাবে quantify করেছি।

**Second**, 13.8 million-এর বেশি cross-shard transaction observation use করে queue-entry indicators এবং subsequent waiting-এর association establish করেছি।

**Third**, atomicity-preserving contention-aware priority scheduler CAPC design এবং verify করেছি।

**Fourth**, full paired 5,400-run experiment-এর মাধ্যমে দেখিয়েছি যে original CAPC formulation global p99 improve করে না; বরং medium/high contention-এ consistently harmful হতে পারে।

**Fifth**, diagnostic analysis থেকে একটা important design lesson পাওয়া গেছে: **priority-aware atomic scheduling average or p95 behaviour improve করলেও extreme tail lower-priority traffic-এর দিকে redistribute করতে পারে**।

আমার কাছে এই fifth finding-টাই future algorithm design-এর জন্য সবচেয়ে useful insight।

---

# 10. Thesis Status

**Script:**

Thesis-এর Chapters 1 থেকে 7 complete draft হয়েছে।

Current structure:

1. Introduction
2. Literature Review
3. Research Methodology
4. CAPC System Design and Algorithm Development
5. Implementation and Verification
6. Results, Analysis and Discussion
7. Conclusion and Future Work

Chapter 6 এবং Chapter 7-এ negative RQ4 result transparently রাখা হয়েছে। RQ1, RQ2, RQ4 evidence এখন frozen।

Original CAPC-v1 result rewrite বা retune করে positive বানানো হয়নি।

Current thesis story হচ্ছে:

```text
Problem identification
→ CAPC design
→ verified implementation
→ frozen paired experiment
→ negative primary result
→ diagnostic mechanism insight
→ design implications and future work
```

---

# 11. Current Limitation

**Script:**

Main limitations আমি openly acknowledge করছি।

প্রথমত, এটা controlled discrete-event simulation; production blockchain implementation না। তাই external validity future deployment study দিয়ে test করতে হবে।

দ্বিতীয়ত, workload synthetic MMPP-based। এটা controlled burst behaviour দেয়, কিন্তু real IoT trace-এর সব complexity represent করে না।

তৃতীয়ত, RQ2 result associational।

চতুর্থত, original CAPC parameters intentionally freeze করা হয়েছিল; main result দেখে retune করা হয়নি। তাই current CAPC-v1 result algorithm-এর frozen formulation-এর result, broader family-এর theoretical limit না।

পঞ্চমত, ablation analysis single-component removals use করেছে; full interaction decomposition করা হয়নি।

---

# 12. Proposed Next Direction — Evidence-Informed CAPC Redesign

**Script:**

Current finding দেখে আমি একটা **separate redesign track** consider করছি, original CAPC-v1 result change করার জন্য না।

Main redesign idea হচ্ছে: urgency benefit completely remove না করে **extreme-tail protection** add করা। Working concept হচ্ছে **CAPC-v2 / TailGuard**।

Possible design directions:

- bounded urgency dominance,
- stronger nonlinear aging,
- soft-tail / hard-tail rescue,
- repeated bypass protection,
- high contention-এ urgency weight reduce করে aging/tail protection increase,
- low-priority extreme waiting explicitly guard করা।

Research-integrity plan হবে:

```text
CAPC-v1 evidence remains frozen
→ separate simulator/redesign track
→ exploratory calibration on new seeds
→ final algorithm + parameters freeze
→ completely fresh unseen validation seeds
→ only then make confirmatory claims
```

So if redesign positive হয়, আমি এটাকে original result-এর replacement বলব না। বরং research evolution হিসেবে দেখাব:

```text
initial design
→ evaluation
→ identified failure mode
→ evidence-informed redesign
→ independent validation
```

এই redesign-এর জন্য আলাদা repository already create করেছি:

`capc-v2-tailguard-simulator`

কিন্তু CAPC-v2 algorithm এখনো final না এবং কোনো positive result claim করা হয়নি।

---

# 13. Meeting-এর জন্য Short Final Statement

**Script:**

সব মিলিয়ে, আমার original CAPC hypothesis p99 latency improvement-এর ক্ষেত্রে supported হয়নি। Frozen primary experiment-এ practical p99 success `0/18`, এবং medium/high contention-এর `12/12` condition-এ CAPC significantly harmful ছিল।

তবে research থেকে তিনটা strong outcome পেয়েছি।

এক, burst-driven contention cross-shard tail latency strongly amplify করে।

দুই, queue-entry system state future waiting-এর সাথে measurable positive association দেখায়।

তিন, সবচেয়ে interestingভাবে, priority-aware atomic scheduling majority behaviour preserve বা কিছু high-priority traffic improve করলেও extreme tail lower-priority transactions-এর দিকে redistribute করতে পারে।

তাই আমি negative result-টাকে hide করছি না। Instead, এটাকে **design boundary and mechanism insight** হিসেবে use করছি।

আমার next question হচ্ছে: **এই observed tail-polarization problem explicitly control করে এমন redesigned scheduler independently validate করা যায় কি না।**

এই direction supervisor-এর মতামত নিয়ে pursue করতে চাই।

---

# 14. Very Short 60-Second Version

Meeting-এ সময় কম থাকলে এই অংশটা বলা যাবে:

**Script:**

আমার CAPC main experiment complete হয়েছে—18 conditions, 60 paired seeds, 5 schedulers, total 5,400 runs। Full provenance and paired-trace audit pass করেছে। RQ1-এ সব 18 condition-এ BURST p99 NORMAL-এর চেয়ে significantly higher ছিল। RQ2-তে 13.86 million cross-shard observation থেকে arrival rate, queue length, dependency degree এবং active-lock conflicts—সবগুলো subsequent waiting-এর সাথে positive association দেখিয়েছে।

কিন্তু RQ4-এ original CAPC expected result দেয়নি। Practical p99 success 0/18, significant harm 14/18, এবং medium/high contention-এ 12/12 harmful। তবে throughput এবং Jain fairness preserved ছিল। Diagnostics-এ দেখেছি কিছু ক্ষেত্রে high-priority tail improve হলেও medium/low-priority extreme tail খুব বেশি worsen করেছে। তাই resultটা simple capacity failure না; evidence tail-delay redistribution-এর সাথে consistent।

আমি CAPC-v1 result unchanged রাখছি। Next step হিসেবে separate CAPC-v2/TailGuard redesign consider করছি, যেখানে tail protection add করে completely new calibration এবং unseen validation seeds use করব।

---

## Evidence References

- [README.md](../README.md)
- [Frozen Primary Results](PRIMARY_RESULTS_2026-10-16.md)
- [Post-Main Experiment Evidence Log](EXPERIMENT_EVIDENCE_LOG_POST_MAIN_2026-10-16.md)
- [Main Experiment Completion and Audit](MAIN_EXPERIMENT_COMPLETION_2026-10-16.md)
- [Thesis Evidence Index](THESIS_EVIDENCE_INDEX_2026-10-16.md)
- [Research Integrity](RESEARCH_INTEGRITY.md)

---

## Research-Integrity Reminder

This meeting summary intentionally preserves the frozen outcome of CAPC-v1. It does not reinterpret negative results as success, does not report unperformed CAPC-v2 experiments, and does not make causal claims from the RQ2 association model.