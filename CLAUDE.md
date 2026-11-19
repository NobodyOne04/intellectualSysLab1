# intellectualSysLab1

A 2020 university lab: fuzzy expert system that recommends cars, Tk GUI, Russian UI.

## Commands
- `python3 app.py` from the repo root (relative paths). Standard library + Tk. No tests.

## Layout
- `app.py`: Tk window, question flow (next / back), result display.
- `expert.py`: `ExpertSystem`: fuzzification, rule base, aggregation, defuzzification.
- `questions/*.json`: one question each (`title`, answer → score); file order is question order.
- `source/convertion.json`: membership values; `source/compare.json` (read as cp1251): purpose preferences.
- `responses/<code>.json`: car lists for the codes the system can produce.
- `docs/adr/`: decision records (`.adr`), index in `docs/adr/README.md`.

## Conventions
- Read the ADR before changing a recorded decision; commit subjects carry its number.
- A new answer option needs entries in `questions/`, `source/convertion.json` and, for new
  codes, a `responses/<code>.json`.
- `nsumber_of_passengers` is misspelled in file and key names; renaming breaks the lookups.
- Archived lab: docs or small fixes only unless asked.
