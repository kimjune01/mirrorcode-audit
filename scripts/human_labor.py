#!/usr/bin/env python3
"""Human-labor context for MirrorCode's target programs, from public git history.

MirrorCode (arXiv:2606.30182) frames its headline around unmeasured belief:
"We believe a human engineer without AI would take months" / "2-17 weeks".
Its targets are REAL open-source programs, so their DEVELOPMENT RECORD is public.
This script reads each target's upstream git history (via the GitHub API) and
reports the hard, falsifiable facts:

  - merged PR count, total commits, unique contributors
  - calendar span (first -> last commit)

and one HEURISTIC (not a validated effort model): person-hours ~= commits * H,
with H = 1.666 h, the published MEDIAN INTER-COMMIT INTERVAL (Kolassa, Riehle &
Salim 2013, arXiv:1408.4978, Table 1). Caveats, stated plainly because this is
the audit's own construction: H is ELAPSED time between commits, not measured
effort (double-counts short breaks, misses non-committing design/review); and it
is computed on the CURRENT DEFAULT BRANCH, not the pinned upstream version
MirrorCode tested. So the hour/week figures are an order-of-magnitude
illustration; the load-bearing output is the descriptive record, not the hours.

Re-runnable: needs `gh` authenticated. `python3 scripts/human_labor.py`.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "human_labor.json")

# target -> (upstream repo, bucket, ref lang, MirrorCode's human estimate, coverage, scope note)
# coverage: how much of the upstream repo MirrorCode's task actually spans, which
# governs whether the whole-repo history is an APT anchor or an OVER-count:
#   whole   - MirrorCode reimplements essentially the whole program
#   most    - the tested surface is the bulk of the repo
#   partial - a substantial component of a larger repo
#   scoped  - a small slice of a much larger repo (whole-repo count OVER-states)
TARGETS = [
    ("ruff",       "astral-sh/ruff",         "L", "Rust",   "months",     "most",    "the linter (`ruff check`); formatter excluded"),
    ("pkl",        "apple/pkl",              "L", "Java",   "months",     "whole",   "`pkl eval`; full config language"),
    ("gotree",     "evolbioinfo/gotree",     "M", "Go",     "2-17 weeks", "whole",   "40+ subcommands"),
    ("brotlid",    "google/brotli",          "M", "C",      None,          "partial", "DECOMPRESSION only (`brotli -d`); repo also has encoder"),
    ("mailauth",   "stalwartlabs/mail-auth", "M", "Rust",   None,          "whole",   "SPF/DKIM/DMARC verification"),
    ("wren_cli",   "wren-lang/wren-cli",     "M", "C",      None,          "whole",   "the Wren interpreter CLI"),
    ("nonogrid",   "tsionyx/nonogrid",       "M", "Rust",   None,          "whole",   "nonogram solver"),
    ("jq_simple",  "jqlang/jq",              "S", "C",      None,          "scoped",  "a documented SUBSET of jq"),
    ("gron",       "tomnomnom/gron",         "S", "Go",     None,          "whole",   "whole tool"),
    ("hexyl",      "sharkdp/hexyl",          "S", "Rust",   None,          "whole",   "whole tool"),
    ("choose",     "theryangeary/choose",    "S", "Rust",   None,          "whole",   "whole tool"),
    ("bitwise",    "mellowcandle/bitwise",   "S", "C",      None,          "scoped",  "expression-evaluation subset"),
    ("qsv_select", "dathere/qsv",            "S", "Rust",   None,          "scoped",  "`qsv select` only; repo is a 40+ cmd toolkit"),
    ("uuidparse",  "util-linux/util-linux",  "S", "C",      None,          "scoped",  "just `uuidparse` within all of util-linux"),
    ("cal",        "util-linux/util-linux",  "S", "C",      None,          "scoped",  "just `cal` within all of util-linux"),
    ("bib2json",   "jgm/pandoc",             "M", "Haskell","2-17 weeks", "scoped",  "one format pair (biblatex->csljson) of pandoc"),
    ("tssql",      "seanhess/txt-sushi",     "M", "Haskell",None,          "partial", "`tssql` tool of txt-sushi"),
    # Not GitHub-native / unresolved upstream (recorded, not queried):
    #   sed (GNU), numfmt (GNU coreutils), texmacros (pdftex/TeX Live),
    #   giac_subset (Giac/Xcas), cprepro (GCC-derived), private_{S,M,L}
]

# Neutral, PUBLISHED effort-per-commit constant, not an invented one:
# Kolassa, Riehle & Salim, "The Empirical Commit Frequency Distribution of Open
# Source Projects", WikiSym+OpenSym 2013 (arXiv:1408.4978), Table 1: the MEDIAN
# interval between two consecutive commits of the same committer is 1.666 h.
# (The MEAN is 3.206 DAYS, dominated by idle gaps; mean*commits would measure
# calendar span, not effort, so the median is the right active-work proxy.)
# We treat each commit as ~1.666 h of development work: an order-of-magnitude
# anchor on ORIGINAL creation effort. It excludes non-committing work
# (design/review), so it under-counts total project effort; it charges a full
# interval to rapid-fire commits, so it over-counts bursts. Net: a citable,
# neutral central estimate, used as ONE standard across all targets.
H_PER_COMMIT = 1.666
WORK_WEEK_H = 40.0

# Cross-check anchor from MirrorCode's OWN published human baseline (footnote 7):
# a skilled SWE did NOT finish a ~2,000-LoC task in 20 h, passing 42% of tests
# => ~20/0.42 = ~48 h to 100%. This measures REIMPLEMENTATION-from-a-working-
# reference, a different (easier) task than original creation.
MIRRORCODE_HUMAN_REIMPL_H = round(20 / 0.42, 1)  # ~47.6 h for a ~2k-LoC scoped task

def gh_json(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except Exception:
        return None

def gh_count_via_link(path):
    """Total items = last-page number when per_page=1 (from the Link header)."""
    r = subprocess.run(["gh", "api", "-i", path], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    m = re.search(r'[?&]page=(\d+)>;\s*rel="last"', r.stdout)
    if m:
        return int(m.group(1))
    # no Link header => 0 or 1 items; count the body
    body = r.stdout.split("\r\n\r\n", 1)[-1]
    try:
        return len(json.loads(body))
    except Exception:
        return None

def merged_prs(repo):
    d = gh_json(f"/search/issues?q=repo:{repo}+type:pr+is:merged&per_page=1")
    return d.get("total_count") if d else None

def commit_count(repo):
    return gh_count_via_link(f"/repos/{repo}/commits?per_page=1")

def first_commit_date(repo, n):
    if not n:
        return None
    d = gh_json(f"/repos/{repo}/commits?per_page=1&page={n}")
    if isinstance(d, list) and d:
        return d[0]["commit"]["committer"]["date"][:10]
    return None

def contributors(repo):
    return gh_count_via_link(f"/repos/{repo}/contributors?per_page=1&anon=1")

def main():
    rows = []
    for name, repo, bucket, lang, est, coverage, scope in TARGETS:
        meta = gh_json(f"/repos/{repo}")
        if not meta:
            print(f"[skip] {name}: {repo} not resolvable", file=sys.stderr)
            rows.append({"target": name, "repo": repo, "error": "unresolved"})
            continue
        prs = merged_prs(repo)
        commits = commit_count(repo)
        first = first_commit_date(repo, commits)
        contrib = contributors(repo)
        last = (meta.get("pushed_at") or "")[:10]
        span_years = None
        if first and last:
            span_years = round((int(last[:4]) - int(first[:4])) + (int(last[5:7]) - int(first[5:7])) / 12, 1)
        # commits are the universal labor unit (every repo has them; PR workflow varies).
        # ORIGINAL-creation effort anchor = commits * 1.666 h  (Kolassa et al. 2013).
        dev_h = round(commits * H_PER_COMMIT) if commits else None
        dev_wk = round(dev_h / WORK_WEEK_H, 1) if dev_h else None
        row = {
            "target": name, "repo": repo, "bucket": bucket, "ref_lang": lang,
            "mirrorcode_human_estimate": est, "coverage": coverage, "scope_tested": scope,
            "merged_prs": prs, "commits": commits, "contributors": contrib,
            "first_commit": first, "last_activity": last, "span_years": span_years,
            # original-development effort embodied in the WHOLE upstream repo:
            "creation_dev_hours_kolassa": dev_h,
            "creation_dev_weeks_kolassa": dev_wk,
            "note": "whole-repo count OVER-states MirrorCode's scoped slice" if coverage == "scoped" else "",
            "stars": meta.get("stargazers_count"),
        }
        rows.append(row)
        flag = "  [OVER-COUNT: scoped slice]" if coverage == "scoped" else ""
        print(f"{name:12} {repo:26} commits={commits} span={span_years}y  "
              f"creation~{dev_h}h (~{dev_wk}wk) [{coverage}]{flag}", flush=True)
    # median over the CLEAN anchors only (coverage=='whole'): exclude 'most'/'partial'
    # (ruff, brotlid) and 'scoped' (whole-repo over-counts the tested slice).
    whole = [r for r in rows if r.get("coverage") == "whole" and r.get("creation_dev_weeks_kolassa")]
    wk = sorted(r["creation_dev_weeks_kolassa"] for r in whole)
    def _median(xs):
        n = len(xs)
        if n == 0:
            return None
        return xs[n//2] if n % 2 else round((xs[n//2 - 1] + xs[n//2]) / 2, 1)
    median_wk = _median(wk)
    out = {
        "meta": {
            "effort_per_commit_hours": H_PER_COMMIT,
            "effort_source": "Kolassa, Riehle & Salim 2013 (arXiv:1408.4978), Table 1 median inter-commit interval",
            "work_week_hours": WORK_WEEK_H,
            "mirrorcode_human_reimpl_hours_2kLoC": MIRRORCODE_HUMAN_REIMPL_H,
            "mirrorcode_human_reimpl_source": "MirrorCode arXiv:2606.30182 footnote 7: 20 h -> 42% of tests on a ~2,000-LoC task",
            "median_creation_weeks_whole_only": median_wk,
            "whole_only_targets": [r["target"] for r in whole],
        },
        "targets": rows,
    }
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"\n--- anchors ---")
    print(f"ORIGINAL CREATION (Kolassa 1.666 h/commit): median whole-program target "
          f"= ~{median_wk} dev-weeks embodied in the upstream repo")
    print(f"REIMPLEMENTATION (MirrorCode's own human baseline): ~{MIRRORCODE_HUMAN_REIMPL_H} h "
          f"(~{round(MIRRORCODE_HUMAN_REIMPL_H/WORK_WEEK_H,1)} wk) for a ~2k-LoC scoped task")
    print(f"wrote {OUT}")

if __name__ == "__main__":
    main()
