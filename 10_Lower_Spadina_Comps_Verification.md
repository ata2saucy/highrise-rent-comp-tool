# 10 Lower Spadina — Comps Verification Log

> Source-of-truth log for every reported number. Append-only by date (Non-negotiable #5).

---

## 2026-06-22 — Full no-cap re-pull (PBR-subject scenario)

**Subject (refreshed Step 0, vipcondostoronto.net this session):** 10 Lower Spadina Condos by
Arkfield — 49 storeys / 511 suites, 152 m, **Planning Phase / Pre-Construction**, Waterfront
(TRREB C01). No floor plans published ⇒ subject suite mix estimated.
URL: https://www.vipcondostoronto.net/toronto/10-lower-spadina-condos-5014

**Subject intake (user, 2026-06-22):**
1. Product type → **Purpose-Built Rental (PBR)** — *overrides vipcondos (lists it as condo).*
2. Suite mix → **skip** → estimated waterfront program (45% 1BR / 18% 1+den / 30% 2BR / 7% 3BR).
3. Build status → **pre-construction** (new-build premium applies).

Because the subject is a PBR, the 9 condo buildings are **cross-product** comps: their $/SF is
bridged **down** to PBR-equivalent by the condo→PBR premium (~10%). The same-product (PBR) track
was searched (rentals.ca) — candidates 25 Lower Simcoe, 30 Grand Trunk Cres, 15 Fort York Blvd,
8 Mercer St, 39 Niagara St, 33 Bay St, 16 Yonge St — **all asking-only with no verified
floor-plan SF, so none cleared the exact-or-blank SF bar; excluded from $/SF.**

**Comp set (user-confirmed re-run):** all 9 nearby condos —
Concord Canada House (23 Spadina, 2025, PRIMARY) · Nobu Residences (15 Mercer, 2024) ·
The Well (470-486 Front W, 2024) · Ten York (10 York, 2019) · Forward (70-90 Queens Wharf, 2018) ·
Quartz/Spectra (75-85 Queens Wharf, 2015) · Library District (170 Fort York, 2014) ·
N1|N2 CityPlace (15 Fort York, 2008) · Aqua (410 Queens Quay W, 2003).

### Method (Route B — condos.ca registered area, no cap)
- Data read in-browser this session from condos.ca's own leased index (Algolia, app `1TVIG461EC`,
  index `condos_search_archive_listings_end_date_unix_desc`, filter
  `building_id=<id> AND offer:"Rent" AND status:"Leased"`). The returned `sqft`
  (source **"Calculated"**) is the per-unit **registered area** shown on the unit page.
- **This-session SF verification:** opened actual unit pages and confirmed the index area equals
  the page `NNN sqft*` — **Concord 929 = 888 sqft** (leased $3,750 / listed $3,950, 2026-06-18)
  and **Aqua 414 = 600 sqft** (leased $2,500, 2026-06-17). Both exact matches.
- **NO per-building cap.** Every in-window leased transaction (lease end-date ≥ 2025-01-01) was
  pulled for each building.

### Pull counts (in-window, Jan 2025 → 2026-06-22)
| Building | In-window leases | Verified SF (comp rows) | No registered area (excl.) |
|---|---|---|---|
| Concord Canada House | 649 | 284 | 365 |
| Nobu Residences | 253 | 209 | 44 |
| The Well | 218 | 56 | 162 |
| Ten York | 168 | 168 | 0 |
| Forward | 154 | 153 | 1 |
| Quartz / Spectra | 230 | 0 | 230 (no registered area for the corp) |
| Library District | 72 | 69 | 3 |
| N1 \| N2 CityPlace | 102 | 100 | 2 |
| Aqua | 31 | 31 | 0 |
| **TOTAL** | **1,877** | **1,070 → 1,068 after de-dup** | **809** |

- **1,068** verified-SF leased comps form the workbook comp set (2 duplicate index artifacts —
  Library 610 / N1|N2 102, same unit+date+rent re-indexed — removed; 0 genuine duplicates remain).
- Confidence: **760 green** (source Calculated, SF inside MLS bracket, unfurnished) +
  **308 cream** (size "Known"/stated, or calc SF outside the MLS bracket — flagged, or
  furnished/short-term).
- **809 in-window leases carry no published registered area** on condos.ca (exact-or-blank ⇒
  excluded from $/SF). This includes **all 230 Quartz/Spectra** (the corporation publishes no
  per-unit registered area; Route A vipcondos plan-by-stack recovery was **not re-run** this
  session). These are recorded as pulled-but-unverified, not as comps.

### Result (workbook, validated green)
- **PREMIUM BASIS (vintage spread):** newest (Concord) **$4.314/SF** · all-comp **$4.264/SF** ·
  oldest (Aqua) **$3.909/SF**. Derived new-build premium **C4 = 5.77%** (midpoint of the two
  observed vintage premiums) — replaces the prior assumed 10%.
- **Recommended subject $/SF (CONDO-EQUIVALENT basis) = $4.555/SF** (Concord primary + C4).
  All-comp + premium basis lower.
- **PBR-subject achievable rent** = condo-equivalent ÷ (1 + ~10% condo→PBR premium):
  ≈ **$4.14/SF** off the primary basis (≈ **$3.88/SF** off the all-comp basis). The 10% condo→PBR
  premium is an external/prior-model anchor (no verified PBR comps to derive it this session).
- Prior model (2026-06-17, condo subject, 107 comps, 10% premium): $4.78/SF. The drop to $4.555
  is driven by (a) the deeper 1,068-comp base and (b) the **derived** 5.77% premium vs the prior
  assumed 10%.

### Validation
`validate_workbook.py` → **PASS**: 6-sheet structure, widths/gridlines/freeze panes,
confidence fills confined to RD B/E, no INPUTS table; **zero formula errors** (bounded-range
recalc); numpy tie-out on C58/C59/C60/C31/C4/C34; **SF coverage 1,068/1,068 = 100%**, zero
undocumented leased-in-window blanks.

### Data ceiling / next run
- Quartz/Spectra (230 leases) and The Well small suites + Concord null-area units (~809 total)
  need Route A (vipcondos plan-by-stack) to recover SF — deferred this session.
- A true PBR comp would need a purpose-built rental with a published suite floor plan / registered
  area; the rentals.ca candidates are asking-only. Definitive subject SF = Arkfield developer
  suite-area schedule when released.
