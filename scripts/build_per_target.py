#!/usr/bin/env python3
"""Per-target audit of all 25 MirrorCode targets — the ProgramBench-style read.

Each target is classified by the same lens as the ProgramBench audit, against the
public MirrorCode repo (github.com/epoch-research/MirrorCode, mc/<target>/) and
the paper (arXiv:2606.30182). Emits data/per_target.json and findings/06_per_target.md.

Columns and their provenance (so every cell traces):
- bucket/lang/loc/command : paper Table 3 (verbatim).
- recall_class            : read of the graded I/O. "recall" = the graded output is
    an un-inferable function's value (hash/cipher/codec) no offline solver reproduces;
    verified against data/gold_outputs/<t>.jsonl and mc/<t>/ fixtures. "scale" =
    reconstructable in principle but large/intricate (the coverage barrier, not recall).
    "clean" = small + documented + reconstructable.
- screen_positive         : above the baseline band in Fig 9 (binary read; ~).
- solved_100              : whole-task 100% ever reached. Exact aggregate is "17/25
    ever" (paper 3.1); per-cell values are figure/text reads (flagged approx).
- spec_flag               : underdetermination the paper itself surfaces (3.3).
- lang_forced             : implementation language pinned to defeat stdlib-triviality (App. A).
- witness                 : for recall rows, a re-fetchable receipt.

This is a hand-adjudicated read (model proposes, author decides), not an automated
sweep: MirrorCode grades whole-task byte-exact I/O, so the recall judgement is per
target, and 22 of 25 are public (3 private marked "unread").
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# (target, bucket, lang, loc, command, recall_class, screen_pos, solved_100, spec_flag, lang_forced, note)
T = [
 ("qsv_select","S","Rust","87k","qsv select","clean",True,True,None,False,"column select/reorder; scoped to one subcommand of a 40+ cmd toolkit"),
 ("jq_simple","S","C","21k","jq","clean",True,True,None,False,"documented subset of jq; filter builtins discoverable via `jq -n builtins`"),
 ("gron","S","Go","2.3k","gron","clean",True,True,None,False,"flatten JSON to assignments; reconstructable"),
 ("bitwise","S","C","1.9k","bitwise","clean",False,True,None,False,"bitwise/base-conversion expression eval"),
 ("hexyl","S","Rust","1.8k","hexyl","clean",False,True,"hexyl: --block-size self-referential reject is non-obvious (E.1.3)",False,"hex viewer; some scope non-obvious but small"),
 ("uuidparse","S","C","1.2k","uuidparse","clean",True,True,None,False,"parse/describe UUIDs; format, not crypto"),
 ("numfmt","S","C","1.1k","numfmt","clean",True,True,None,False,"number reformatting; coreutils"),
 ("cal","S","C","984","cal","clean",True,True,None,False,"terminal calendar; util-linux"),
 ("choose","S","Rust","931","choose","clean","borderline",True,None,False,"cut/awk-like field selection"),
 ("private_S","S","?","?","(private)","unread",None,None,None,False,"private target — test bodies not released"),

 ("giac_subset","M","C++","31k","giac","scale",False,False,None,False,"symbolic integration + Groebner basis; math, reconstructable in principle but hard; a hardest target (3.1)"),
 ("texmacros","M","C","18k","pdftex","scale",False,True,None,False,"TeX macro/e-TeX expansion; intricate but documented semantics"),
 ("gotree","M","Go","16k","gotree","scale",True,"near",None,False,"phylogenetic trees; best run 2000/2001 (fn3), a date-edge miss"),
 ("mailauth","M","Rust","16k","mailauth","recall",True,False,None,False,"SPF/DKIM/DMARC/ARC verify+seal; graded output includes an exact RSA-SHA256 signature"),
 ("brotlid","M","C","13k","brotli -d","recall",True,False,None,False,"Brotli DEcompression of bundled .br streams to exact bytes; needs the RFC-7932 decoder + static dictionary"),
 ("wren_cli","M","C","7.8k","wren_cli","scale",True,True,None,False,"Wren interpreter; runs arbitrary Wren programs (incl. cipher test programs) — reconstructable from language semantics, not recall"),
 ("nonogrid","M","Rust","5.9k","nonogrid","clean",False,True,None,True,"nonogram solver; a search algorithm, deterministic output; forced to Go in 1L config"),
 ("sed","M","C","4.1k","sed","clean",True,True,"sed: --posix incompatible-flag disabling under-specified in visible tests (3.3)",False,"stream editor; scripting language, reconstructable"),
 ("tssql","M","Haskell","2.1k","tssql","clean",False,True,None,False,"SQL SELECT over CSV; solved though NOT screen-positive (4.3)"),
 ("bib2json","M","Haskell","2.0k","pandoc -f biblatex -t csljson","clean","borderline",True,"bib2json: useprefix default (absent->false) not pinned by visible tests (3.3)",False,"one format pair of pandoc"),
 ("private_M","M","?","?","(private)","unread",True,None,None,False,"private target; screen-positive per Fig 9"),

 ("ruff","L","Rust","250k","ruff check","scale",True,False,None,True,"Python linter (linter only); THE hardest target, best 67% hidden (3.1); forced to Go to avoid Python ast"),
 ("pkl","L","Java","61k","pkl eval","scale",True,"near",None,False,"Apple config language; reimplemented but rarely to strict 100% (L bucket)"),
 ("cprepro","L","C","27k","cc1 -E -quiet","scale",True,False,None,True,"C preprocessor; the one target with a known language-triviality flaw (D.4); forced to Go"),
 ("private_L","L","?","?","(private)","unread",None,None,None,True,"private target; excluded from Fig 9 screen"),
]

RECALL_WITNESS = {
 "brotlid": "`brotli --base64 10x10y.compressed` (bundled Brotli blob) -> exact decompressed bytes; "
            "real-world .br fixtures (mc/brotlid/test_data/) need the RFC-7932 decoder + static dictionary. "
            "gh api .../data/gold_outputs/brotlid.jsonl",
 "mailauth": "`mailauth arc-seal --key key.pem --domain gmail.com ...` -> stdout is an ARC-Seal header whose "
             "`b=` is an exact RSA-SHA256 signature; reproducing it needs RSA + SHA-256 + RFC-8617 canonicalization. "
             "gh api .../data/gold_outputs/mailauth.jsonl",
}

def main():
    rows = []
    for (t,b,l,loc,cmd,rc,sp,s100,spec,lf,note) in T:
        rows.append({
            "target": t, "bucket": b, "lang": l, "loc": loc, "command": cmd,
            "recall_class": rc, "screen_positive": sp, "solved_100": s100,
            "spec_flag": spec, "lang_forced": lf,
            "witness": RECALL_WITNESS.get(t), "note": note,
        })
    json.dump({"targets": rows, "provenance": {
        "table3": "paper arXiv:2606.30182 Table 3 (bucket/lang/loc/command)",
        "recall": "read of data/gold_outputs/<t>.jsonl + mc/<t>/ fixtures; hand-adjudicated",
        "screen_positive": "Fig 9 baseline-band binary read (approximate)",
        "solved_100": "aggregate 17/25-ever exact (3.1); per-cell figure/text reads (approximate)",
    }}, open(os.path.join(ROOT,"data","per_target.json"),"w"), indent=1)

    def cell(v):
        return {True:"yes",False:"no",None:"—"}.get(v, v)
    # counts
    n=len(rows); recall=[r for r in rows if r["recall_class"]=="recall"]
    scale=[r for r in rows if r["recall_class"]=="scale"]
    clean=[r for r in rows if r["recall_class"]=="clean"]
    unread=[r for r in rows if r["recall_class"]=="unread"]
    screenpos=[r for r in rows if r["screen_positive"] in (True,"borderline")]
    specf=[r for r in rows if r["spec_flag"]]

    with open(os.path.join(ROOT,"findings","06_per_target.md"),"w") as f:
        f.write("# 06 — Per-target audit (all 25)\n\n")
        f.write("The ProgramBench-style read: every MirrorCode target given a verdict, against the public repo "
                "(`github.com/epoch-research/MirrorCode`, `mc/<target>/`) and the paper. 22 are public and read "
                "here; 3 are private and marked *unread*. Hand-adjudicated, since MirrorCode grades whole-task "
                "byte-exact I/O, so the recall call is per target, not per assertion.\n\n")
        f.write("## Headline counts\n\n")
        f.write(f"- **Recall by construction: {len(recall)}/25** — `{'`, `'.join(r['target'] for r in recall)}`. "
                "The graded output is an un-inferable function's value (a codec, a cryptographic signature) no "
                "offline solver reproduces. Contrast ProgramBench's 21/201: MirrorCode's selection genuinely "
                "drained the recall surface — no hash, image, or media targets survive in the public set.\n")
        f.write(f"- **Scale/complex (reconstructable, but the coverage barrier bites): {len(scale)}/25** — "
                f"`{'`, `'.join(r['target'] for r in scale)}`. These are where solve rates fall (3.1, Fig 3): "
                "size and intricacy, not recall.\n")
        f.write(f"- **Clean/small (documented, reconstructable): {len(clean)}/25**.\n")
        f.write(f"- **Screen-positive (Fig 9): {len(screenpos)}** · **spec-underdetermined (paper's own 3.3): "
                f"{len(specf)}** (`{'`, `'.join(r['target'] for r in specf)}`) · **unread (private): {len(unread)}**.\n\n")
        f.write("## The table\n\n")
        f.write("| target | bkt | lang | LoC | recall class | screen+ | solved 100% | flags |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            flags=[]
            if r["spec_flag"]: flags.append("spec")
            if r["lang_forced"]: flags.append("lang-forced")
            if r["witness"]: flags.append("recall-witness")
            f.write(f"| {r['target']} | {r['bucket']} | {r['lang']} | {r['loc']} | "
                    f"**{r['recall_class']}** | {cell(r['screen_positive'])} | {cell(r['solved_100'])} | "
                    f"{', '.join(flags) or '—'} |\n")
        f.write("\n## Recall witnesses (receipts)\n\n")
        for r in recall:
            f.write(f"**{r['target']}** — {r['witness']}\n\n")
        f.write("## Reading the columns\n\n")
        f.write("- **recall class** is the load-bearing verdict, read from the graded I/O (`data/gold_outputs/"
                "<t>.jsonl`, `mc/<t>/`). Only `brotlid` and `mailauth` are recall by construction.\n")
        f.write("- **screen+** is the Fig 9 baseline-band read (approximate); **solved 100%** is exact only in "
                "aggregate (17/25 ever, 3.1) — per-cell values are figure/text reads and `near` marks "
                "2000/2001-style near-perfect runs.\n")
        f.write("- **flags**: `spec` = underdetermination the paper's own 3.3 charges to the model; `lang-forced` "
                "= implementation language pinned to defeat stdlib-triviality (App. A); `recall-witness` = a "
                "re-fetchable receipt above.\n\n")
        f.write("*Data: `data/per_target.json`. Re-derive: `python3 scripts/build_per_target.py`. Recall receipts "
                "re-fetchable from the public MirrorCode repo. Sources: paper Table 3, §3.1, §3.3, §4.3, Fig 3, "
                "Fig 9, App. A, App. D.4, App. E.*\n")
    print(f"wrote findings/06_per_target.md and data/per_target.json")
    print(f"recall={len(recall)} scale={len(scale)} clean={len(clean)} unread={len(unread)} "
          f"screen+={len(screenpos)} spec={len(specf)}")

if __name__ == "__main__":
    main()
