# 05 — A metric worth reporting: the size × time × success profile

The construct gap (finding 00) and the human-labor equivocation (finding 01) have a constructive fix.
The marketing question has three dimensions — **how large a program, how much faster than a human, and
how reliably** — and "% Resolved = 56%" collapses all three into one number. The fix is to *un-collapse*
them. But the honest deliverable is a **preregistered profile**, not a catchy three-number slogan: the
slogan ("N× faster at X% on programs up to S") is a valid *readout* only where the profile supports it.
This finding states the dimensions at their true strength — a first draft, reviewed hard (see the
`## Caveats` the critique forced), not a ready-made metric.

## The three dimensions

> **(1) Size.** A covariate, not a difficulty score. LoC (MirrorCode's Table 3) is easy but gameable —
> it swings with language verbosity, generated code, bundled assets, and how narrowly a subcommand is
> scoped, and a 2k-LoC parser can be harder than a 20k-LoC utility with a tiny tested surface. So pair
> LoC with the **tested behavioral surface** (independently specified features, interface/input-domain
> breadth) and predeclare exactly what counts (revision, comments, generated code, vendored deps,
> subcommand scope). Size is the *x-axis*; difficulty must be estimated, not read off LoC.
>
> **(2) Time-to-success (the speed axis).** Not a naive `human_time / AI_time` ratio — that is
> undefined when either side fails and survivor-biased when conditioned on success, discarding exactly
> the hard cases that define the frontier. Instead treat non-completion as **right-censored** and
> estimate the success-probability-vs-elapsed-time curve for each population. A single compression
> factor is then defined only *at a predeclared success probability* (e.g., the time each population
> needs to reach 50% whole-task success); if a population never reaches it within the study horizon,
> report a bound, not a ratio.
>
> **(3) Whole-task success (the accuracy axis).** The primary outcome is MirrorCode's own unit — a task
> passes all tests or it does not — as a **binomial over independent runs/tasks**, where a Wilson
> interval is legitimate. The per-*test* pass fraction (e.g. 2000/2001) is a **diagnostic, not** a
> Wilson-able correctness measure: tests share fixtures and code paths, one defect fails many at once,
> so a narrow interval on it describes the finite suite, not the program.

## Report a surface, not a slogan

Size is the x-axis, not a number to average in. Speed and accuracy vary *with* size — MirrorCode's own
Figure 3 shows the whole-task **solve rate** falling from the S bucket to ~0 on the L targets (it is
silent on how *time* scales, which the study would measure) — so a single collapsed "56%, N× faster"
conflates "reimplements small utilities fast and reliably" with "cannot touch a large program." The
deliverable is a **Pareto profile**: success probability and time-to-success as functions of size and
task covariates, each carrying its budget. The title's "*largest* project" claim is then a
size-conditioned success probability under a stated population, model, scaffold, and budget — *"under
protocol Q, the estimated size at which whole-task success drops below 50% is S, 95% CI […]"* — not a
deterministic point and not a scaling law a convenience sample of 25 confounded programs could
establish.

## "Same conditions" needs a written protocol

"Human vs AI on the same task" is only meaningful under a predeclared, construct-equivalent protocol,
because these knobs move the numbers with no capability change: which docs/tooling each side gets;
whether human breaks and AI overnight latency count as "wall-clock"; whether AI runs are parallelized
or best-of-*n* or first-trajectory; whether the scaffold, prompts, and stopping rules are frozen;
participant skill and domain familiarity; and the intervention protocol (the "on its own" claim dies if
a human curates the winning run). Freeze these in advance or the comparison is unfalsifiable.

## Wall-clock, and also cost — neither alone

Time is the capability-relevant axis: a model's dollar cost is not capability, and MirrorCode's headline
"$251"/"$2,600" speak to inference spend. But **cost is not nothing** — it sets feasibility, how many
retries are affordable, and whether parallelism can *buy* lower wall-clock (which is exactly why
wall-clock alone is gameable: spend 1000× compute in parallel, report a dramatic latency drop). So
report both: primary outcome is success-vs-time under a fixed protocol; alongside it log active human
labor, tokens/compute/dollar cost, number of attempts, and parallelism. Price is an *operational*
measure, not the capability axis — and not irrelevant.

## Statistics, honestly

- **Tasks, not tests, are the primary independent unit** for any benchmark-wide claim. Use hierarchical
  inference that separates variation across tests, runs, people, tasks, languages, and size; bootstrap
  at the task level.
- **Small n is exploratory, not presumptively adequate.** Five human runs give honestly *wide*
  intervals (5/5 whole-task successes is a Wilson 95% CI of ~57–100%), and whether 5–10 runs can
  separate 10× from 100× depends entirely on between-engineer and between-run time variance — run a
  pilot and a precision analysis first; predeclare the estimand (paired ratios? median-of-ratios? — they
  differ, since median(H/A) ≠ median(H)/median(A)).
- **An n=1 measurement is a case study, not an estimate.** Predeclared, it is *useful illustrative
  evidence*; it is not "strictly stronger" than expert elicitation, and selected after seeing results it
  can mislead. Label it "illustrative case, no population inference" — an asterisk alone does not stop
  headline laundering.

## Why this lands as a request, not a result

**Had MirrorCode published its run records** — per-task, per-model time-to-success and pass grids, with
budgets and parallelism — we could have *estimated* the success-vs-time surface ourselves and reported
numbers instead of a design. It did not (findings 02, 03): the per-run receipts are unpublished though
they already exist as data. And MirrorCode cannot report even one honest compression factor today: it
has no task with both a completed human baseline and an AI run under a matched protocol. Its closest
pair is mismatched — a ~2,000-LoC human task (20 h, *incomplete*) against `gotree` (16k LoC, 14 h AI) —
and dividing those repeats the exact apples-to-oranges this audit flags.

## The challenge, stated plainly

Preregister a protocol (tools, docs, budget, retries, parallelism, intervention, stopping, timeout,
success criterion). Run blinded human reimplementation on a handful of targets — at least the
private/post-cutoff ones, where recall cannot help — construct-equivalent to the agent's conditions.
Report the **profile**: whole-task success and time-to-success (censoring failures) against size and
tested-surface, with task-level intervals, alongside cost/tokens/parallelism. That profile answers the
size/speed/reliability question the marketing gestures at — and, where it is well-supported, collapses
to the one honest headline sentence the current "56%" cannot earn.

*Sources: MirrorCode [arXiv:2606.30182](https://arxiv.org/abs/2606.30182) §3 (compute-vs-score, cost),
§4.1–4.2 (time horizon, footnote 7 human baseline), Fig 3 (solve-rate vs size); [finding
01](01_human_labor.md), [finding 03](03_how_much_is_recall.md). Wilson: E. B. Wilson, *JASA* 22 (1927),
209–212.*
