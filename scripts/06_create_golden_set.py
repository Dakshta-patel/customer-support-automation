from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "processed" / "classified_conversations.csv"
OUTPUT_FILE = ROOT / "data" / "golden_set" / "golden_set_template.csv"


SAMPLES_PER_INTENT = 20


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "Run scripts/05_keyword_classifier.py before creating the golden set."
        )

    df = pd.read_csv(INPUT_FILE)

    sampled_parts = []

    for intent, group in df.groupby("predicted_intent"):
        sample_size = min(SAMPLES_PER_INTENT, len(group))

        sampled_group = group.sample(
            n=sample_size,
            random_state=42
        )

        sampled_parts.append(sampled_group)

    golden = pd.concat(sampled_parts, ignore_index=True)

    golden = golden.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    golden["human_intent"] = ""
    golden["human_handling"] = ""
    golden["human_notes"] = ""

    columns = [
        "customer_message",
        "brand_response",
        "predicted_intent",
        "handling_decision",
        "handling_reason",
        "human_intent",
        "human_handling",
        "human_notes"
    ]

    golden = golden[columns]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    golden.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"Golden-set template created: {OUTPUT_FILE}")
    print(f"Total examples: {len(golden)}")
    print()
    print("Next step:")
    print("Open the CSV and fill in human_intent and human_handling manually.")


if __name__ == "__main__":
    main()