# 01 — Human labor is falsifiable, and the framing equivocates

## The claim under test

MirrorCode's marketing and paper carry the capability story on human-time estimates, all hedged
*"we believe"*:

- *"What's the largest software project AI can complete on its own?"* (site title)
- *"We believe a human engineer without AI would take months to solve the most complex MirrorCode tasks."*
- *"We believe this same task [gotree] would take a human engineer without AI assistance 2–17 weeks."*
- *"Reimplementing entire programs is extremely challenging for human software engineers."*
- contrasted with: Opus 4.7 *"solved it in 14 hours, costing $251."*

These estimates are unmeasured belief. But the targets are **real open-source programs**, so the
human labor embodied in them is a matter of public record. We anchor it two ways, both external to
us.

This is not a peripheral nitpick. The human-time comparison *is* MirrorCode's headline product — the
site asks *"What's the largest software project AI can complete on its own?"* and answers in units of
human weeks and months. A benchmark's central marketed quantity is exactly the thing an audit must
put on a falsifiable footing; if the number that carries the story is belief rather than measurement,
that is the finding, not a footnote.

## Method

**Anchor A — the creation record (descriptive facts, then a heuristic).** For each target's upstream
repo we pull the public git history via the GitHub API. The **hard, falsifiable facts** are the counts
themselves: each program is hundreds-to-tens-of-thousands of commits, over years of calendar time, by
many contributors (table below). That alone refutes "weekend program."

Turning commits into hours needs a rate, and here we are explicit that this is a **heuristic, not a
validated effort model.** We borrow the one published, neutral statistic available — Kolassa, Riehle &
Salim, *The Empirical Commit Frequency Distribution of Open Source Projects* (WikiSym+OpenSym 2013,
arXiv:1408.4978), Table 1: the **median interval between two consecutive commits of the same committer
is 1.666 h** — and treat one commit as ≈1.666 h of work: `creation_hours ≈ commits × 1.666 h`. Two
honest caveats, because this is the audit's own construction, not a source's: (i) 1.666 h is *elapsed
time between commits*, not measured effort — it double-counts short breaks and misses design/review
that leaves no commit; (ii) it is applied to the **current default branch**, not the pinned upstream
version MirrorCode tested (§5 of the script notes this). So the person-hour figures are an
order-of-magnitude illustration; the load-bearing claim is the descriptive record, not the constant.

**Anchor B — reimplementation.** MirrorCode's task is not to *create* a program but to *reimplement*
one from a working reference. Its own paper gives a human baseline (footnote 7): a skilled SWE **did
not finish a ~2,000-LoC task in 20 hours, passing 42% of tests.** So reimplementation of a ~2k-LoC task
costs **at least 20 h**; a linear extrapolation puts full completion near ~48 h (and, since the tests
left are usually the harder ones, ~48 h reads as a floor, not a ceiling). Either way it is **days, not
tens of weeks** — the correctly-scoped human number for what MirrorCode actually measures.

## Anchor A: original creation embodied in the targets

Whole-program targets, where the upstream repo's history is a fair anchor for the task (counts as of
2026-07-17, live and re-derivable via `scripts/human_labor.py`; they drift slowly):

The conversion is explicit in the last two columns: **commits × 1.666 h = dev-hours**, then **÷ 40 h =
dev-weeks**. The first three columns are the hard record; the last two are the heuristic.

| target | upstream repo | commits | span | contributors | × 1.666 h = dev-hours | ÷ 40 = dev-weeks |
|---|---|---|---|---|---|---|
| choose | theryangeary/choose | 164 | 6.8y | 7 | 273 h | ~6.8 |
| mailauth | stalwartlabs/mail-auth | 193 | 3.7y | 13 | 322 h | ~8.1 |
| gron | tomnomnom/gron | 223 | 12.7y | 23 | 372 h | ~9.3 |
| nonogrid | tsionyx/nonogrid | 400 | 2.8y | 2 | 666 h | ~16.6 |
| hexyl | sharkdp/hexyl | 490 | 7.4y | 61 | 816 h | ~20.4 |
| gotree | evolbioinfo/gotree | 836 | 10.0y | 7 | 1,393 h | ~34.8 |
| pkl | apple/pkl | 851 | 2.4y | 80 | 1,418 h | ~35.5 |
| wren_cli | wren-lang/wren-cli | 1,703 | 10.4y | 94 | 2,837 h | ~70.9 |
| brotlid* | google/brotli | 1,538 | 12.8y | 131 | 2,562 h | ~64.0 |
| ruff* | astral-sh/ruff | 16,217 | 3.9y | 927 | 27,018 h | ~675 |

<sub>*`brotlid` (decoder only) and `ruff` (linter only) test part of the repo, so their whole-repo row over-states the tested slice; both are excluded from the median below.</sub>

**Median of the eight pure-`whole` targets ≈ 18.5 developer-weeks of original creation** (the bottom
two rows, `brotlid` and `ruff`, are excluded from that median — MirrorCode tests only part of `brotli`
and most of `ruff`). Spread over years of calendar time and many contributors, these are not weekend
programs.

Scoped targets, where MirrorCode tests a small slice of a much larger repo — the whole-repo count
**over-states** the labor and is shown only to mark the trap:

| target | upstream repo | commits | note |
|---|---|---|---|
| bitwise | mellowcandle/bitwise | 264 | expression subset |
| jq_simple | jqlang/jq | 1,929 | a documented subset of jq |
| bib2json | jgm/pandoc | 19,099 | one format pair of all of pandoc |
| qsv_select | dathere/qsv | 17,728 | one subcommand of a 40+ command toolkit |
| cal / uuidparse | util-linux/util-linux | 22,949 | two tiny tools inside 33 years of util-linux |

For these, the upstream number is meaningless as a per-task anchor; the honest figure needs
per-directory history, which we do not claim here.

## The finding: four different "how long?" numbers, slid together

At least four "how long would a human take" numbers attach to essentially one task. They measure
different things, and MirrorCode's framing slides between them. Worked for **gotree** — the one target
with both a stated human estimate and a reported AI run:

| "how long?" | value | what it actually measures | source |
|---|---|---|---|
| **Original creation** | ~1,393 dev-hours (~35 dev-weeks) | building gotree from scratch, over 10 years and 836 commits | Anchor A: git history × 1.666 h (heuristic) |
| **MirrorCode's belief** | *"2–17 weeks"* | four contributors' guess at reimplementation effort (~7× spread) | MirrorCode paper/site (untested) |
| **Measured reimplementation** | ≥ 20 h; ~48 h to 100% (for a ~2k-LoC task; gotree is 16k) | a real SWE reimplementing from the reference binary | MirrorCode footnote 7 (20 h → 42%) |
| **AI (Opus 4.7)** | 14 h, $251, passed 2000/2001 tests | the benchmark run | MirrorCode site |

The takeaway, read straight off the table:

- **Creation and reimplementation differ by ~an order of magnitude.** For a ~2k-LoC whole program,
  creation is ~370–820 h (`gron` ~372, `hexyl` ~816) while MirrorCode's own reimplementation baseline
  is ~48 h. Reimplementing from a working reference is the far cheaper task.
- **The marketing evokes the top row; the benchmark measures the third.** "A human would take
  weeks/months" reads as *creation*; the task posed is *reimplementation from an oracle*. The belief
  row sits between the two falsifiable numbers, untested.
- **The AI row looks miraculous only against the wrong comparison** — 14 h vs ~35 creation-weeks, not
  14 h vs a ~48 h reimplementation — and it is confounded: MirrorCode's own screen is **screen-positive
  on 17 of 25 targets** (finding 02), and gotree's run *passed 2000/2001*, not a strict 100%.

## What this does and does not show

- It does **not** claim MirrorCode's tasks are easy. Reimplementation-to-byte-exact is hard, and their
  own human passed only 42% in 20 h.
- It **does** show the human-labor claim is *checkable*, and that checking it separates two quantities
  MirrorCode's framing blurs — the creation record embodied in the target (large, on the public record) and the
  reimplementation effort the benchmark measures (small, from MirrorCode's own baseline). The
  belief-estimate in between is the marketing.
- Anchor A's person-hours are an order-of-magnitude illustration from a single heuristic rate; they
  fix scale, not any one program's true cost. The descriptive record (commits, years, contributors) is
  the falsifiable part, not the hours.

*Data: `data/human_labor.json`. Re-derive: `python3 scripts/human_labor.py` (needs `gh`).*
*Conversion rate (heuristic): Kolassa, Riehle & Salim 2013, [arXiv:1408.4978](https://arxiv.org/abs/1408.4978), median inter-commit interval — an elapsed-time statistic, not a validated effort model.*
