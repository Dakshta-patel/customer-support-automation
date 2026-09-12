from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)


ROOT = Path(__file__).resolve().parents[1]

GOLDEN_FILE = ROOT / "data" / "golden_set" / "golden_set_labeled.csv"
CLASSIFIED_FILE = ROOT / "data" / "processed" / "classified_conversations.csv"
AGENT_OUTPUT_FILE = ROOT / "data" / "processed" / "support_agent_outputs.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "agent_evaluation.txt"


def evaluate_column(y_true, y_pred, title):
    accuracy = accuracy_score(
        y_true,
        y_pred,
    )

    macro_f1 = f1_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0,
    )

    report = classification_report(
        y_true,
        y_pred,
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_true,
        y_pred,
    )

    return f"""
{title}
{"-" * len(title)}

Accuracy: {accuracy:.4f}
Macro F1: {macro_f1:.4f}

Classification report:
{report}

Confusion matrix:
{matrix}
""".strip()


def validate_agent_output():
    if not AGENT_OUTPUT_FILE.exists():
        return (
            "Agent output validation:\n"
            "support_agent_outputs.csv was not found.\n"
        )

    agent_output = pd.read_csv(
        AGENT_OUTPUT_FILE,
        encoding="utf-8",
    )

    required_columns = [
        "customer_message",
        "predicted_intent",
        "handling_decision",
        "agent_action",
        "agent_response",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in agent_output.columns
    ]

    if missing_columns:
        return (
            "Agent output validation:\n"
            f"Missing columns: {missing_columns}\n"
        )

    empty_response_count = (
        agent_output["agent_response"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    invalid_action_count = (
        ~agent_output["agent_action"].isin(
            [
                "respond",
                "human_review",
            ]
        )
    ).sum()

    return f"""
Agent output validation
-----------------------

Rows generated: {len(agent_output)}
Empty responses: {empty_response_count}
Invalid actions: {invalid_action_count}
Required columns: present
""".strip()


def main():
    if not GOLDEN_FILE.exists():
        raise FileNotFoundError(
            f"Golden set not found: {GOLDEN_FILE}"
        )

    if not CLASSIFIED_FILE.exists():
        raise FileNotFoundError(
            f"Classified file not found: {CLASSIFIED_FILE}"
        )

    golden = pd.read_csv(
        GOLDEN_FILE,
        encoding="utf-8",
    )

    classified = pd.read_csv(
        CLASSIFIED_FILE,
        encoding="utf-8",
    )

    golden = golden.dropna(
        subset=[
            "human_intent",
            "human_handling",
        ]
    ).copy()

    y_true_intent = golden[
        "human_intent"
    ].astype(str)

    y_pred_intent = golden[
        "predicted_intent"
    ].astype(str)

    y_true_handling = golden[
        "human_handling"
    ].astype(str)

    y_pred_handling = golden[
        "handling_decision"
    ].astype(str)

    intent_result = evaluate_column(
        y_true_intent,
        y_pred_intent,
        "INTENT CLASSIFICATION",
    )

    handling_result = evaluate_column(
        y_true_handling,
        y_pred_handling,
        "HANDLING DECISION",
    )

    corpus_majority_intent = (
        classified["predicted_intent"]
        .value_counts()
        .idxmax()
    )

    majority_predictions = [
        corpus_majority_intent
    ] * len(y_true_intent)

    majority_accuracy = accuracy_score(
        y_true_intent,
        majority_predictions,
    )

    mismatch_mask = (
        y_true_handling != y_pred_handling
    )

    mismatches = golden.loc[
        mismatch_mask,
        [
            "customer_message",
            "predicted_intent",
            "handling_decision",
            "human_intent",
            "human_handling",
            "human_notes",
        ],
    ].copy()

    mismatch_text = "No handling mismatches found."

    if not mismatches.empty:
        mismatch_text = mismatches.to_string(
            index=False
        )

    validation_result = validate_agent_output()

    report = f"""
SUPPORT AGENT EVALUATION
========================

Golden set rows evaluated: {len(golden)}

{intent_result}

{handling_result}

MAJORITY BASELINE
-----------------

Corpus majority intent: {corpus_majority_intent}
Majority baseline accuracy: {majority_accuracy:.4f}

HANDLING MISMATCHES
-------------------

Number of handling mismatches: {len(mismatches)}

{mismatch_text}

{validation_result}
"""

    print(report)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_FILE.write_text(
        report.strip() + "\n",
        encoding="utf-8",
    )

    print(
        f"Saved evaluation report to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()