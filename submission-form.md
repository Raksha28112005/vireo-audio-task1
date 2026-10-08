# Submission Form — Draft

## What did you build, and what business outcome does it move? State the number and the money.

I built a lightweight AI-assisted support-ticket categorisation tool using the customer opening message and agent closing note. It produces monthly category/team breakdowns and flags routing mismatches.

Business target: reduce Billing's current-helpdesk transfer rate from 40.6% toward 25%. At the observed volume, this is approximately Rs 74K over the observed period, or about Rs 49K annualised in avoided internal transfer costs.

## What does one run cost, and what would a month cost at Vireo's volume (roughly 650 tickets a week)? Show the arithmetic. If you used no paid calls, say so.

No paid API calls are required by the submitted tool. It runs locally using scikit-learn.

One run: Rs 0 in model/API calls.
650 tickets/week × 52/12 ≈ 2,817 tickets/month.
2,817 × Rs 0 = Rs 0/month in model/API calls.

## How do you know it works? Sample size, how you checked, error rate, and the kind of case it gets wrong.

I created a 20-ticket human-review sample rather than treating Vireo's existing bot tags as ground truth, because the brief explicitly warns that those tags may be unreliable.

BEFORE SUBMITTING: review the 20 rows in `outputs/validation_sample.csv`, fill the `human_check` column, count mismatches with `ai_category`, and replace this paragraph with the resulting accuracy/error rate.

The known failure mode is ambiguity: closing notes can mention a secondary action (for example a refund or firmware update) that differs from the customer's primary problem.

## Did you change, narrow, or push back on the client's ask? What, when, and why.

Yes. I kept the requested two-hire decision but pushed back on using raw queue size alone as the staffing diagnosis. Billing is not the largest team overall, but it has significant SLA-breach and transfer pressure. I also separated process leakage from genuine staffing demand.

## What is wrong with what you are handing us? Be specific.

- The validation sample is only 20 tickets.
- The gold labels are human spot-check labels, not independently double-annotated ground truth.
- Some borderline tickets remain ambiguous.
- The classifier is lightweight rather than a foundation model.
- Legacy transfer data is unavailable.

## What did you deliberately leave out, and why that rather than something else?

I did not build a production UI, detailed agent-performance scoring, or a full causal staffing model. The five-hour cap makes those lower-value than categorisation, validation, monthly workload analysis, and the staffing/process decision.

## Anything you built or found that nobody asked for?

A routing/process view: category-to-policy ownership mismatches. This helps distinguish genuine workload from tickets arriving in the wrong queue.

## What did you use AI for?

I used ChatGPT to inspect the data pack, reason about the policy, design the taxonomy and validation approach, and iterate on the classifier implementation. The submitted runtime uses local scikit-learn and no paid LLM calls.

Screen recording: [PASTE PUBLIC GOOGLE DRIVE LINK]

## Your Public Google Drive Link

[PASTE LINK]

## Someone picks this up on Monday and you are unreachable. The three things they need to know.

1. Put the five CSV inputs in `data/` using the exact names listed in README.md.
2. Run `python run.py --data ./data --out ./outputs`.
3. Review `validation_sample.csv` before treating the classifier as production-ready; legacy blank transfers are not zeros.

## Honest hours spent.

[ENTER ACTUAL HOURS]

## Github Repo Link

[PASTE PUBLIC REPO URL]
