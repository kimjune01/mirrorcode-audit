# 05 — A metric worth reporting: speed × accuracy

The construct gap (finding 00) and the human-labor equivocation (finding 01) have a constructive fix.
The marketing question is really two questions — **how much faster than a human is the model, and is it
actually right?** — and "% Resolved = 56%" answers neither. Here is the pair that does, and why a small
sample is enough to report it.

## The metric: two numbers

> **(1) Wall-clock compression factor.** `WCF = human wall-clock to pass / AI wall-clock to pass`, on
> the *same* task under *identical* conditions (reimplement from the execute-only reference + docs,
> offline). This is the **10× / 100× / 1000×** number.
>
> **(2) Accuracy at that speed.** The fraction of tests (or tasks) passed — a proportion reported with
> a **Wilson 95% CI**.

Neither alone answers the marketing claim. Speed without accuracy rewards a fast wrong answer; accuracy
without speed is today's % Resolved, silent on "does weeks of work in hours." Together they read as one
sentence: ***N× faster, at X% accuracy.*** That sentence is falsifiable; "the largest software project
AI can complete on its own" is not.

## Why the pair kills the equivocation

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
single asterisked measurement ("~12× faster at 99.95%\*, single sample") is strictly stronger than an
unmeasured belief range, because it is a measurement. The asterisk is the honesty; the belief has no
asterisk that would make it true.

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
5–10 runs per target, report the **pair**: WCF median with a bootstrap CI, and accuracy with a Wilson
CI, split by contamination status. One small table — *N× faster, at X% accuracy* — replaces four
sliding numbers with the single falsifiable measurement the marketing is reaching for.

*Sources: MirrorCode [arXiv:2606.30182](https://arxiv.org/abs/2606.30182) §4.1–4.2 (time horizon,
footnote 7 human baseline), §3 (AI wall-clock/cost); [finding 01](01_human_labor.md),
[finding 03](03_how_much_is_recall.md). Wilson: E. B. Wilson, *JASA* 22 (1927), 209–212.*
