import os
import pandas as pd


INPUT_PATH = "data/processed/classified_conversations.csv"
OUTPUT_PATH = "data/processed/support_agent_outputs.csv"


ESCALATION_RESPONSES = {
    "delivery_issue": (
        "Sorry about the delivery issue. Please contact private support "
        "so the delivery status and order details can be checked."
    ),
    "delivery_date_confusion": (
        "Sorry for the confusion about the delivery date. Please contact "
        "private support if the estimated date has passed or needs review."
    ),
    "refund_cancellation": (
        "Sorry for the inconvenience. Please contact private support so "
        "your refund or cancellation request can be reviewed."
    ),
    "product_replacement": (
        "Sorry that the product did not meet your expectations. Please "
        "contact private support so replacement options can be checked."
    ),
    "prime_membership_billing": (
        "Sorry for the membership or billing issue. Please contact private "
        "support so the account and billing details can be reviewed."
    ),
    "account_order_privacy": (
        "For your security, please do not share account or order details "
        "publicly. Contact private support for account-specific assistance."
    ),
    "technical_device_issue": (
        "Sorry you are experiencing a technical issue. Please contact "
        "private support and include the relevant device or service details."
    ),
    "digital_content_support": (
        "Sorry for the trouble with digital content. Please contact private "
        "support with the relevant content or account details."
    ),
    "general_feedback": (
        "Thank you for sharing your feedback. We are sorry for the "
        "inconvenience and appreciate you bringing this to our attention."
    ),
}


AUTO_RESPONSES = {
    "delivery_issue": (
        "Sorry about the delivery issue. Please check the latest tracking "
        "information in your order details."
    ),
    "delivery_date_confusion": (
        "Please check the estimated delivery date shown in your order "
        "details. Delivery dates can change as tracking updates."
    ),
    "refund_cancellation": (
        "Please check your order details for the latest refund or "
        "cancellation status. Processing times may vary."
    ),
    "product_replacement": (
        "Please check the order details and available return or replacement "
        "options for the product."
    ),
    "prime_membership_billing": (
        "Please review your membership and billing details in your account. "
        "Check the relevant membership help options if needed."
    ),
    "account_order_privacy": (
        "For your security, please avoid sharing account or order details "
        "publicly. Use private support for account-specific questions."
    ),
    "technical_device_issue": (
        "Please try the relevant troubleshooting steps for your device or "
        "service and check the official help section for further guidance."
    ),
    "digital_content_support": (
        "Please check the digital-content help section and try again after "
        "reviewing the relevant playback or access settings."
    ),
    "general_feedback": (
        "Thank you for sharing your feedback. We are sorry for the "
        "inconvenience and appreciate you bringing this to our attention."
    ),
}


def generate_response(intent, handling):
    if handling == "escalate":
        return ESCALATION_RESPONSES.get(
            intent,
            "Please contact private support for further assistance.",
        )

    return AUTO_RESPONSES.get(
        intent,
        "Thank you for contacting support. Please check the relevant "
        "help section for the next steps.",
    )


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(
            f"Input file not found: {INPUT_PATH}"
        )

    df = pd.read_csv(
        INPUT_PATH,
        encoding="utf-8",
    )

    required_columns = [
        "customer_message",
        "predicted_intent",
        "handling_decision",
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    df["agent_response"] = df.apply(
        lambda row: generate_response(
            row["predicted_intent"],
            row["handling_decision"],
        ),
        axis=1,
    )

    df["agent_action"] = df["handling_decision"].map(
        {
            "auto_handle": "respond",
            "escalate": "human_review",
        }
    )

    output_columns = [
        "tweet_id_customer",
        "customer_message",
        "predicted_intent",
        "handling_decision",
        "agent_action",
        "agent_response",
    ]

    output_columns = [
        column
        for column in output_columns
        if column in df.columns
    ]

    result = df[output_columns]

    os.makedirs(
        os.path.dirname(OUTPUT_PATH),
        exist_ok=True,
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8",
    )

    print(f"Generated {len(result)} agent outputs.")
    print(f"Saved to: {OUTPUT_PATH}")

    print("\nHandling distribution:")
    print(result["handling_decision"].value_counts())

    print("\nSample outputs:")
    print(
        result[
            [
                "predicted_intent",
                "handling_decision",
                "agent_action",
                "agent_response",
            ]
        ].head(10).to_string(index=False)
    )


if __name__ == "__main__":
    main()