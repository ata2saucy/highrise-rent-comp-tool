# 10 Lower Spadina Condos — building memory (stable facts only; NO reportable SF)

> Memory is a map, not proof. Re-open the source this session before reporting any number.
> SUBJECT — pre-construction downtown-waterfront condo (Arkfield). Comps = 9 nearby condos.

## Identity
- Marketing name: 10 Lower Spadina Condos
- Developer: Arkfield / A1 Development
- Address: 10 Lower Spadina Ave, Toronto — Waterfront / CityPlace fringe — **TRREB district C01**
- Storeys / total units: **49 storeys / 511 suites** (vipcondos Step 0, 2026-06-16)
- Status: Planning Phase / pre-construction; expected delivery ~2029-30. **No floor plans / suite
  areas published** (vipcondos: "No floor plans currently available") → subject unit mix is
  **estimated**, not derived.

## Working sources
- vipcondostoronto.net: subject page (search the on-page box — never guess the URL). Step-0 identity
  only; no plans yet.
- Comp lease + per-unit SF: **condos.ca** (signed-in). Floor plans / key-plates for SF-ceiling comps:
  **vipcondostoronto.net** (Route A).

## Subject parameters (workbook levers — confirm/refresh each run)
- Suite count T2 = 511 · storeys 49. Estimated mix (Q8:Q10 den-incl) **63% 1-Bed / 30% 2-Bed / 7% 3-Bed**;
  Output 4-way (T3:T6) **45% 1BR / 18% 1+Den / 30% 2BR / 7% 3BR**. Source: estimated downtown-waterfront
  program — **supersede with the developer suite schedule when published** (authoritative).
- Date filter C1 = 2025-01-01. Apartment premium C3 = 10% (unused — no apartment comps).
  **Subject rental premium C4 = 10%** (proposed; brand-new 2029-30 vs comp blend; anchored to the live
  PREMIUM BASIS block — observed vintage spread +3.4% newest÷all to +16.3% newest÷oldest).

## Comp set (user-confirmed 2026-06-16 — all 9 shortlisted picked)
| Building | Address | Built | Role /10 | SF on condos.ca | Notes |
|---|---|---|---|---|---|
| [Concord Canada House](concord_canada_house.md) | 23 Spadina Ave | 2025 | PRIMARY 10 | exact (registered) | Newest, on Spadina; deepest fresh-lease depth |
| Nobu Residences | 15 Mercer St | 2024 | secondary 8 | exact | King West luxury; Madison Group |
| [The Well](the_well_toronto.md) | 470-480 Front St W | 2024 | secondary 8 | **small suites bracket-only** | Tridel flagship; Route A for SF |
| Ten York | 10 York St | 2019 | secondary 7 | exact | Tridel; waterfront |
| Forward Condos | 70-90 Queens Wharf Rd | 2018 | secondary 7 | exact | Concord Adex; CityPlace |
| [Quartz/Spectra](quartz_spectra.md) | 75-85 Queens Wharf Rd | 2015 | supporting 5 | **bracket-only (0 verified)** | SF ceiling → Route A |
| Library District | 170 Fort York Blvd | 2014 | supporting 6 | exact | CityPlace |
| N1 \| N2 – CityPlace | 15 Fort York Blvd | 2008 | supporting 5 | exact | CityPlace |
| Aqua | 410 Queens Quay W | 2003 | supporting 5 | exact | Waterfront; sets oldest-vintage floor |

## Evaluated & excluded (logged in Output → comp-quality scores)
Sugar Wharf (95 Lake Shore E, 2023 — different micro-market) · Lighthouse / Aquabella / Aqualuna
(East Bayfront, ~2.5 km) · Bisha / King Blue / Theatre Park (Entertainment District) · older CityPlace
(Optima/Apex/Montage/Neo/Luna/Parade/West One/Harbour View — redundant with the included CityPlace floor).

## Gotchas
- **2026-06-17 (resolves the prior "thin coverage" gotcha):** all 9 buildings now at 11–12 verified comps.
  Quartz/Spectra has **no per-unit registered area on condos.ca** (whole corp) — recover SF from the **vipcondos
  Spectra plan sheet**: unit's last 2 digits = stack = suite plan (01=980, 02=712, 03/05=645, 06=1008, 07=590,
  08=438, 09=540, 10=535, 11=570, 12=808). condos.ca `title` field separates 75 (Quartz) from 85 (Spectra).
- **2026-06-17 (operational):** condos.ca search/leased data is Algolia-backed — index
  `condos_search_archive_listings_end_date_unix_desc`, filter `building_id=<id> AND offer:"Rent" AND status:"Leased"`;
  building ids: Concord 6190, Nobu 5805, The Well 8795, Ten York 1494, Forward 2046, Quartz/Spectra 2193,
  Library 1378, N1|N2 368, Aqua 628. The returned `sqft` (source "Calculated") = the same per-unit registered area
  shown on the unit page (validated live this session). The on-page search box is hard to drive headlessly.
- **Coverage is thin on deep buildings** (The Well 3, CityPlace 3, Library 3, Aqua 4, Ten York 5
  verified) — deepen to 8–12 each next run ("The-Well failure mode"). Quartz/Spectra = 0 verified.
- Marketing-name ≠ condos.ca name: condos.ca "The Well" = vipcondos "Tridel at The Well"; "Aqua" =
  410 Queens Quay W. Always confirm comps by **address**.
- Parking adds little to rent downtown — LINEST C2 = ~$26/spot/mo (most verified comps lease w/o parking).

## Dead-ends (don't re-try)
- vipcondos subject floor plans — none published (pre-construction). Definitive subject SF = developer
  suite-area schedule / registered declaration once released.

## Last touched
- 2026-06-22 — **FULL NO-CAP RE-PULL + PBR-subject scenario** (signed-in condos.ca + vipcondos, live).
  User chose to treat 10 LS as a **purpose-built rental (PBR)** subject this run (overrides vipcondos
  condo classification) → 9 condo comps become cross-product (bridged DOWN to PBR-equiv by ~10%).
  Pulled **EVERY** in-window lease (Jan-2025→now) via the condos.ca Algolia leased index (no per-building
  cap): **1,877 total** across the 9 buildings → **1,068 verified-SF comps** (760 green / 308 cream;
  2 dup index artifacts removed). **809 leases have no published registered area** (excluded, incl. all
  230 Quartz/Spectra — corp still publishes no per-unit sqft*; Route A not re-run). Re-verified index==unit-page
  SF this session: Concord 929=888, Aqua 414=600. **C4 now DERIVED = 5.77%** (vintage spread Concord
  $4.314 / all-comp $4.264 / Aqua $3.909) vs the prior assumed 10%. **Recommended condo-equiv $/SF = $4.555**
  (Concord primary + C4); **PBR-equiv ≈ $4.14/SF** (÷1.10). Was $4.78 on the 107-comp/10%-premium set — drop
  driven by the deeper base + derived (lower) premium. Workbook rebuilt from scratch via build_workbook.py
  (1,068 rows), validate_workbook.py **PASS** (0 formula errors, numpy tie-out, SF coverage 100%). Comp set
  unchanged from 2026-06-16 (user re-confirmed all 9). PBR same-product track searched on rentals.ca
  (25 Lower Simcoe, 30 Grand Trunk, 15 Fort York, 8 Mercer, 39 Niagara, 33 Bay, 16 Yonge) — all asking-only,
  no verified SF, excluded. See `10_Lower_Spadina_Comps_Verification.md` (2026-06-22 entry).
- 2026-06-17 — **LIVE BROWSER RE-PULL** (signed-in condos.ca + vipcondos). Ran the deferred 2026-06-16 browser
  worklist. Deepened comps **39 → 107 verified** (12 per building; N1|N2 11 after de-duping a twice-leased unit):
  95 via condos.ca per-unit registered area (Route B) + **12 Quartz/Spectra via the vipcondos Spectra plan
  dictionary matched by stack (Route A, plate-verified)**. The Well small suites now carry registered areas on
  condos.ca (3 → 12; no Route A needed). Furnished/short-term leases excluded. Recomputed: LINEST parking
  C2 = **$2.27/spot/mo** (very low — downtown), ALL-CONDOS **$4.149/SF**, Concord weighted **$4.344** → +10%
  → **RECOMMENDED subject $/SF $4.78** (was $4.98 on the thinner 39-comp set; premium unchanged 10%). LibreOffice
  recalc 0 errors (2,205 formulas), tied to numpy. Removed the /10 comp-quality scores from Output (per current
  spec). Workbook `_vACTIVE` updated; copy also placed in the "10 LS" folder.
- 2026-06-16 — Audit & structural fix of `10 Lower Spadina Rental Comps _vACTIVE.xlsx` (no data
  changed). 9-comp set, 39 verified-SF condo comps carried from the 2026-06-16 pull. Added Date
  Scraped/AutoFilter, hid gridlines, added live INPUTS/PREMIUM BASIS/MIX BASIS blocks, Output
  recommendation mirror + /10 scores, future-proofed Low/High ranges. Recommended subject $/SF ≈
  **$4.98** (Concord+10%); ALL CONDOS $4.38/SF. Browser deepening worklist outstanding (see
  `10_Lower_Spadina_Comps_Verification.md`).
