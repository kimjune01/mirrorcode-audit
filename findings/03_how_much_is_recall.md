# 03 — How much of the score is recall?

For ProgramBench the answer to "does it measure what it claims?" was *not really* — it measured recall.
MirrorCode gives us its own data to ask the same question of itself. The honest answer is that the
recall share *cannot* be estimated from what MirrorCode released — even though MirrorCode ran the
measurement that would settle it and did not publish the join.

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
but **no memorization-screen scores and no per-run solve results** — inspecting the repo
(as of 2026-07-17; pin the MirrorCode commit to re-verify), the only `results` path is a single
`tssql` test fixture, not run outputs. So MirrorCode's own
contamination check is not reproducible — the reader must take "not solely memorization" on faith.

## What the figures show (and what they cannot)

Reading Figure 9 as a binary (Opus-4.7 bar above vs. within/below the baseline band — robust even
where exact heights are not), the **8 non-memorized** MirrorCode targets are approximately:

`tssql`, `hexyl`, `private_S`, `bitwise`, `texmacros`, `nonogrid`, `giac_subset`, and one borderline
(`choose`). The other 17 are screen-positive. (Solve status below is read from §3.1/§4.3 text where stated
and Figure 2 otherwise; per-cell reads from Figure 2 are approximate, so target *placements* are
illustrative — the reading that follows does not depend on any single cell.)

| bucket | targets | reading |
|---|---|---|
| **Recall-gated by construction** | `brotlid`, `mailauth` | pass ⇒ recall regardless of the screen (offline RFC specs; [finding 02](02_recall_and_verifiability.md)) |
| **Non-memorized AND solved** — the clean signal | `nonogrid`, `tssql` (both named in §4.3 as solved-though-not-memorized), `hexyl`, `bitwise` (small non-memorized S-bucket tools; `private_S`, `texmacros` probably) | genuine reconstruction-from-behavior evidence — but all small/medium, simple-logic tools (a nonogram solver, CSV-SQL, a hex viewer, a bitwise calculator) |
| **Non-memorized AND unsolved** | `giac_subset` | the hardest non-memorized target was not solved |
| **Screen-positive AND solved-or-near** — recall not excludable from released data | `uuidparse`, `qsv_select`, `jq_simple`, `numfmt`, `gron`, `cal`, `wren_cl`, `gotree` (near-perfect, 2000/2001), `private_M`, … | the bulk of the headline; MirrorCode's own method cannot tell reconstruction from recall here |
| **Screen-positive AND unsolved** | `sed`, `ruff`, `cprepro`, `pkl`/`private_L` | screen-positive did not guarantee a solve — the authors' valid partial point |

## What the evidence supports (and what it does not)

Precision matters here, so state each claim at exactly its strength:

- **Screen-positive prevalence: 68%.** 17 of 25 targets showed similarity evidence consistent with
  memorization on MirrorCode's own screen (§B.3). This is a *target count*, not a fraction of the score
  caused by recall — the screen measures similarity when a model is *prompted* to reproduce named
  upstream functions, which is evidence of exposure, not proof that a solving run used that memory.
- **Two targets are recall by construction**, independent of any screen: `brotlid` and `mailauth`
  ([finding 02](02_recall_and_verifiability.md)). For these, a pass ⇒ recall.
- **The recall share of the 56% cannot be estimated from released data.** This is *not* a "≤32% clean"
  bound: a screen-positive target can still be solved by genuine reconstruction, and a screen-negative
  target can still involve undetected memorization. Screen positivity neither includes nor excludes
  clean reconstruction, and the join needed to decompose the score is unpublished. So the honest
  statement is: only 8 targets were *not* flagged by the screen (of which the paper names `nonogrid`
  and `tssql` as solved-yet-unflagged), and without the per-target screen×solve join or an
  intervention, memorization's contribution to the headline is unquantifiable — by MirrorCode or by us.

We deliberately do **not** publish a single "X% of the score is recall" figure, and we do **not** claim
a bound: the raw per-target solve data is not released, so either would be fabricated. The
receipt-backed finding is the meta-finding — MirrorCode ran exactly the measurement that would settle
the question (the screen), has the solve rates, and never reported the association or released the data
to compute it.

## What would settle it (and MirrorCode could)

Fill the 2×2. Publish per-target memorization score × per-target 100%-solve rate, and report the
difference in solve rate between memorized and non-memorized targets, stratified by size bucket to
control for the fame↔simplicity confound. That is one table from data they already have. Until then,
"not solely driven by memorization" is an assertion the released data neither confirms nor refutes.

*Sources: MirrorCode [arXiv:2606.30182](https://arxiv.org/abs/2606.30182) §3.1, §4.3, §B.3 (Fig 9),
Fig 2; [github.com/epoch-research/MirrorCode](https://github.com/epoch-research/MirrorCode) (no screen
or results data). Memorization classification read from Figure 9; borderline targets flagged.*
