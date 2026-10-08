# Vireo Audio — Task 1

## What this does

This is a small AI-assisted support-ticket analysis tool.

It:
1. Reads the supplied ticket CSV.
2. Classifies tickets using the customer opening message + agent closing note.
3. Produces monthly ticket volume by AI category.
4. Produces monthly ticket volume by assigned team.
5. Produces the requested charts.
6. Creates a human-review validation sample.
7. Flags category/team ownership mismatches using the support policy.

## Run from a clean machine

Put these five files inside `data/` with these exact names:

- `tickets.csv`
- `agents.csv`
- `customers.csv`
- `orders.csv`
- `products.csv`

Then:

```bash
pip install -r requirements.txt
python run.py --data ./data --out ./outputs
```

Windows:

```powershell
python -m pip install -r requirements.txt
python run.py --data .\data --out .\outputs
```

## Outputs

- `classified_tickets.csv` — one row per ticket with `ai_category`
- `monthly_category.csv` — monthly category volume
- `monthly_team.csv` — monthly team volume
- `monthly_category.png` — requested category chart
- `monthly_team.png` — requested team chart
- `summary.csv` — headline business metrics
- `validation_sample.csv` — 20-ticket human review queue

## Validation

The validation sample is deliberately presented as a human-review queue. Do not treat the existing bot category as ground truth because the client says the tags may be unreliable.

For the assessment, review the 20 rows in `validation_sample.csv` and fill `human_check` with the category you believe is correct. Use this to report the observed spot-check error rate.

## Scope decisions

- Analysis window is exactly 1 Jan 2025 through 30 Jun 2026, matching the README.
- Legacy blank transfer values are not treated as zero.
- Tier 2 is not compared with Tier 1 on raw ticket volume, per policy.
- The classifier is intentionally lightweight; it is a decision-support prototype, not a production deployment.
