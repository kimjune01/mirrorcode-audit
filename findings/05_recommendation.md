# 05 — A metric worth reporting: size × speed × accuracy

The construct gap (finding 00) and the human-labor equivocation (finding 01) have a constructive fix.
The marketing question is really *three* questions — **how large a program, how much faster than a
human, and at what accuracy?** — and "% Resolved = 56%" answers none. The site's own headline is a size
claim ("the *largest* software project AI can complete"), so size is not optional: it is the axis being
advertised. Here is the triple that answers it, and why a small sample is enough to report it.

## The metric: three numbers

> **(1) Size.** The program's scale — lines of code (MirrorCode's Table 3 has it) or its S/M/L bucket.
> This is the *"largest project"* axis, and it is **free**: MirrorCode already knows it.
>
> **(2) Wall-clock compression factor.** `WCF = human wall-clock to pass / AI wall-clock to pass`, on
> the *same* task under *identical* conditions (reimplement from the execute-only reference + docs,
> offline). This is the **10× / 100× / 1000×** number.
>
> **(3) Accuracy at that speed.** The fraction of tests (or tasks) passed — a proportion with a
> **Wilson 95% CI**.

None alone answers the claim. Speed without accuracy rewards a fast wrong answer; accuracy without speed
is today's % Resolved, silent on "does weeks of work in hours"; and both **collapsed across sizes** hide
that the frontier is small tools. Reported right, they read as one sentence — ***on programs up to S
lines, N× faster, at X% accuracy*** — which is falsifiable, where "the largest software project AI can
complete on its own" is not.

**Why wall-clock, not dollars.** Cost is deliberately *not* a fourth axis. A frontier model's token cost
is negligible against a human SWE's: MirrorCode's priciest single run was $2,600, set against the tens
of thousands of dollars a human's weeks of labor would cost. So dollars-per-task favors AI by a huge
margin *regardless of capability* and measures nothing interesting; the binding, meaningful variable is
**time** — how much faster, at what accuracy, on what size. (It also means MirrorCode's headline dollar
figures, "$251" and "$2,600", speak to inference spend, not capability; the capability number is the
wall-clock they sit beside.)

## Report speed and accuracy as a function of size, not collapsed

Size is not a fourth number to average in; it is the **x-axis**. Speed and accuracy both **degrade with
size** — MirrorCode's own Figure 3 shows the 100%-solve rate falling from the S bucket to ~0 on the L
targets — so a single collapsed "56%, N× faster" conflates "reimplements small utilities fast and
exactly" with "cannot touch a large program." Plot (or table) WCF and accuracy against LoC/bucket, and
the *"largest project"* claim becomes readable directly: it is the size at which accuracy (and a
worthwhile WCF) stay above a stated threshold. On MirrorCode's own results that frontier is modest —
whole-program 100% solves concentrate in the S bucket; the L targets sit near zero — which is a
defensible, specific claim, unlike the collapsed headline.

## Why the triple kills the equivocation

- **Same task, same conditions.** Both numerator and denominator are *reimplementation from an oracle*.
  No more sliding between "a human would take months" (original *creation*, finding 01) and "AI in 14 h"
  (reimplementation). The compression factor is measured against the task actually posed.
- **It forces the human baseline they mostly skipped** (finding 01/04) — but cheaply, see below.
- **It composes with METR's own time-horizon work** (which the paper cites): time-horizon asks *what
  length* of task AI can do; WCF asks *by what factor* it compresses the human clock on tasks it can do.

## You do not need a big human study

The standing objection to human baselines is cost. Both numbers are small-sample-estimable:

- **Accuracy is a binomial proportion**, so a **Wilson score interval** gives a defensible CI from a
  handful of runs. Wilson is well-behaved at small *n* and near 0 or 1 — exactly the regime here (pass
  rates of 42%, or 99.95% = 2000/2001) where the normal approximation breaks.
- **WCF is a ratio of wall-clocks.** Estimate its median and a bootstrap (or log-scale) interval from
  5–10 human runs per task. Wide intervals at small *n* are fine — they are honest, and they still
  separate 10× from 100× from 1000×.

A modest study — a few blinded, incentivized engineers on the private/post-cutoff targets — yields both
numbers with stated uncertainty. Four contributors' unblinded belief with no interval (what the paper
ships) is strictly weaker than five measured runs with a Wilson CI.

And if even that is out of budget: report a **single number, asterisked** — one blinded human run, one
AI run, one task — flagged as a low-confidence *n = 1* point estimate with no interval. Even a
single asterisked measurement ("on a 2k-LoC program, ~12× faster at 99.95%\*, single sample") is strictly stronger than an
unmeasured belief range, because it is a measurement. The asterisk is the honesty; the belief has no
asterisk that would make it true.

## It scales with the sample: point → curve

The same instrument upgrades as you spend more, and each rung is honest at its own budget:

- **n = 1 (asterisked point):** "on a 2k-LoC program, ~12× faster at 99.95%\*." One measurement, no
  claim about any other size.
- **small n (per-bucket intervals):** WCF and accuracy for the S / M / L buckets, each with a Wilson (accuracy)
  and bootstrap (speed) CI. Now you can say "on S-bucket programs, N× at X%; on L-bucket, the model
  fails" — size-resolved, not collapsed.
- **large n (a fitted relationship):** with enough targets across the size range you can *model* the
  two surfaces — accuracy(size) and WCF(size) — and state the trade-off as a law with a confidence band:
  the LoC at which 100%-accuracy crosses 50%, how WCF decays with size, where the frontier actually is.

Only the third rung licenses the title's claim. **"The largest software project AI can complete" is a
point on the accuracy(size) curve** — the size where accuracy stays above a threshold — and you cannot
name it without the curve. A single collapsed 56% is not that point; it is an average over a curve whose
shape is the whole question.

## So: 10×, 100×, or 1000×?

The marketing implies **~100×+** — weeks of human work compressed to hours. The matched,
reimplementation-vs-reimplementation reality is almost certainly **~10×**, because the human side is
also working from the oracle, not building greenfield. This audit does not assert the answer; it points
out that **MirrorCode already has the AI wall-clock and the pass grid** (finding 03), so one small human
study would decide 10× vs 100× vs 1000×. Right now the claim floats across two orders of magnitude and
the reader cannot tell which.

Note *why* this lands as a request rather than a result. **Had MirrorCode published its run records —
per-task, per-model AI wall-clock and pass grids, plus the human-baseline timings — we would have
computed the WCF ourselves**, and this finding would report a number instead of asking for one. It did
not (findings 02, 03): the per-run receipts are unpublished though they already exist as data. So we are
left with what the public artifacts allow, which is the observation that MirrorCode **cannot compute
even one honest WCF today** either: it has no task with both a completed human baseline and an AI run
under matched conditions. Its closest pair is mismatched — a ~2,000-LoC human task (20 h, incomplete)
against `gotree` (16k LoC, 14 h AI) — and dividing those would repeat the exact apples-to-oranges this
audit flags. The metric's first requirement is the baseline they skipped; its second is the receipts
they withheld.

## The challenge, stated plainly

Run blinded human reimplementation baselines on a handful of targets — at least the private/post-cutoff
ones, where recall cannot help — under the same offline, oracle-only conditions the models get. From
5–10 runs per target, report the **triple**: size (already known), WCF median with a bootstrap CI, and
accuracy with a Wilson CI, split by contamination status. One small table — *on programs up to S lines,
N× faster, at X% accuracy* — replaces four
sliding numbers with the single falsifiable measurement the marketing is reaching for.

*Sources: MirrorCode [arXiv:2606.30182](https://arxiv.org/abs/2606.30182) §4.1–4.2 (time horizon,
footnote 7 human baseline), §3 (AI wall-clock/cost); [finding 01](01_human_labor.md),
[finding 03](03_how_much_is_recall.md). Wilson: E. B. Wilson, *JASA* 22 (1927), 209–212.*
