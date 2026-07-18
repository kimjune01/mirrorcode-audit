# 06 — Per-target audit (all 25)

The ProgramBench-style read: every MirrorCode target given a verdict, against the public repo (`github.com/epoch-research/MirrorCode`, `mc/<target>/`) and the paper. 22 are public and read here; 3 are private and marked *unread*. Hand-adjudicated, since MirrorCode grades whole-task byte-exact I/O, so the recall call is per target, not per assertion.

## Headline counts

- **Recall by construction: 2/25** — `mailauth`, `brotlid`. The graded output is an un-inferable function's value (a codec, a cryptographic signature) no offline solver reproduces. Contrast ProgramBench's 21/201: MirrorCode's selection genuinely drained the recall surface — no hash, image, or media targets survive in the public set.
- **Scale/complex (reconstructable, but the coverage barrier bites): 7/25** — `giac_subset`, `texmacros`, `gotree`, `wren_cli`, `ruff`, `pkl`, `cprepro`. These are where solve rates fall (3.1, Fig 3): size and intricacy, not recall.
- **Clean/small (documented, reconstructable): 13/25**.
- **Screen-positive (Fig 9): 17** · **spec-underdetermined (paper's own 3.3): 3** (`hexyl`, `sed`, `bib2json`) · **unread (private): 3**.

## The table

| target | bkt | lang | LoC | recall class | screen+ | solved 100% | flags |
|---|---|---|---|---|---|---|---|
| qsv_select | S | Rust | 87k | **clean** | yes | yes | — |
| jq_simple | S | C | 21k | **clean** | yes | yes | — |
| gron | S | Go | 2.3k | **clean** | yes | yes | — |
| bitwise | S | C | 1.9k | **clean** | no | yes | — |
| hexyl | S | Rust | 1.8k | **clean** | no | yes | spec |
| uuidparse | S | C | 1.2k | **clean** | yes | yes | — |
| numfmt | S | C | 1.1k | **clean** | yes | yes | — |
| cal | S | C | 984 | **clean** | yes | yes | — |
| choose | S | Rust | 931 | **clean** | borderline | yes | — |
| private_S | S | ? | ? | **unread** | — | — | — |
| giac_subset | M | C++ | 31k | **scale** | no | no | — |
| texmacros | M | C | 18k | **scale** | no | yes | — |
| gotree | M | Go | 16k | **scale** | yes | near | — |
| mailauth | M | Rust | 16k | **recall** | yes | no | recall-witness |
| brotlid | M | C | 13k | **recall** | yes | no | recall-witness |
| wren_cli | M | C | 7.8k | **scale** | yes | yes | — |
| nonogrid | M | Rust | 5.9k | **clean** | no | yes | lang-forced |
| sed | M | C | 4.1k | **clean** | yes | yes | spec |
| tssql | M | Haskell | 2.1k | **clean** | no | yes | — |
| bib2json | M | Haskell | 2.0k | **clean** | borderline | yes | spec |
| private_M | M | ? | ? | **unread** | yes | — | — |
| ruff | L | Rust | 250k | **scale** | yes | no | lang-forced |
| pkl | L | Java | 61k | **scale** | yes | near | — |
| cprepro | L | C | 27k | **scale** | yes | no | lang-forced |
| private_L | L | ? | ? | **unread** | — | — | lang-forced |

## Recall witnesses (receipts)

**mailauth** — `mailauth arc-seal --key key.pem --domain gmail.com ...` -> stdout is an ARC-Seal header whose `b=` is an exact RSA-SHA256 signature; reproducing it needs RSA + SHA-256 + RFC-8617 canonicalization. gh api .../data/gold_outputs/mailauth.jsonl

**brotlid** — `brotli --base64 10x10y.compressed` (bundled Brotli blob) -> exact decompressed bytes; real-world .br fixtures (mc/brotlid/test_data/) need the RFC-7932 decoder + static dictionary. gh api .../data/gold_outputs/brotlid.jsonl

## Reading the columns

- **recall class** is the load-bearing verdict, read from the graded I/O (`data/gold_outputs/<t>.jsonl`, `mc/<t>/`). Only `brotlid` and `mailauth` are recall by construction.
- **screen+** is the Fig 9 baseline-band read (approximate); **solved 100%** is exact only in aggregate (17/25 ever, 3.1) — per-cell values are figure/text reads and `near` marks 2000/2001-style near-perfect runs.
- **flags**: `spec` = underdetermination the paper's own 3.3 charges to the model; `lang-forced` = implementation language pinned to defeat stdlib-triviality (App. A); `recall-witness` = a re-fetchable receipt above.

## Classes checked (the full rejection taxonomy from the prior audits)

Every rejection category from the [ProgramBench audit](https://github.com/kimjune01/program-bench-audit) (witness classes + `class_checks`), the SWE-bench Pro determinacy audit, Terminal-Bench, and tau-bench, swept against MirrorCode so the read is demonstrably complete rather than only the three classes above. One-sided: *no witness surfaced* and *neutralized* are not certificates of absence.

| category | from | verdict on MirrorCode | basis |
|---|---|---|---|
| recall (hash/cipher/codec/compressor) | ProgramBench | **PRESENT — 2 (brotlid, mailauth)** | graded output is a codec's / cryptographic signature's exact value; receipts above |
| implementation-pinned render (PNG/PDF/framemd5 bytes) | ProgramBench | **no witness surfaced** | no image/PDF/media/terminal-image target in the public set; the `*Renderer*.pkl` fixtures are pkl's text renderers, and such reverse-engineering targets were excluded by selection (§2.3) |
| undiscoverable entry point | ProgramBench | **no witness surfaced (public set)** | visible tests reveal task scope; the one candidate (gron `argv[0]`→ungron) MirrorCode itself dropped (E.1.2) |
| self-capturing golden | ProgramBench | **WHOLE-BENCHMARK, by construction** | every `data/gold_outputs/*` record is the reference binary's own I/O, with no independent contract check — the ProgramBench 'answer key written from the reference' pattern is structural here. Mitigated by I/O-only grading + the non-determinism screen (finding 00 gold clause), not eliminated |
| scale / coverage | ProgramBench | **PRESENT — 7 (the scale class)** | the hard/unsolved targets; size and intricacy, not recall |
| spec underdetermination (Airtight / Misdetermined / Plural) | SWE-bench Pro | **3 Plural (hexyl, sed, bib2json)** | the paper's own §3.3 failure cases; no Misdetermined or Airtight witness surfaced |
| non-determinism: time / random / uuid | ProgramBench | **neutralized** | screened and gold regenerated at runtime (Table 1); `uuidparse` parses, it does not generate |
| float-formatting | ProgramBench | **neutralized by selection** | exact-float-arithmetic targets were rejected (§2.3); `numfmt` is fixed-decimal SI, `giac` is exact symbolic (`1/6`, `ln(3)`) — spot-checked |
| locale / collation | ProgramBench | **neutralized** | fixed sandbox locale; `numfmt`'s eight locales reproduce identically for solver and reference |
| dir / hashmap enumeration order | ProgramBench | **no witness surfaced** | output orders are defined — `gron` sorts keys, `jq` preserves input order (spot-checked golds) |
| env / host / path leakage | ProgramBench | **neutralized** | shared sandbox reproduces any $HOME/host-derived output identically |
| parser-error-text (exact diagnostics) | ProgramBench | **benchable** | exact error wording is discoverable from the visible tests and by probing the reference |
| concurrency / interleaving | ProgramBench | **N/A** | single-shot CLI tasks; no interleaving graded |
| archive bit-exact (tar/zip layout) | ProgramBench | **no witness surfaced** | no archive-producing target; ruff's `*.tar.gz` are lint INPUTS, not graded output |
| frame (destructive completion scores 1) | Terminal-Bench | **avoided by design** | the oracle is I/O only, not final environment state (finding 00 frame clause; finding 04) |
| gold fails its own test | DeepSWE / SWE-bench Pro | **cannot arise** | the reference binary IS the oracle, so goldens pass by construction — which is also the self-capturing-golden concern above |
| decay / contamination | tau-bench | **PRESENT — 17 screen-positive** | finding 03 |

The only per-target rejection classes that fire are **recall** (2) and **scale** (7); **self-capturing goldens** are a whole-benchmark property; everything else is absent in the public set or neutralized by MirrorCode's non-determinism screen and its selection away from reverse-engineering targets. That MirrorCode drains so many of the categories that sank ProgramBench is itself the finding — and the credit ([finding 04](04_what_it_gets_right.md)).

*Data: `data/per_target.json`. Re-derive: `python3 scripts/build_per_target.py`. Recall receipts re-fetchable from the public MirrorCode repo. Sources: paper Table 3, §3.1, §3.3, §4.3, Fig 3, Fig 9, App. A, App. D.4, App. E.*
