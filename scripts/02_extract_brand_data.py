import os
import pandas as pd

DATA_PATH = "data/raw/twcs.csv"
OUTPUT_PATH = "data/processed/amazonhelp_tweets.csv"

BRAND = "AmazonHelp"

os.makedirs("data/processed", exist_ok=True)

selected_chunks = []
total_selected = 0

print(f"Extracting tweets for {BRAND}...")

for chunk_number, chunk in enumerate(
    pd.read_csv(DATA_PATH, chunksize=100_000)
):
    brand_rows = chunk[chunk["author_id"].astype(str) == BRAND].copy()

    if not brand_rows.empty:
        selected_chunks.append(brand_rows)
        total_selected += len(brand_rows)

    print(
        f"Processed chunk {chunk_number + 1} | "
        f"Selected rows: {total_selected:,}"
    )

if selected_chunks:
    result = pd.concat(selected_chunks, ignore_index=True)
    result.to_csv(OUTPUT_PATH, index=False)

    print("\nExtraction completed.")
    print(f"Rows saved: {len(result):,}")
    print(f"Output file: {OUTPUT_PATH}")
else:
    print("No rows found for the selected brand.")