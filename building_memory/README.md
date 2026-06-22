# Building Memory — stable facts only

Persistent, cross-session memory for this square-footage verification agent. It exists to
save you from re-hunting the same building from scratch on every run. It does **not** store
reportable square footage.

## The one rule that keeps this safe

Memory is a **map, not proof.** It tells you *where* the readable plans live and *what* to
expect — it NEVER substitutes for opening the source this session. Every SF number you
report must still name a URL you opened **this session** and state what you saw on it,
exactly as the methodology requires. A value remembered from a past session is a hint to
confirm, never an answer to copy into output.

## What goes in memory (safe — these don't change)

- **Building identity:** marketing name, developer, address(es), storeys, total units, year.
- **Working sources:** the exact vipcondos / aggregator URLs where readable floor plans and
  key-plates actually live, so you don't re-hunt. Note what each page shows.
- **Plan dictionary:** named plans with beds/baths (+den), exposure, terrace/balcony, and the
  plate interior SF — recorded as *expected values to confirm on the sheet*, not as unit answers.
- **Key-plate / stacking notes:** floor bands, band breaks, stack→plan mapping observations.
- **Dead-ends:** sources that were useless (watermarked-only, gated, no key-plate) — don't re-try.
- **Gotchas:** e.g. building spans two addresses; floor 4 or 13 doesn't exist; terrace band.

## What NEVER goes in memory

- A unit's reportable interior SF as a finished answer.
- Anything you would copy into output without re-opening the source this session.

## How to use it

1. **Start of a building:** scan `INDEX.md`. If the building is on file, open its memory file
   and use it to jump straight to the working plans — then verify each unit as normal.
2. **End of a building:** create/update its file from `_TEMPLATE.md` with any new stable facts,
   working URLs, dead-ends, and gotchas. Add or refresh its line in `INDEX.md`.
3. **Never let memory shortcut per-unit verification.** Re-read the plan source each session.
   **But before you BLANK a leased-in-window unit, the working key-plate URLs stored here MUST
   be consulted as part of the SF ladder** (the unit's own condos.ca page → its free-text
   description → these key-plates). Memory exists to make that Route A rung cheap; skipping it
   is exactly the gap that left resolvable units blank. A blank is valid only once the ladder —
   including the remembered key-plates — is spent.
4. **Updates are append-only — never rewrite the dated record.** "Update" means **add a new
   dated entry** under the current date; do **not** overwrite or delete a prior dated line. Keep
   each earlier "Last touched" / run-log entry intact and add the new run beneath it. If a fact
   has changed, write a new dated entry saying what changed and why it supersedes the old — the
   old dated line stays as the record of what was known then. Only a fact proven outright wrong
   is removed, and even then note the dated correction rather than silently erasing it. New dates
   carry only new info; they never edit prior dates.

No downloads — everything here is captured by reading pages in the browser.
