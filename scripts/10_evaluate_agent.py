from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, f1_score


ROOT = Path(__file__).resolve().parents[1]

GOLDEN_FILE = ROOT / "data" / "golden_set" / "golden_set_labeled.csv"
CLASSIFIED_FILE = ROOT / "data" / "processed" / "classified_conversations.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "agent_evaluation.txt"


def main():
    golden = pd.read_csv(GOLDEN_FILE, encoding="utf-8")
    classified = pd.read_csv(CLASSIFIED_FILE, encoding="utf-8")

    # Remove rows without manual labels.
    golden = golden.dropna(subset=["human_intent", "human_handling"]).copy()

    # ---------------------------------------------------------
    # Intent classification evaluation
    # ---------------------------------------------------------
    y_true_intent = golden["human_intent"].astype(str)
    y_pred_intent = golden["predicted_intent"].astype(str)

    intent_accuracy = accuracy_score(y_true_intent, y_pred_intent)
    intent_macro_f1 = f1_score(
        y_true_intent,
        y_pred_intent,
        average="macro",
        zero_division=0,
    )

    intent_report = classification_report(
        y_true_intent,
        y_pred_intent,
        zero_division=0,
    )

    # ---------------------------------------------------------
    # Handling decision evaluation
    # ---------------------------------------------------------
    y_true_handling = golden["human_handling"].astype(str)
    y_pred_handling = golden["handling_decision"].astype(str)

    handling_accuracy = accuracy_score(
        y_true_handling,
        y_pred_handling,
    )

    handling_macro_f1 = f1_score(
        y_true_handling,
        y_pred_handling,
        average="macro",
        zero_division=0,
    )

    handling_report = classification_report(
        y_true_handling,
        y_pred_handling,
        zero_division=0,
    )

    # ---------------------------------------------------------
    # Corpus-level intent distribution
    # ---------------------------------------------------------
    corpus_majority_intent = (
        classified["predicted_intent"]
        .value_counts()
        .idxmax()
    )

    golden_majority_accuracy = accuracy_score(
        y_true_intent,
        [corpus_majority_intent] * len(y_true_intent),
    )

    # ---------------------------------------------------------
    # Save report
    # ---------------------------------------------------------
    report = f"""
SUPPORT AGENT EVALUATION
========================

Golden set rows evaluated: {len(golden)}

INTENT CLASSIFICATION
---------------------
Accuracy: {intent_accuracy:.4f}
Macro F1: {intent_macro_f1:.4f}

Classification report:
{intent_report}

HANDLING DECISION
-----------------
Accuracy: {handling_accuracy:.4f}
Macro F1: {handling_macro_f1:.4f}

Classification report:
{handling_report}

BASELINE
--------
Corpus majority intent: {corpus_majority_intent}
Majority baseline accuracy on golden set: {golden_majority_accuracy:.4f}
"""

    print(report)

    OUTPUT_FILE.write_text(
        report.strip() + "\n",
        encoding="utf-8",
    )

    print(f"Saved evaluation report to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()