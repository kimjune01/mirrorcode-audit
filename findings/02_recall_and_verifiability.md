# 02 — Recall witnesses and verifiability

## Recall: the ProgramBench barrier survives MirrorCode's better engineering

MirrorCode grades byte-exact output against a captured reference — the same pseudo-oracle the
[ProgramBench audit](https://june.kim/programbench-measures-recall) analyzed. Its selection criteria
deliberately exclude "extreme reverse-engineering" targets, which removes *most* recall-only programs.
But two survive, both flagged by the ProgramBench five-class rule (a graded value is *recall-only*
when it is the output of a function no source-blind, offline solver can reproduce from feasible I/O —
a hash, cipher, codec, or compressor whose specification is withheld and unfetchable):

| target | recalled function | why it is recall-only |
|---|---|---|
| **brotlid** | Brotli decoder | Decoding a bundled `.br` stream to exact bytes requires the RFC-7932 decoder *and its 122 KB static dictionary*, which are not derivable from a few hundred decompression I/O examples and are not in the bundled docs. |
| **mailauth** | DKIM/DMARC/SPF verify | Matching the reference requires RSA/Ed25519 verification, SHA-256, and RFC-6376 canonicalization — all offline spec knowledge. It is the target Opus 4.7 scored *worst* on. |

MirrorCode engages this directly (Appendix E.1.1) and defends `brotlid` on the grounds that
decompression is *"fully determined by the documented format."* That conflates two things the
ProgramBench audit separates: *determined by RFC 7932* (true) and *determined by the **bundled**
documentation* (false — the bundle is `brotli --help`, which contains neither the bit-level format nor
the static dictionary). Determinacy is not reconstructability from the artifact; the specification is
exactly what a no-internet solver cannot reach. `brotlid` is a recall witness.

MirrorCode's own **memorization screen** (§B.3, Figure 9) is corroborating: it finds evidence of
training-data memorization for **17 of 25 targets** (p<0.05), with `brotlid` and `wren_cli` among the
highest. So for the recall-gated and memorized targets, a passing score measures recall of a published
algorithm or a famous program, not reconstruction — the ProgramBench thesis, on MirrorCode's own data.

### Convergence: MirrorCode independently rediscovered three ProgramBench-audit findings

It reads like a benchmark built by people who had internalized the failure modes:

1. **Implementation-pinned oracle → they chose decompression, not compression.** They scope `brotlid`
   to `brotli -d` and note ProgramBench grades the encoder byte-exact (`test_encoder_paths.py`,
   45 assertions), which pins one of many valid outputs (E.1.1).
2. **The stdlib-triviality predictor → they force the language.** `ruff` is run in Go "because the
   availability of the Python `ast` package would circumvent the need to write a Python parser";
   `cprepro` in Go because it ships no C toolchain (Appendix A). This is the ProgramBench audit's
   "implementation language's standard library" predictor, used as a design lever.
3. **The undiscoverable-entry-point class → they drop the exact case ProgramBench grades.** For `gron`
   they note the `argv[0]`-ends-in-`ungron` reverse-mode behavior "cannot reasonably be guessed" and
   do **not** test it, while ProgramBench does (E.1.2). Same bright line, same exclusion.

## Verifiability of the marketing claims

Split decision, along the line between the instrument and the story told about it.

**Verifiable (the instrument).** The repo ([`epoch-research/MirrorCode`](https://github.com/epoch-research/MirrorCode),
MIT) ships the Inspect harness, 22 of 25 public tasks, the gold outputs (`data/gold_outputs/*.jsonl`),
prebuilt container images, and canary strings. A stranger can rerun the benchmark and re-derive the
grading — better than most benchmarks. The recall triage above is runnable directly on it: `brotlid`
ships its `.br` fixtures, `mailauth` ships `source_test_suite/`. The container-level cheat-proofing
(§D: four isolated containers, seccomp-BPF + Landlock + `RLIMIT_CORE=0` blocking every byte-read path
to the execute-only reference) is real and enforced, not asserted — the *"cheat-resistant by design"*
claim is fair.

**Not falsifiable as stated (the story).**

- **Score receipts don't exist publicly.** The leaderboard numbers (56%) and the anecdotes
  (*"14 hours, $251"* for gotree; *"$2,600, 19 days"* for the largest task) ship no per-trial
  trajectory or log. Runs used METR's external Hawk orchestrator; outputs are not in the repo. You can
  only "verify" by re-spending $100–3,000 per task on a stochastic rerun.
- **Human-time claims are unmeasured belief** (finding 01): every human-effort figure is *"we
  believe,"* and the one real human baseline (20 h → 42%) is left in a footnote, off the marketing
  page. Making them falsifiable would mean publishing the per-trial trajectories and replacing "we
  believe … weeks/months" with the measured baseline, scoped to creation vs reimplementation.
- **The title claim overreaches.** *"AI can rebuild entire programs from behavior alone"* is
  half-confounded: 17/25 targets are memorized, so "from behavior alone" is not cleanly separable from
  recall, and the paper concedes the produced code is piecemeal and would not merge.

The conflict of interest is at least disclosed: the site states MirrorCode is *"co-developed with
METR,"* and Epoch AI runs the leaderboard.

*Sources: MirrorCode [arXiv:2606.30182](https://arxiv.org/abs/2606.30182) (§2.2, §2.5, §B.3, §D, §E);
[epoch.ai/MirrorCode](https://epoch.ai/MirrorCode); [github.com/epoch-research/MirrorCode](https://github.com/epoch-research/MirrorCode).*
