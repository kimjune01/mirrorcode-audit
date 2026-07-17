# 03 — How much of the score is recall?

For ProgramBench the answer to "does it measure what it claims?" was *not really* — it measured recall.
MirrorCode gives us its own data to ask the same question of itself, and the honest answer is a bound,
not a point estimate, because MirrorCode ran the measurement and did not publish the number.

## What MirrorCode measured, and didn't report

MirrorCode ran a **memorization screen** (§B.3, Figure 9): it prompted each model to reproduce
functions from a target's original source and scored similarity against a baseline of five programs
published after the training cutoff (mean 33.7%, upper 95% bound ≈ 38.6%). Result: **17 of 25 targets
score above the band — evidence of memorization at p < 0.05.**

It also has per-target **solve rates** (Figure 2). The one question that decides construct validity is
the *association* between the two: do models solve the memorized targets more than the non-memorized
ones? MirrorCode never reports it. Its entire defense that performance is "not solely driven by
memorization" is **two anecdotes** — it solved non-memorized `nonogrid` and `tssql`, and failed
memorized `sed` and `ruff` (§4.3). That is four hand-picked cells of a 2×2 it never filled in.

And it cannot be filled in from public artifacts: the repo ships the harness, tasks, and gold outputs
but **neither the memorization scores nor the per-run solve results** (confirmed: no screen/results
data in 9,021 repo files). So MirrorCode's own contamination check is not reproducible — the reader
must take "not solely memorization" on faith.

## What we can bound from the published figures

Reading Figure 9 as a binary (Opus-4.7 bar above vs. within/below the baseline band — robust even
where exact heights are not), the **8 non-memorized** MirrorCode targets are approximately:

`tssql`, `hexyl`, `private_S`, `bitwise`, `texmacros`, `nonogrid`, `giac_subset`, and one borderline
(`choose`/`gron`). The other 17 are memorized.

Crossing with solvability (§3.1, §4.3, Figure 2):

| bucket | targets | reading |
|---|---|---|
| **Recall-gated by construction** | `brotlid`, `mailauth` | pass ⇒ recall regardless of the screen (offline RFC specs; [finding 02](02_recall_and_verifiability.md)) |
| **Non-memorized AND solved** — the clean signal | `nonogrid`, `tssql`, `hexyl`, `bitwise`, `texmacros`, `private_S` | genuine reconstruction-from-behavior evidence — but all small/medium, simple-logic tools (a nonogram solver, CSV-SQL, a hex viewer, a bitwise calculator, TeX macro expansion) |
| **Non-memorized AND unsolved** | `giac_subset` | the one hard non-memorized target was not solved |
| **Memorized AND solved** — recall not excludable | `uuidparse`, `qsv_select`, `jq_simple`, `numfmt`, `gron`, `cal`, `gotree`, `wren_cl`, `pkl`, `private_M`, … | the bulk of the headline 56%; MirrorCode's own method cannot tell reconstruction from recall here |
| **Memorized AND unsolved** | `sed`, `ruff`, `cprepro`, `private_L` | memorization is necessary-not-sufficient — the authors' valid partial point |

## The bound

- **Contamination breadth: 68%.** 17 of 25 targets are memorized on MirrorCode's own screen. Whatever
  the headline measures, two-thirds of its targets are ones the model has partly seen.
- **Clean signal ≤ 32%, and in practice ~6 small tools.** The uncontaminated measurement of
  "reconstruction from behavior alone" is confined to the ≤8 non-memorized targets, of which ~6 were
  solved — all small-to-medium, simple-algorithm programs. That is real and creditable evidence, and
  it is a much narrower claim than "AI can rebuild entire programs from behavior alone."
- **The memorized-and-solved targets drive the number and are indistinguishable from recall** under
  MirrorCode's own instrument.

We deliberately do **not** publish a single "X% of the score is recall" point estimate: the raw
per-target solve data is not released, so a precise effect size would be fabricated. The defensible,
receipt-backed statement is the bound above — and the meta-finding that MirrorCode measured exactly
what would settle the question and left it unreported.

## What would settle it (and MirrorCode could)

Fill the 2×2. Publish per-target memorization score × per-target 100%-solve rate, and report the
difference in solve rate between memorized and non-memorized targets, stratified by size bucket to
control for the fame↔simplicity confound. That is one table from data they already have. Until then,
"not solely driven by memorization" is an assertion, and the reproducible facts bound the recall-free
signal to a handful of small programs.

*Sources: MirrorCode [arXiv:2606.30182](https://arxiv.org/abs/2606.30182) §3.1, §4.3, §B.3 (Fig 9),
Fig 2; [github.com/epoch-research/MirrorCode](https://github.com/epoch-research/MirrorCode) (no screen
or results data). Memorization classification read from Figure 9; borderline targets flagged.*
