#!/usr/bin/env python3
"""
quality_agent.py — plausibility / sanity gate for a generated v2 comp workbook.

    python quality_agent.py comp_data.json ["<workbook>.xlsx"]

`validate_workbook.py` proves the workbook is INTERNALLY correct (right structure, zero
formula errors, averages tie out). It does NOT ask whether the underlying comp set is
*good enough* to trust the recommendation. This agent does — it inspects the verified
inputs for the kinds of thin / weird data that quietly poison a triangulation, and tells
the operator (Claude) when the run must be REDONE rather than delivered.

It is deliberately separate from the validator: a workbook can be perfectly well-formed
(PASS) and still rest on, say, one comp building with six leases and no 2-bed SF — which
this agent catches and turns into a RERUN with concrete actions.

Verdict + exit code:
    PASS    (0) — comp set is healthy; deliver.
    REVIEW  (2) — usable, but deliver WITH the listed caveats noted in the writeup.
    RERUN   (1) — the comp set is too thin / anomalous to trust; do the listed actions
                  (re-pull leases, widen the window, add/replace comps, resolve more SF,
                  drop outliers), then regenerate + re-validate + re-run this gate.

Thresholds are tunable constants below — they encode "what good looks like" for this tool.
"""
import sys, json, re, statistics
from collections import defaultdict, Counter

# ---- tunable thresholds -----------------------------------------------------------------
MIN_TOTAL_LEASED        = 25      # total leased-in-window across all comps; below -> RERUN
MIN_BLDG_LEASED_RERUN   = 5       # a comp building this thin can't anchor anything -> RERUN
MIN_BLDG_LEASED_WARN    = 10      # thin building -> REVIEW (consider re-pull / drop)
SF_COVERAGE_RERUN       = 0.25    # SF-verified / leased-in-window below this -> RERUN
SF_COVERAGE_WARN        = 0.50    # ...below this -> REVIEW
BEDTYPE_MIN_SFCOMPS     = 3       # a subject-mix bed group needs >= this many SF comps
BEDTYPE_SFCOMPS_RERUN   = 0       # a subject-mix bed group with this many SF comps -> RERUN
PSF_SANE_LO, PSF_SANE_HI = 2.0, 6.0      # $/SF outside this band is implausible (GTA condo)
PSF_OUTLIER_FRAC_RERUN  = 0.10    # >this fraction of SF rows out of band -> RERUN
RENT_SANE_LO, RENT_SANE_HI = 1200, 9000  # monthly rent outside this band is suspicious
MAD_K                   = 4.0     # per building+bed, $/SF more than K MADs off median = outlier
C4_WARN_LO, C4_WARN_HI  = -0.10, 0.25    # subject premium outside this -> REVIEW
C4_RERUN_LO, C4_RERUN_HI = -0.25, 0.50   # ...outside this -> RERUN
C3_WARN_LO, C3_WARN_HI  = 0.0, 0.25      # apartment premium plausibility
WINDOW_UNDERPULL_DAYS   = 45      # building's oldest in-window lease this far AFTER C1 -> maybe under-pulled

rerun, review, info = [], [], []
def R(m): rerun.append(m)
def W(m): review.append(m)
def I(m): info.append(m)

BEDGRP = lambda b: ("1BR" if str(b) in ("0", "1") else "1+Den" if str(b) == "1+1"
                    else "2BR" if str(b) in ("2", "2+1") else "3BR" if str(b) in ("3", "3+1") else "?")

def days_between(a, b):
    import datetime
    try:
        da = datetime.date.fromisoformat(a); db = datetime.date.fromisoformat(b)
        return (da - db).days
    except Exception:
        return None

def main():
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    lev = data["levers"]; C1 = lev["date_filter"]
    C4 = None  # derived; recompute below the same way validate does
    subj = data["subject"]
    condo = data.get("condo_rows", []); apt = data.get("apartment_rows", [])

    def leased_inwin(rows):
        return [r for r in rows if r.get("leased_rent") and str(r.get("date", "")) >= C1]
    def has_sf(r): return bool(r.get("sqft"))

    li = leased_inwin(condo)
    sfrows = [r for r in li if has_sf(r)]
    print("QUALITY AGENT — plausibility gate")
    print("  subject: %s (%s, %s)  | window C1>=%s" % (
        subj["name"], subj.get("product"), subj.get("status"), C1))
    print("  comp condo leased-in-window=%d  SF-verified=%d (%.0f%%)  apartment rows=%d" % (
        len(li), len(sfrows), (100.0*len(sfrows)/len(li) if li else 0), len(apt)))

    # 1) total volume
    if len(li) < MIN_TOTAL_LEASED:
        R("Total leased-in-window comps = %d (< %d). Sample too thin to triangulate — widen the "
          "date window (C1) or add comp buildings." % (len(li), MIN_TOTAL_LEASED))

    # 2) per-building transaction counts + SF coverage + window under-pull
    by_b = defaultdict(list)
    for r in li: by_b[r["building"]].append(r)
    comp_bldgs = [b["name"] for b in data.get("comp_buildings", []) if b.get("product") != "Apartment"]
    for name in comp_bldgs:
        rows = by_b.get(name, [])
        n = len(rows); nsf = sum(1 for r in rows if has_sf(r))
        if n == 0:
            W("Comp building '%s' has 0 leased-in-window rows — confirm it belongs in the set or re-pull." % name); continue
        if n < MIN_BLDG_LEASED_RERUN:
            R("Comp building '%s' has only %d leased-in-window leases (< %d) — re-pull its history "
              "(load ALL pages back to C1) or drop/replace it." % (name, n, MIN_BLDG_LEASED_RERUN))
        elif n < MIN_BLDG_LEASED_WARN:
            W("Comp building '%s' is thin (%d leased-in-window) — verify the full history loaded." % (name, n))
        cov = nsf / n
        if nsf == 0:
            W("Comp building '%s' contributes 0 verified $/SF (%d leases, all SF-blank) — it adds rent "
              "depth only; resolve its per-unit SF (condos.ca registered areas) to make it count in $/SF." % (name, n))
        # window under-pull: oldest in-window lease far from C1
        ds = sorted(str(r.get("date", "")) for r in rows)
        if ds:
            gap = days_between(ds[0], C1)
            if gap is not None and gap > WINDOW_UNDERPULL_DAYS and n >= MIN_BLDG_LEASED_WARN:
                I("'%s' oldest in-window lease is %s (%d days after C1) — likely fully pulled, but confirm "
                  "the loader reached the filter." % (name, ds[0], gap))

    # 3) SF coverage overall
    cov = len(sfrows) / len(li) if li else 0
    if cov < SF_COVERAGE_RERUN:
        R("SF-verified coverage = %.0f%% (< %.0f%%). Too few $/SF anchors — resolve more interior SF "
          "(vipcondos plan-match / condos.ca registered areas / key-plates) before trusting $/SF." % (100*cov, 100*SF_COVERAGE_RERUN))
    elif cov < SF_COVERAGE_WARN:
        W("SF-verified coverage = %.0f%% (< %.0f%%). Recommendation rests on the verified minority — "
          "deepen SF where feasible; note the coverage in the writeup." % (100*cov, 100*SF_COVERAGE_WARN))

    # 4) per-bed-type SF comp counts vs the subject mix
    mix = lev.get("subject_mix_output", {})
    bed_sf = Counter(BEDGRP(r.get("beds")) for r in sfrows)
    mix_share = {"1BR": mix.get("1BR", 0), "1+Den": mix.get("1+Den", 0),
                 "2BR": mix.get("2BR", 0), "3BR": mix.get("3BR", 0)}
    for grp, share in mix_share.items():
        if share and share > 0:
            nb = bed_sf.get(grp, 0)
            if nb <= BEDTYPE_SFCOMPS_RERUN:
                W("Subject mix has %.0f%% %s but ZERO SF-verified %s comps — that bed type's $/SF is "
                  "unsupported (0-weighted / indicative only). Resolve SF for %s leases or treat its rent as indicative."
                  % (100*share, grp, grp, grp))
            elif nb < BEDTYPE_MIN_SFCOMPS:
                W("Only %d SF-verified %s comp(s) for a %.0f%% mix share — %s $/SF is fragile." % (nb, grp, 100*share, grp))

    # 5) $/SF sane-band + per-(building,bed) MAD outliers
    out_band = []
    for r in sfrows:
        psf = r["leased_rent"] / r["sqft"]
        if psf < PSF_SANE_LO or psf > PSF_SANE_HI:
            out_band.append((r["building"], r.get("unit"), round(psf, 2)))
    if out_band:
        frac = len(out_band) / len(sfrows)
        msg = "$/SF out of sane band [%.1f, %.1f] on %d row(s): %s" % (
            PSF_SANE_LO, PSF_SANE_HI, len(out_band), out_band[:6])
        (R(msg + " — >%.0f%% of SF rows; SF or rent likely wrong, fix before delivering." % (100*PSF_OUTLIER_FRAC_RERUN))
         if frac > PSF_OUTLIER_FRAC_RERUN else W(msg + " — inspect (furnished/partial/short-term or SF error)."))
    grp = defaultdict(list)
    for r in sfrows: grp[(r["building"], BEDGRP(r.get("beds")))].append(r)
    mad_out = []
    for (b, g), rows in grp.items():
        if len(rows) < 5: continue
        ps = [x["leased_rent"]/x["sqft"] for x in rows]
        med = statistics.median(ps)
        mad = statistics.median([abs(p - med) for p in ps]) or 0.01
        for x in rows:
            p = x["leased_rent"]/x["sqft"]
            if abs(p - med) > MAD_K * mad:
                mad_out.append((b, x.get("unit"), round(p, 2), "med %.2f" % med))
    if mad_out:
        W("$/SF outliers vs building+bed median (>%.0f MAD): %s — verify SF/rent (mis-matched plan, "
          "furnished, or short-term)." % (MAD_K, mad_out[:6]))

    # 6) rent sane band
    rent_out = [(r["building"], r.get("unit"), r["leased_rent"]) for r in li
                if r["leased_rent"] < RENT_SANE_LO or r["leased_rent"] > RENT_SANE_HI]
    if rent_out:
        W("Leased rent outside [$%d, $%d] on %d row(s): %s — confirm (room rental / luxury PH / typo)."
          % (RENT_SANE_LO, RENT_SANE_HI, len(rent_out), rent_out[:6]))

    # 7) premiums in band  (recompute C4 like validate does)
    primary = subj.get("primary_building"); oldest = subj.get("oldest_building", primary)
    E = lambda r: r["leased_rent"]/r["sqft"]
    avg = lambda sel: (sum(E(r) for r in sel)/len(sel)) if sel else None
    c58 = avg([r for r in sfrows if r["building"] == primary])
    c59 = avg(sfrows)
    c60 = avg([r for r in sfrows if r["building"] == oldest])
    c61 = (c58/c59 - 1) if (c58 and c59) else 0
    c62 = (c58/c60 - 1) if (c58 and c60) else 0
    sp = lev.get("subject_premium")
    C4 = (sp["value"] if sp else 0.0) if (abs(c61) < 1e-4 and abs(c62) < 1e-4) else (c61 + c62)/2
    if C4 < C4_RERUN_LO or C4 > C4_RERUN_HI:
        R("Derived subject premium C4 = %+.1f%% is implausible (outside [%+.0f%%, %+.0f%%]) — the "
          "newest/oldest $/SF anchors are likely mis-set or distorted by thin SF; re-check primary/oldest "
          "buildings and SF coverage." % (100*C4, 100*C4_RERUN_LO, 100*C4_RERUN_HI))
    elif C4 < C4_WARN_LO or C4 > C4_WARN_HI:
        W("Derived subject premium C4 = %+.1f%% is outside the usual [%+.0f%%, %+.0f%%] — sanity-check vs "
          "a lease-up assumption / prior model." % (100*C4, 100*C4_WARN_LO, 100*C4_WARN_HI))
    apc = lev.get("apt_premium", {})
    if not apc.get("off") and (apc.get("value", 0) < C3_WARN_LO or apc.get("value", 0) > C3_WARN_HI):
        W("Apartment premium C3 = %.1f%% outside [%.0f%%, %.0f%%] — re-check basis." % (
            100*apc.get("value", 0), 100*C3_WARN_LO, 100*C3_WARN_HI))

    # 8) duplicate leases
    seen = Counter((r["building"], r.get("unit"), r.get("date"), r.get("leased_rent")) for r in li)
    dups = [k for k, c in seen.items() if c > 1]
    if dups:
        W("Possible duplicate leases (building, unit, date, rent) x%d: %s — dedupe." % (len(dups), dups[:5]))

    # 9) TRREB + listed-rent context
    if not data.get("trreb"):
        I("TRREB quarterly rent table absent — populate from the latest TRREB Rental Market Report "
          "for the subject district (blank beats invented, but the Output table stays empty).")
    listed_cov = sum(1 for r in condo if r.get("listed_rent")) / len(condo) if condo else 0
    if listed_cov < 0.05:
        I("Listed (asking) rent captured on ~0%% of condo rows — the asking-vs-leased ('selling as vs "
          "sold for') gap is not populated for condos; pull listed rents if that view is wanted.")

    # ---- verdict ----
    print()
    for tag, items in (("RERUN", rerun), ("REVIEW", review), ("INFO", info)):
        for m in items:
            print("  [%s] %s" % (tag, m))
    print()
    if rerun:
        print("VERDICT: RERUN — the comp set is too thin/anomalous to deliver. Address the [RERUN] actions "
              "above, then regenerate (build_workbook.py), re-validate (validate_workbook.py), and re-run this gate.")
        sys.exit(1)
    if review:
        print("VERDICT: REVIEW — deliverable, but surface the [REVIEW] caveats in the writeup/verification log.")
        sys.exit(2)
    print("VERDICT: PASS — comp set looks healthy.")
    sys.exit(0)

if __name__ == "__main__":
    main()
