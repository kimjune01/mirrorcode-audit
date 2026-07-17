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
human labor embodied in them is a public, falsifiable fact. We anchor it two ways, both external to
us.

This is not a peripheral nitpick. The human-time comparison *is* MirrorCode's headline product — the
site asks *"What's the largest software project AI can complete on its own?"* and answers in units of
human weeks and months. A benchmark's central marketed quantity is exactly the thing an audit must
put on a falsifiable footing; if the number that carries the story is belief rather than measurement,
that is the finding, not a footnote.

## Method

**Anchor A — original creation.** For each target's upstream repo we pull the public git history
(merged PRs, total commits, contributors, calendar span) via the GitHub API, then convert commits to
developer-hours at a **published, neutral** rate: Kolassa, Riehle & Salim, *The Empirical Commit
Frequency Distribution of Open Source Projects* (WikiSym+OpenSym 2013, arXiv:1408.4978), Table 1 —
the **median interval between two consecutive commits of the same committer is 1.666 h**. (The paper's
*mean* interval is 3.206 days, dominated by idle gaps; mean×commits would measure calendar time, not
effort, so the median is the right active-work proxy.) `creation_hours ≈ commits × 1.666 h`. This is
an order-of-magnitude anchor: it excludes non-committing work (design, review), so it under-counts
total effort, and charges a full interval to rapid-fire commits, so it over-counts bursts.

**Anchor B — reimplementation.** MirrorCode's task is not to *create* a program but to *reimplement*
one from a working reference. Its own paper gives a human baseline (footnote 7): a skilled SWE **did
not finish a ~2,000-LoC task in 20 hours, passing 42% of tests.** So reimplementation of a ~2k-LoC task
costs **at least 20 h**; a linear extrapolation puts full completion near ~48 h (and, since the tests
left are usually the harder ones, ~48 h reads as a floor, not a ceiling). Either way it is **days, not
tens of weeks** — the correctly-scoped human number for what MirrorCode actually measures.

## Anchor A: original creation embodied in the targets

Whole-program targets, where the upstream repo's history is a fair anchor for the task:

| target | upstream repo | commits | span | contributors | creation (Kolassa) |
|---|---|---|---|---|---|
| choose | theryangeary/choose | 164 | 6.8y | 7 | ~6.8 dev-weeks |
| mailauth | stalwartlabs/mail-auth | 193 | 3.7y | 13 | ~8.1 dev-weeks |
| gron | tomnomnom/gron | 223 | 12.7y | 23 | ~9.3 dev-weeks |
| nonogrid | tsionyx/nonogrid | 400 | 2.8y | 2 | ~16.6 dev-weeks |
| hexyl | sharkdp/hexyl | 490 | 7.4y | 61 | ~20.4 dev-weeks |
| gotree | evolbioinfo/gotree | 836 | 10.0y | 7 | ~34.8 dev-weeks |
| pkl | apple/pkl | 851 | 2.4y | 80 | ~35.5 dev-weeks |
| wren_cli | wren-lang/wren-cli | 1,703 | 10.4y | 94 | ~70.9 dev-weeks |
| brotlid | google/brotli | 1,538 | 12.8y | 131 | ~64.0 dev-weeks (decoder is a *part* of this) |
| ruff | astral-sh/ruff | 16,216 | 3.9y | 927 | ~675 dev-weeks (linter is *most* of this) |

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

## The finding: the two anchors bracket the belief, and differ by ~an order of magnitude

Take a ~2,000-LoC *whole* program: `gron` (2.3k LoC, 223 commits ≈ **372 h** of original creation by
Anchor A) or `hexyl` (1.8k LoC, 490 commits ≈ **816 h**). MirrorCode's *own* reimplementation baseline
for a task that size is **~48 h** — days (Anchor B). So **reimplementing from a working reference is
roughly an order of magnitude cheaper than original creation** (the exact ratio, ~8–17× here, depends
on the program; it is illustrative, not a constant). That gap is the whole story:

- **Readers of the marketing picture creation** — "a human would take weeks/months" evokes building
  the program. Anchor A confirms these programs *did* take tens of developer-weeks to create.
- **The benchmark measures reimplementation** — the far cheaper task. Anchor B (MirrorCode's own data)
  puts a ~2k-LoC reimplementation at ~1.2 weeks, not weeks-to-months.
- **MirrorCode's estimates ("2–17 weeks", "months") sit between the two anchors and are unfalsifiable
  belief.** The falsifiable numbers are Anchor A (creation, from public history) and Anchor B
  (reimplementation, from MirrorCode's own baseline). Neither supports the headline as framed: the
  large number is the wrong task, and the right-task number is a week.
- **The "AI in 14 h" contrast is further confounded**: MirrorCode's own memorization screen flags
  **17 of 25 targets** as showing training-data memorization (see finding 02), so the AI is partly
  recalling these specific, famous programs rather than reconstructing them.

## What this does and does not show

- It does **not** claim MirrorCode's tasks are easy. Reimplementation-to-byte-exact is hard, and their
  own human passed only 42% in 20 h.
- It **does** show the human-labor claim is *checkable*, and that checking it separates two quantities
  MirrorCode's framing blurs — the creation effort embodied in the target (large, falsifiable) and the
  reimplementation effort the benchmark measures (small, falsifiable from their own baseline). The
  belief-estimate in between is the marketing.
- Anchor A is order-of-magnitude (a single published constant across all repos); it is meant to fix
  scale, not to price any one program to the hour.

*Data: `data/human_labor.json`. Re-derive: `python3 scripts/human_labor.py` (needs `gh`).*
*Effort constant: Kolassa, Riehle & Salim 2013, [arXiv:1408.4978](https://arxiv.org/abs/1408.4978).*
