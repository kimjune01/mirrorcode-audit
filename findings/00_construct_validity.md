# 00 — Does MirrorCode measure what it says it measures?

This is the whole audit in one question. MirrorCode is a measurement instrument; every other finding
here is evidence about whether its number means what the title claims.

## What it says it measures

- *"MirrorCode: AI can rebuild entire programs from behavior alone"* (paper title)
- *"What's the largest software project AI can complete on its own?"* (site)
- *"AI models are tasked with reimplementing an entire program end-to-end, without access to the
  original source code"* — pitched against human labor of *"weeks"* to *"months."*

The claimed construct: **autonomous reconstruction of whole programs from behavior**, as a measure of
frontier AI doing what would take a human engineer weeks-to-months of software work.

## What it actually measures

The metric — byte-exact match of `(stdout, stderr, exit)` against a captured reference on held-out
tests, 100% to count — measures a real capability, but four gaps separate it from the claimed
construct. Each is evidenced elsewhere in this repo or in MirrorCode's own paper.

| # | The metric actually rewards… | …not the claimed construct, because | evidence |
|---|---|---|---|
| 1 | **Reimplementation from a working oracle** | readers of "largest project a human would take months on" picture *creation*; reimplementing from a live reference is ~an order of magnitude cheaper (MirrorCode's own human baseline: ~48 h for a ~2k-LoC task vs ~370–820 h of original creation for a whole program that size) | [finding 01](01_human_labor.md) |
| 2 | **Recall of specific, famous public programs** | "from behavior alone" is confounded: MirrorCode's own memorization screen flags **17 of 25 targets** (p<0.05); the uncontaminated signal is bounded to ≤8 targets, ~5 small tools; `brotlid`/`mailauth` are recall-gated | [finding 03](03_how_much_is_recall.md), [02](02_recall_and_verifiability.md) |
| 3 | **Passing byte-exact I/O tests** | "rebuild entire programs" overstates it — the paper concedes the produced code is piecemeal, monolithic, and *"would not be merged into existing repositories"* (§4.3) | MirrorCode §3.5, §4.3 |
| 4 | **Reproducing a scoped slice** | several "programs" are a small part of a large repo (`cal`/`uuidparse` inside util-linux; `bib2json` = one format pair of pandoc; `qsv select`; a jq subset), so "entire program" is literally not the unit tested | [finding 01](01_human_labor.md) table; §2.3 |

## Verdict

MirrorCode measures, precisely: *can a frontier model — aided by memorization of these specific public
programs — reproduce the byte-exact I/O of a **scoped reimplementation** task, given a **working
reference oracle** and documentation, offline.* That is a real, hard, and interesting capability, and
the instrument for it is unusually well-built (isolated scoring, enforced execute-only reference,
disclosed COI — [finding 02](02_recall_and_verifiability.md)).

It is **not** what the title and site say. "The largest software project AI can complete on its own,"
measured against weeks-to-months of human labor, equivocates between the cheap reimplementation task
the metric scores and the expensive creation task the framing evokes (gap 1), while "from behavior
alone" is not separable from recall for two-thirds of the targets (gap 2). The construct is narrower
than the claim, and narrower in exactly the direction that makes the headline more impressive.

This is a construct-validity gap, not a grading bug — the same shape as the ProgramBench finding
([*ProgramBench Measures Recall*](https://june.kim/programbench-measures-recall)): the number is sound
on what it checks, and the checking is not what the title claims. The pattern is an academic
bait-and-switch — one question posed ("can AI build whole programs autonomously?"), a different one
answered ("can it reproduce scoped I/O from an oracle, partly from memory?").

**Credit where due.** Unlike a saturated benchmark, MirrorCode has genuine range: 8 of 25 targets were
never solved to 100% and the Large targets sit near 0%, so the instrument still discriminates at the
frontier rather than topping out. The scoring isolation is real, the execute-only reference is
enforced, and the COI is disclosed. The critique is of the *claim placed on the number*, not of the
engineering under it.

## The contract, clause by clause

Running the [*How to Audit a Benchmark*](https://june.kim/how-to-audit-a-benchmark) checklist against
MirrorCode, so the coverage is comprehensive rather than only the two deep-dives:

| clause | check | verdict on MirrorCode |
|---|---|---|
| **spec** | is the graded value pinned by the materials the solver gets? | **partial** — visible tests pin scope well, but the paper's own failure cases (`bib2json` `useprefix` default, `sed --posix`) are underdetermination charged to the model |
| **oracle** | classify each exact-value assertion by how a source-blind solver gets it | **breaks on 2+ targets** — `brotlid`, `mailauth` are recall-only ([finding 02](02_recall_and_verifiability.md)) |
| **frame** | does the grader guard what the task never named? | **strong** — I/O-only oracle + enforced execute-only reference; the Gemini binary-wrap cheat is defeated structurally (§D) |
| **gold** | does the reference pass its own tests? | trivially yes — the reference *is* the oracle (self-capturing by construction); apt for an I/O bench, but see oracle |
| **score** | recompute the headline; is it comparing like with like? | **caveat** — Gemini run Python-only vs Opus all-6-languages; L targets single-language; disclosed in text, flattened in the 3-bar figure |
| **decay** | what survives publication? | **weak** — targets are famous public programs, 17/25 memorized; the recall-free signal is bounded to ~5 small tools ([finding 03](03_how_much_is_recall.md)); canary strings help detect, not prevent |
| **construct** | does it measure what it says? | **no, as titled** — see verdict above |

## Reproduce / re-derive

- Human-labor anchors: `python3 scripts/human_labor.py` → `data/human_labor.json`.
- Recall witnesses: read `mc/brotlid/…` and `mc/mailauth/…` test assertions in
  [`epoch-research/MirrorCode`](https://github.com/epoch-research/MirrorCode) and classify by the
  five-class rule.
- Every claim traces to a cited paper section, a public repo file, or a re-runnable script.
