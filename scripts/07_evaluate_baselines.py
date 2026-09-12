import os
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

GOLDEN_PATH = "data/golden_set/golden_set_labeled.csv"
OUTPUT_PATH = "data/processed/baseline_evaluation.txt"


def evaluate_model(name, y_true, y_pred):
    print(f"\n{'=' * 60}")
    print(name)
    print(f"{'=' * 60}")

    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0,
    )

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Macro F1 : {macro_f1:.4f}")
    print("\nClassification report:")
    print(
        classification_report(
            y_true,
            y_pred,
            zero_division=0,
        )
    )

    return accuracy, macro_f1


def main():
    if not os.path.exists(GOLDEN_PATH):
        raise FileNotFoundError(
            f"Golden set not found: {GOLDEN_PATH}"
        )

    df = pd.read_csv(GOLDEN_PATH)

    required_columns = [
        "human_intent",
        "predicted_intent",
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    df = df.dropna(subset=["human_intent"])

    y_true = df["human_intent"].astype(str)

    # Baseline 1: existing keyword classifier
    keyword_predictions = df["predicted_intent"].astype(str)

    # Baseline 2: majority-class classifier
    majority_intent = y_true.value_counts().index[0]
    majority_predictions = [
        majority_intent
        for _ in range(len(y_true))
    ]

    results = []

    accuracy, macro_f1 = evaluate_model(
        "Keyword Classifier Baseline",
        y_true,
        keyword_predictions,
    )

    results.append(
        f"Keyword Classifier Baseline\n"
        f"Accuracy: {accuracy:.4f}\n"
        f"Macro F1: {macro_f1:.4f}\n"
    )

    accuracy, macro_f1 = evaluate_model(
        "Majority-Class Baseline",
        y_true,
        majority_predictions,
    )

    results.append(
        f"Majority-Class Baseline\n"
        f"Majority intent: {majority_intent}\n"
        f"Accuracy: {accuracy:.4f}\n"
        f"Macro F1: {macro_f1:.4f}\n"
    )

    os.makedirs(
        os.path.dirname(OUTPUT_PATH),
        exist_ok=True,
    )

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write("\n\n".join(results))

    print("\nEvaluation saved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()