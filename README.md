# High-Rise Rent-Comp & Price-Triangulation Tool

A reusable, deterministic toolchain for building **rent-comp workbooks** for high-rise
developments (condo *or* purpose-built-rental) and triangulating the rent a subject should
achieve. You assemble verified comp data into a single JSON input; a generator emits a fully
formatted 6-sheet Excel workbook; a validator proves it is correct and reproducible.

The process is **subject-agnostic** — point it at any building by supplying that building's
`comp_data.json`. A complete **worked example (10 Lower Spadina)** is included so you can verify
the toolchain end-to-end.

## How it works (any subject)

```bash
pip install -r requirements.txt

# 1. Assemble <subject>.json conforming to comp_data.schema.json  (VERIFIED comps only)
# 2. Generate the workbook:
python build_workbook.py comp_data.json "<Subject> Rental Comps _vACTIVE.xlsx"
# 3. Validate (structure, zero-error recalc, numpy tie-out, SF coverage):
python validate_workbook.py "<Subject> Rental Comps _vACTIVE.xlsx" comp_data.json
```

- **`build_workbook.py`** is the single source of truth for workbook structure and every formula.
  It reads a `comp_data.json` (the input contract) and writes the `.xlsx` deterministically.
- **`validate_workbook.py`** asserts the 6-sheet structure, recalculates every formula to **zero
  errors**, ties the averages/blocks to an independent numpy recomputation, and checks **SF
  coverage** (every leased-in-window unit has a verified SF or a documented exhaustion record).
  A green **PASS** means the workbook reproduces exactly from its inputs.
- **`comp_data.schema.json`** is the input contract; **`comp_data.example.json`** is a filled
  template. **`CLAUDE.md`** is the full operating method (triangulation logic, SF-verification
  rules, output spec); **`condo_sqft_verification_method_1.md`** details the SF methodology.

## Core (reusable tool)

| File | Purpose |
|---|---|
| `build_workbook.py` | Workbook generator — owns all structure & formulas |
| `validate_workbook.py` | Validator — structure, zero-error recalc, numpy tie-out, SF coverage |
| `comp_data.schema.json` | Input contract |
| `comp_data.example.json` | Filled example input (template) |
| `CLAUDE.md` | Operating method / triangulation + verification rules + output spec |
| `condo_sqft_verification_method_1.md` | SF-verification methodology |
| `v2 Format Conformance — what was missing + target spec.md` | Format spec |
| `requirements.txt` | `openpyxl`, `formulas`, `numpy` |

## Included worked example — 10 Lower Spadina (PBR scenario)

Reproduce it exactly:

```bash
python build_workbook.py comp_data.json "10 Lower Spadina Rental Comps _vACTIVE.xlsx"
python validate_workbook.py "10 Lower Spadina Rental Comps _vACTIVE.xlsx" comp_data.json
```

- **`comp_data.json`** — the example input: **1,068 verified-SF leased comps** across 9 nearby
  buildings, pulled with **no per-building cap** (every in-window lease, Jan 2025 → Jun 2026).
- **`10 Lower Spadina Rental Comps _vACTIVE.xlsx`** — the generated workbook.
- **`10_Lower_Spadina_Comps_Verification.md`** — full provenance log.
- **`building_memory/`** — cross-session notes (the tool's memory system) for this example.

Result: recommended **$4.555/SF** condo-equivalent (primary comp + a *derived* 5.77% new-build
premium); for the PBR subject, achievable rent bridges **down** by the ~10% condo→PBR premium to
**≈ $4.14/SF**.

## Notes & disclaimers

- **Redactions:** internal SharePoint coordinates for the originating organization were removed
  from `CLAUDE.md` (`[REDACTED-*]`), and unrelated projects were excluded from this repo.
- **Data:** the example comp records are factual lease data derived from condos.ca for analysis;
  re-use is subject to the source site's terms. Provided for reproducibility of the analysis, not
  redistribution of a listing service.
