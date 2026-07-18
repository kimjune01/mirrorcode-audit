# MirrorCode audit

A re-runnable audit of [MirrorCode](https://arxiv.org/abs/2606.30182) (arXiv:2606.30182,
Adamczewski, Owen, Rein et al.; Epoch AI + METR), the benchmark that grades AI agents on
reimplementing whole CLI programs from an execute-only binary plus docs, byte-exact against
the reference. Marketing site: [epoch.ai/MirrorCode](https://epoch.ai/MirrorCode).

Companion to the [ProgramBench audit](https://github.com/kimjune01/program-bench-audit)
([*ProgramBench Measures Recall*](https://june.kim/programbench-measures-recall)). MirrorCode
is the same construct — reconstruct-a-program-from-behavior, graded by byte-exact-vs-reference —
built more carefully. This audit checks the claims that carry the marketing, using only public
artifacts.

## Findings

- **[00 — Does MirrorCode measure what it says it measures?](findings/00_construct_validity.md)** The
  capstone. The claimed construct is "autonomous reconstruction of whole programs from behavior,"
  pitched against weeks-to-months of human labor. What the metric actually rewards is scoped
  *reimplementation from a working oracle*, partly via *recall* of these specific public programs.
  Includes the full [*How to Audit a Benchmark*](https://june.kim/how-to-audit-a-benchmark)
  contract run clause-by-clause.

- **[01 — Human labor is falsifiable, and the framing equivocates](findings/01_human_labor.md).**
  MirrorCode's headline rests on *"we believe a human would take weeks / months."* The targets are
  real open-source programs, so their development history is a matter of public record: hundreds to
  tens of thousands of commits over years, by many contributors. As a rough heuristic (treating the
  published median inter-commit interval, Kolassa et al. 2013 = 1.666 h, as work-per-commit — an
  illustration, not a validated effort model), the whole-program targets come to a median of ~18
  developer-weeks of original creation.
  But MirrorCode's *own* human baseline shows reimplementation-from-a-working-reference costs
  **~48 h (~1.2 weeks)** for a ~2,000-LoC task — ~an order of magnitude cheaper than original creation. The marketing
  equivocates between the two: readers picture creation, the benchmark measures the cheaper
  reimplementation, and the "AI did it in 14 h" contrast (a gotree run that passed 2000/2001 tests, not a strict 100%) rides on 17/25 targets that are screen-positive for memorization.

- **[02 — Recall witnesses and verifiability](findings/02_recall_and_verifiability.md).**
  Two targets are recall-gated by the ProgramBench 5-class rule: **`brotlid`** (Brotli decompression;
  the decoder + static dictionary are RFC-7932 knowledge, offline-unfetchable) and **`mailauth`**
  (DKIM/DMARC crypto verification). MirrorCode's defense — decompression is *"fully determined by the
  documented format"* — conflates RFC 7932 with the *bundled* docs. Its own memorization screen flags
  17/25 targets. Separately: the **instrument** is genuinely verifiable (harness, tests, gold outputs,
  container images all public), but the **scores** ship no per-run receipts and the **human-time
  claims** are unmeasured belief.

- **[03 — How much of the score is recall?](findings/03_how_much_is_recall.md)** MirrorCode ran a
  memorization screen (17/25 flagged) but never reported the memorization×solve-rate association and
  ships no raw data to compute it — its "not solely memorization" defense is two anecdotes, an unfilled
  2×2. From the published figures: contamination breadth **68%**; the uncontaminated reconstruction
  screen flags 17/25 targets, but only two (`brotlid`, `mailauth`) are recall-gated *by construction*;
  the recall contribution to the score cannot be estimated from released data (the join isn't published).
  Reported as what the evidence supports, not a fabricated point estimate.

## Reproduce

```bash
python3 scripts/human_labor.py     # needs `gh` authenticated; writes data/human_labor.json
```

Every number in `findings/01` re-derives from `data/human_labor.json`, which re-derives from the
upstream repos' public git history via the GitHub API. The commit and branch counts are live GitHub facts; the
commit→hours conversion is a cited but heuristic rate (an inter-commit interval, not measured effort).

The upstream commit counts are live and drift slowly; the figures here are as of **2026-07-17** and
re-derive (order-of-magnitude stable) on any rerun. Quantitative claims trace to a cited paper section/figure, a
public repo file, or a re-runnable script; scope classifications and figure-reads are labeled as the
audit's own judgment, not receipts.

## What's here

- `scripts/human_labor.py` — pulls each target's upstream commit history and converts to a
  developer-effort anchor at a published rate.
- `data/human_labor.json` — the computed table (source of truth for finding 01).
- `findings/` — the write-ups.

## License

Network-copyleft, dual: **content** (`findings/`, `data/`, `README.md`) under **CC BY-SA-NS**
(CC BY-SA 4.0 + a Network Services clause); **code** (`scripts/`) under **AGPL-3.0-or-later**. See
[`LICENSE`](LICENSE). The MirrorCode paper and repository under audit are their authors' own work,
referenced by link and not redistributed here.
