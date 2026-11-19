# intellectualSysLab1

A fuzzy-logic **expert system that recommends a car** (Intelligent Systems lab 1, 2020). A Tk
window asks eight questions, the answers go through fuzzification, a rule base and
defuzzification, and the two best matches are shown as concrete models.

## Run

```sh
python3 app.py      # from the repo root: it reads questions/, responses/, source/ by relative path
```

Python 3 with Tk, standard library only. The interface is in Russian.

## How it works

| Step | Where | What |
|---|---|---|
| Questions | `questions/*.json` | body type, budget, condition, gearbox, make, passengers, purpose, year; each answer has a score 0-100 |
| Fuzzification | `source/convertion.json` | maps each criterion's options to membership values 0-1 |
| Rules | `ExpertSystem.apply_rule_base` | for every answer, take the 2 closest options (`_ITERATIONS = 2`) |
| Aggregation | `aggregate` | average per criterion |
| Defuzzification | `dephasifier` | pick option indexes and weights (1 - distance); their product ranks the result |
| Answer | `responses/<code>.json` | the option-index code (e.g. `11501212`) names a file with matching cars |

`source/compare.json` holds per-purpose preferences (family, sport, …) used by the window.

Decisions: [docs/adr](docs/adr/README.md).
