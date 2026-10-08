import argparse, re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def pred_rule(msg, note):
    s = (str(msg) + " " + str(note)).lower()
    explicit = [
        (r'issue:\s*(mic|microphone|audio|sound|crack|distortion|single side|no audio)', "Audio Quality"),
        (r'issue:\s*(battery|battery drain|charging|no power)', "Charging & Battery"),
        (r'issue:\s*(app|fw|firmware)', "App & Firmware"),
        (r'issue:\s*(pair|pairing|disconnect|connection)', "Connectivity"),
        (r'(device not discoverable|bt dropouts|unable to pari|pairing is not working)', "Connectivity"),
        (r'(otp not received|unable to log|unable to login|cannot login|locked out|login issue)', "Account & Login"),
        (r'(repair status|warranty claim|rma status|service centre took|warranty claim status)', "Warranty & Repair"),
        (r'(delivery query|shipment not rcvd|order not delivered|incorrect product shipped|address update|delivery delayed|transit damage)', "Delivery & Shipping"),
        (r'(invoice|gst invoice|gstin|coupon|discount not applied|payment debited|payment gateway|duplicate or failed payment)', "Billing & Payments"),
        (r'(reverse pickup|refund delay|refund pending|return pickup|cancellation request|cancel order)', "Returns & Refunds"),
        (r'(product enquiry|compatibility query|pre-sales query|compatible w|survive a shower)', "Product Enquiry"),
    ]
    for pattern, category in explicit:
        if re.search(pattern, s):
            return category
    return None

def expected_team(cat, channel):
    if cat == "Delivery & Shipping": return "Logistics"
    if cat == "Billing & Payments": return "Billing"
    if cat == "Returns & Refunds": return "Returns Desk"
    if cat == "Warranty & Repair": return "Escalations & Warranty"
    return {"chat":"Chat Frontline","email":"Email Frontline",
            "voice":"Voice Frontline","social":"Chat Frontline"}.get(channel)

def main(data_dir, out_dir):
    data = Path(data_dir)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    t = pd.read_csv(data / "tickets.csv")
    t["created_at"] = pd.to_datetime(t["created_at"], errors="coerce")
    t["first_response_at"] = pd.to_datetime(t["first_response_at"], errors="coerce")
    t["month"] = t.created_at.dt.to_period("M").astype(str)

    # Use exactly the README's stated analysis window.
    t = t[(t.created_at >= "2025-01-01") & (t.created_at < "2026-07-01")].copy()

    # Local fallback model. The supplied tag is used only as a weak training signal;
    # explicit issue rules take precedence because the brief warns that tags are noisy.
    text = (t.customer_message.fillna("") + " " + t.agent_notes.fillna("")).str.lower()
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2), min_df=2, max_features=40000, sublinear_tf=True
    )
    X = vectorizer.fit_transform(text)
    model = LogisticRegression(max_iter=700, C=2)
    model.fit(X, t.category)

    predicted = []
    method = []
    for _, row in t.iterrows():
        rule = pred_rule(row.customer_message, row.agent_notes)
        if rule:
            predicted.append(rule)
            method.append("rule")
        else:
            s = str(row.customer_message) + " " + str(row.agent_notes)
            predicted.append(model.predict(vectorizer.transform([s]))[0])
            method.append("ml_fallback")

    t["ai_category"] = predicted
    t["classification_method"] = method
    t["expected_team_ai"] = [
        expected_team(c, ch) for c, ch in zip(t.ai_category, t.channel)
    ]
    t["routing_mismatch"] = t.assigned_team != t.expected_team_ai

    t.to_csv(out / "classified_tickets.csv", index=False)

    monthly_category = (
        t.groupby(["month", "ai_category"]).size()
        .unstack(fill_value=0)
        .reset_index()
    )
    monthly_team = (
        t.groupby(["month", "assigned_team"]).size()
        .unstack(fill_value=0)
        .reset_index()
    )
    monthly_category.to_csv(out / "monthly_category.csv", index=False)
    monthly_team.to_csv(out / "monthly_team.csv", index=False)

    # Requested charts.
    for filename, df, title, ylabel in [
        ("monthly_category.png", monthly_category,
         "Vireo Audio — Monthly Ticket Volume by AI Category", "Tickets"),
        ("monthly_team.png", monthly_team,
         "Vireo Audio — Monthly Ticket Volume by Assigned Team", "Tickets"),
    ]:
        plt.figure(figsize=(12, 6))
        for col in df.columns[1:]:
            plt.plot(df["month"], df[col], label=col)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend(ncol=2, fontsize=8)
        plt.tight_layout()
        plt.savefig(out / filename, dpi=160)
        plt.close()

    current_billing = t[
        (t.assigned_team == "Billing") & (t.source_system == "helpdesk")
    ]
    billing = t[t.assigned_team == "Billing"]

    summary = pd.DataFrame([{
        "analysis_window_tickets": len(t),
        "rows_excluded_outside_readme_window": len(pd.read_csv(data/"tickets.csv")) - len(t),
        "billing_tickets": int(len(billing)),
        "billing_share": float(len(billing) / len(t)),
        "billing_current_helpdesk_transfers": float(current_billing["transfers"].sum()),
        "billing_current_transfer_rate": float(current_billing["transfers"].mean()),
        "billing_sla_breach_count": int(billing["first_response_at"].notna().sum()),  # replaced below if SLA fields available
        "routing_mismatch_count": int(t.routing_mismatch.sum()),
        "routing_mismatch_rate": float(t.routing_mismatch.mean()),
    }])

    # SLA breach calculation from policy targets.
    targets = {"chat": 15, "voice": 120, "social": 240, "email": 480}
    t["response_minutes"] = (
        pd.to_datetime(t.first_response_at, errors="coerce")
        - pd.to_datetime(t.created_at, errors="coerce")
    ).dt.total_seconds() / 60
    t["sla_target_minutes"] = t.channel.map(targets)
    t["sla_breach"] = t.response_minutes > t.sla_target_minutes
    summary.loc[0, "billing_sla_breach_count"] = int(
        t.loc[t.assigned_team=="Billing", "sla_breach"].sum()
    )
    summary.loc[0, "billing_sla_breach_rate"] = float(
        t.loc[t.assigned_team=="Billing", "sla_breach"].mean()
    )
    summary.to_csv(out / "summary.csv", index=False)

    # A transparent validation sheet: this is a human-review queue, NOT fabricated ground truth.
    validation = t.sample(min(20, len(t)), random_state=42)[
        ["ticket_id", "customer_message", "agent_notes", "category", "ai_category"]
    ].copy()
    validation["human_check"] = ""
    validation["notes"] = ""
    validation.to_csv(out / "validation_sample.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=".")
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()
    main(args.data, args.out)
