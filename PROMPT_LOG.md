# Prompt / AI-use log

Prompts used during analysis included:
1. Inspect the supplied Vireo data pack and identify the decision that matters most to the client.
2. Use the support policy to distinguish ticket ownership, cost standards, SLA breaches and Tier 2 reporting rules.
3. Review a stratified sample of tickets and identify where the bot's category appears to describe the wrong primary issue.
4. Design a lightweight, reproducible categorisation approach that can run locally without paid API calls.
5. Quantify the business effect of Billing transfers and compare that process-saving opportunity with the requested two-hire decision.

Discarded approach:
- A pure TF-IDF classifier trained directly on the existing bot tags was rejected as the primary categoriser because the client explicitly says the tags may be poor; it would learn the same label noise. It remains only as a fallback for ambiguous cases.

Important honesty note:
- The final audit labels are manual review labels, not ground truth from Vireo.
