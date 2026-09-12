import json
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "processed" / "amazonhelp_conversations.csv"
INTENT_FILE = ROOT / "data" / "processed" / "intent_definitions.json"
OUTPUT_FILE = ROOT / "data" / "processed" / "classified_conversations.csv"


INTENT_KEYWORDS = {
    "delivery_date_confusion": [
        "delivery date",
        "arrive date",
        "arrival date",
        "expected date",
        "promised date",
        "date changed",
        "later date",
        "one day delivery",
        "two day delivery"
    ],
    "delivery_issue": [
        "delivery",
        "delivered",
        "package",
        "parcel",
        "shipment",
        "tracking",
        "courier",
        "out for delivery",
        "not arrived",
        "not received",
        "where is my order",
        "missing order",
        "late"
    ],
    "refund_cancellation": [
        "refund",
        "money back",
        "cancel",
        "cancellation",
        "cancelled",
        "reimburse",
        "return my money"
    ],
    "product_replacement": [
        "defective",
        "damaged",
        "broken",
        "replacement",
        "replace",
        "wrong item",
        "missing item",
        "not working",
        "faulty",
        "damaged product"
    ],
    "prime_membership_billing": [
        "prime",
        "free trial",
        "membership",
        "subscription",
        "renewal",
        "renewed",
        "charged",
        "charge",
        "billing",
        "payment"
    ],
    "account_order_privacy": [
        "account",
        "login",
        "log in",
        "password",
        "order number",
        "order no",
        "personal information",
        "private information",
        "privacy",
        "security",
        "details"
    ],
    "technical_device_issue": [
        "alexa",
        "echo",
        "device",
        "app",
        "application",
        "website",
        "server",
        "error",
        "crash",
        "not opening",
        "technical",
        "bug"
    ],
    "digital_content_support": [
        "prime video",
        "video",
        "kindle",
        "ebook",
        "e-book",
        "digital content",
        "streaming",
        "movie",
        "episode"
    ],
    "general_feedback": []
}


ESCALATION_KEYWORDS = [
    "refund",
    "cancel",
    "charged",
    "charge",
    "billing",
    "payment",
    "account",
    "password",
    "privacy",
    "security",
    "personal information",
    "order number",
    "unauthorized",
    "not my order",
    "wrong product",
    "wrong item",
    "missing item",
    "call me",
    "phone",
    "dm",
    "direct message",
]

def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def predict_intent(text):
    text = normalize_text(text)

    scores = {}

    for intent, keywords in INTENT_KEYWORDS.items():
        score = 0
        matched_keywords = []

        for keyword in keywords:
            if keyword in text:
                score += 1
                matched_keywords.append(keyword)

        scores[intent] = {
            "score": score,
            "matched_keywords": matched_keywords
        }

    best_intent = max(
        scores,
        key=lambda intent: (
            scores[intent]["score"],
            -list(INTENT_KEYWORDS.keys()).index(intent)
        )
    )

    if scores[best_intent]["score"] == 0:
        best_intent = "general_feedback"

    return best_intent, scores[best_intent]["matched_keywords"]


def decide_handling(text, intent):
    text = normalize_text(text)

    for keyword in ESCALATION_KEYWORDS:
        if keyword in text:
            return (
                "escalate",
                f"Message contains sensitive or account-related keyword: '{keyword}'"
            )

    # Escalate high-risk Prime, payment, and order situations.
    high_risk_phrases = [
        "not showing in the list while making payment",
        "trying to take payment",
        "not a free trial",
        "wrong product",
        "wrong item",
        "missing episodes",
        "unfinished season",
        "slow delivery",
        "prime shipping",
        "prime versand",
        "waiting for",
        "changed to wednesday",
    ]

    for phrase in high_risk_phrases:
        if phrase in text:
            return (
                "escalate",
                f"Message contains high-risk support phrase: '{phrase}'"
            )

    if intent in {
        "account_order_privacy",
        "technical_device_issue",
        "product_replacement",
        "digital_content_support",
    }:
        return (
            "escalate",
            f"{intent} may require account verification or detailed troubleshooting"
        )

    return (
        "auto_handle",
        "Common low-risk support question suitable for an initial automated response"
    )


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    if not INTENT_FILE.exists():
        raise FileNotFoundError(f"Intent file not found: {INTENT_FILE}")

    with open(INTENT_FILE, "r", encoding="utf-8") as file:
        intent_definitions = json.load(file)

    print(f"Loaded {len(intent_definitions)} intent definitions")

    df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8",
    )

    required_columns = {
        "customer_message",
        "brand_response"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    predicted_intents = []
    matched_keywords_list = []
    handling_decisions = []
    handling_reasons = []

    for message in df["customer_message"]:
        intent, matched_keywords = predict_intent(message)
        decision, reason = decide_handling(message, intent)

        predicted_intents.append(intent)
        matched_keywords_list.append(", ".join(matched_keywords))
        handling_decisions.append(decision)
        handling_reasons.append(reason)

    df["predicted_intent"] = predicted_intents
    df["matched_keywords"] = matched_keywords_list
    df["handling_decision"] = handling_decisions
    df["handling_reason"] = handling_reasons

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print()
    print("Classification completed")
    print(f"Rows processed: {len(df):,}")
    print(f"Output file: {OUTPUT_FILE}")

    print()
    print("Intent distribution:")
    print(df["predicted_intent"].value_counts())

    print()
    print("Handling distribution:")
    print(df["handling_decision"].value_counts())


if __name__ == "__main__":
    main()
