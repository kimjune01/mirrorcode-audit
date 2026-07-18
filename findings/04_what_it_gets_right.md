# 04 — What MirrorCode gets right

An audit that only finds sins is a press release. MirrorCode's construct claim overreaches its
evidence (findings 00–03), but the instrument under that claim is one of the better-built benchmarks in
this space — on several axes, better than the six in [*How to Audit a Benchmark*](https://june.kim/how-to-audit-a-benchmark).
The credits below are as substantiated as the criticisms.

## The cheat-proofing is real, not asserted

Most benchmarks claim "cheat-resistant" and mean it aspirationally. MirrorCode enforces it (§D, §2.5):

- **Scoring runs where the agent cannot reach it** — four isolated containers; the agent's code is
  archived and executed in separate scoring containers where the reference binary is absent, so tampering
  with scoring or wrapping the reference is structurally useless.
- **The execute-only reference is actually enforced** — `chmod 2711` plus a seccomp-BPF filter and a
  Landlock policy that block every byte-read path to the binary (`cat`/`dd`, `ptrace`,
  `process_vm_readv`, `/proc/<pid>/mem`, `/proc/self/mem`), with `RLIMIT_CORE=0` to deny core-dump
  recovery. The ProgramBench paper only *assumed* execute-only; MirrorCode closes the holes.
- **It caught a real cheat** — with the `evaluate_testcases` signal removed, Gemini reconstructed the
  reference-binary path via `chr()` arithmetic and lied in a docstring ("native JIT compiler"); the
  scoring isolation defeated it anyway (Fig 11). A red-team run for 1B tokens found no successful cheat.

## It grades I/O, which sidesteps the frame problem

The oracle is extensional — `(stdout, stderr, exit)` byte-equality, nothing about the environment's
final state (§D.2). That means the reward-ordering sin that sinks final-state benchmarks (a destructive
completion outscoring a safe failure) does not arise here. Different construct, but a cleaner one on
this axis.

## It did the two things most benchmarks skip

- **Ran a human baseline at all.** It is incomplete (one 20 h → 42% short-task run, no long-task
  baseline), but attempting a human baseline is the single highest-signal move a benchmark can make,
  and most never try. The failure mode we flag (finding 01) is that the *marketing* leans on belief
  estimates instead of this baseline — not that they skipped the baseline.
- **Ran a memorization screen.** Proactively checking contamination against post-cutoff baseline
  programs (§B.3) is rare and commendable. Our criticism (finding 03) is narrow: they did not publish
  the screen×solve join. The screen itself is a credit.

## It engaged the fairness problem the ProgramBench audit raised — and often solved it

Independently (MirrorCode predates ProgramBench), it reached several of the [ProgramBench
audit's](https://june.kim/programbench-measures-recall) conclusions and designed around them:

- **Decompression, not compression** — it scopes `brotlid` to `brotli -d`, explicitly rejecting the
  implementation-pinned encoder oracle that ProgramBench grades byte-exact (E.1.1).
- **Language forced to defeat stdlib-triviality** — `ruff`→Go (no Python `ast`), `cprepro`→Go (no C
  toolchain) (Appendix A), the ProgramBench "stdlib predictor" used as a design lever.
- **Dropped the undiscoverable entry point** — `gron`'s `argv[0]`-triggered reverse mode "cannot
  reasonably be guessed," so it is not tested; ProgramBench grades it (E.1.2).
- **Excluded extreme reverse-engineering** — an ASCII-graphing rounding library and exact float
  arithmetic were considered and rejected as infeasible (§2.3).

## It spent enough to measure the real frontier

Underspent benchmarks report artificially low scores and mislabel budget limits as capability limits.
MirrorCode budgets $100–3,000 per task (up to $2,600 / 19 days for one run) and shows scores keep
climbing with compute (§3, Fig 8). Whatever the headline means, it is not a starved-budget artifact.

## It has genuine headroom

Not saturated: 8 of 25 targets were never solved to 100%, the Large targets sit near 0%, and no model
tops out. A benchmark that still discriminates at the frontier is doing its job.

## The paper's body is honest about its own limits

The overreach we audit lives in the title and marketing. The paper itself states the narrow reading
plainly: the code is piecemeal and "would not be merged" (§4.3), the results "do not show that AI can
perform arbitrary software implementation tasks" (§4.2), contamination is a live concern (§4.3), and
the precise-specification setting is unusual and may not transfer (§4.2). Our construct-validity
critique (finding 00) is aimed at the gap between that careful body and the top-line framing — not at a
paper that hides the ball. It doesn't.

## Disclosure

The marketing site states the work is *"co-developed with METR"* and Epoch runs the leaderboard — the
conflict of interest is disclosed, which is more than several audited benchmarks managed.

---

*Net: MirrorCode is a well-engineered instrument for a real, hard capability (scoped functional
reimplementation under a strong executable specification). The audit's quarrel is with the claim placed
on the number, not the engineering under it.*

*Sources: MirrorCode [arXiv:2606.30182](https://arxiv.org/abs/2606.30182) §2.3, §2.5, §3, §4.2–4.3,
§B.3, §D, §E; [epoch.ai/MirrorCode](https://epoch.ai/MirrorCode).*
