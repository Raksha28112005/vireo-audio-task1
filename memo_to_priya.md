# Vireo Audio — Task 1 Memo

## Recommendation

Keep Billing as the candidate for the two requested hires, but do not use raw ticket volume as the only staffing diagnosis. The supplied data shows meaningful Billing service pressure and a high internal-transfer rate, which suggests a process/routing intervention should accompany the hiring decision.

## What the tool does

The prototype reads support tickets, classifies the customer's primary issue from the opening message and agent closing note, and produces monthly category and team volume charts. It also creates a 20-ticket human-review sample and flags cases where the predicted category maps to a different policy-owned team than the first-assigned team.

## Business number

Target: reduce Billing's current-helpdesk transfer rate from 40.6% toward 25%.

At the observed current-helpdesk Billing volume, this is approximately Rs 74K of avoided internal-transfer cost over the observed period, or about Rs 49K annualised. This is a process-saving target, not a claim that the classifier itself creates that saving.

Two agents at the policy's Rs 165/agent-hour and 8-hour shift standard cost roughly Rs 9.64 lakh/year if staffed every day.

## Important context

Across the full Jan 2025–Jun 2026 window, Billing has 2,425 tickets (20.8%). It is not the largest team by raw volume. The policy also says Tier 2 should not be compared with Tier 1 on raw ticket volume.

Billing's current-helpdesk data contains 632 transfers and a 19.7% SLA-breach rate.

## Validation

The existing bot category is not treated as ground truth because the client says those tags may be unreliable. The submission includes a 20-ticket human-review queue. The final submission should report the error rate after those rows are reviewed.

## Limitations

The classifier is a lightweight prototype; the validation sample is small; some tickets are ambiguous; and legacy transfer values are blank. The tool is intended for decision support, not production deployment.
