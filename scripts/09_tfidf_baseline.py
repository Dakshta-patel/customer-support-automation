from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


ROOT = Path(__file__).resolve().parents[1]

GOLDEN_FILE = ROOT / "data" / "golden_set" / "golden_set_labeled.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "tfidf_baseline_report.txt"


def build_classifier():
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    ngram_range=(1, 2),
                    min_df=1,
                    max_features=20000,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def evaluate_target(df, target_column):
    data = df[
        [
            "customer_message",
            target_column,
        ]
    ].dropna()

    data = data[
        data[target_column].astype(str).str.strip() != ""
    ].copy()

    x = data["customer_message"].astype(str)
    y = data[target_column].astype(str)

    if y.nunique() < 2:
        return (
            f"{target_column}\n"
            f"Not enough classes for evaluation.\n"
        )

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = build_classifier()
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)
    macro_f1 = f1_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0,
    )

    report = classification_report(
        y_test,
        predictions,
        zero_division=0,
    )

    result = f"""
{target_column}
{"=" * len(target_column)}

Training rows: {len(x_train)}
Testing rows: {len(x_test)}

Accuracy: {accuracy:.4f}
Macro F1: {macro_f1:.4f}

Classification report:
{report}
"""

    return result.strip()


def main():
    if not GOLDEN_FILE.exists():
        raise FileNotFoundError(
            f"Golden set not found: {GOLDEN_FILE}"
        )

    df = pd.read_csv(
        GOLDEN_FILE,
        encoding="utf-8",
    )

    required_columns = [
        "customer_message",
        "human_intent",
        "human_handling",
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    df = df.dropna(
        subset=[
            "customer_message",
            "human_intent",
            "human_handling",
        ]
    ).copy()

    intent_result = evaluate_target(
        df,
        "human_intent",
    )

    handling_result = evaluate_target(
        df,
        "human_handling",
    )

    report = f"""
TF-IDF BASELINE EVALUATION
==========================

This baseline uses TF-IDF word and bigram features with
Logistic Regression.

Important:
The golden set is used only as a small development dataset.
The results should not be interpreted as production performance.

{intent_result}

{handling_result}
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
        f"Saved TF-IDF baseline report to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()