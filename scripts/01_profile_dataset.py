import pandas as pd
from collections import Counter

DATA_PATH = "data/raw/twcs.csv"

print("Reading dataset in chunks...")

total_rows = 0
inbound_rows = 0
outbound_rows = 0
author_counts = Counter()

for chunk_number, chunk in enumerate(
    pd.read_csv(DATA_PATH, chunksize=100_000)
):
    total_rows += len(chunk)

    inbound_rows += int((chunk["inbound"] == True).sum())
    outbound_rows += int((chunk["inbound"] == False).sum())

    author_counts.update(chunk["author_id"].dropna().astype(str))

    print(
        f"Processed chunk {chunk_number + 1} | "
        f"Rows processed: {total_rows:,}"
    )

print("\nDataset summary")
print("----------------")
print(f"Total rows: {total_rows:,}")
print(f"Inbound messages: {inbound_rows:,}")
print(f"Outbound messages: {outbound_rows:,}")

print("\nMost common author IDs")
print("----------------------")

for author_id, count in author_counts.most_common(30):
    print(f"{author_id}: {count:,}")