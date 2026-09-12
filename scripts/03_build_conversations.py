import os
import pandas as pd

INPUT_PATH = "data/raw/twcs.csv"
OUTPUT_PATH = "data/processed/amazonhelp_conversations.csv"

BRAND = "AmazonHelp"

print("Loading original dataset...")

# Read the complete dataset in chunks
all_chunks = []

for chunk_number, chunk in enumerate(
    pd.read_csv(
        INPUT_PATH,
        chunksize=100_000,
        low_memory=False
    )
):
    all_chunks.append(chunk)

    print(
        f"Loaded chunk {chunk_number + 1} | "
        f"Rows loaded: {sum(len(c) for c in all_chunks):,}"
    )

df = pd.concat(all_chunks, ignore_index=True)

print(f"\nTotal tweets: {len(df):,}")

# Convert inbound values correctly
df["inbound"] = (
    df["inbound"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({
        "true": True,
        "false": False
    })
)

# Select AmazonHelp replies
brand_replies = df[
    (df["author_id"].astype(str) == BRAND)
    & (df["inbound"] == False)
].copy()

print(f"AmazonHelp replies: {len(brand_replies):,}")

# Select all customer tweets
customer_messages = df[
    df["inbound"] == True
].copy()

print(f"Customer messages: {len(customer_messages):,}")

# Convert IDs to strings
customer_messages["tweet_id"] = (
    pd.to_numeric(
        customer_messages["tweet_id"],
        errors="coerce"
    )
    .astype("Int64")
    .astype(str)
)

brand_replies["in_response_to_tweet_id"] = (
    pd.to_numeric(
        brand_replies["in_response_to_tweet_id"],
        errors="coerce"
    )
    .astype("Int64")
    .astype(str)
)

# Join customer messages to AmazonHelp replies
conversations = customer_messages.merge(
    brand_replies[
        [
            "tweet_id",
            "in_response_to_tweet_id",
            "text",
            "created_at"
        ]
    ],
    left_on="tweet_id",
    right_on="in_response_to_tweet_id",
    how="inner",
    suffixes=("_customer", "_brand")
)

conversations = conversations.rename(
    columns={
        "text_customer": "customer_message",
        "text_brand": "brand_response",
        "created_at_customer": "customer_created_at",
        "created_at_brand": "brand_created_at"
    }
)

conversations = conversations[
    [
        "tweet_id_customer",
        "customer_message",
        "brand_response",
        "customer_created_at",
        "brand_created_at"
    ]
]

conversations = conversations.drop_duplicates()

os.makedirs("data/processed", exist_ok=True)

conversations.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8"
)

print("\nConversation extraction completed.")
print(f"Conversation pairs: {len(conversations):,}")
print(f"Output file: {OUTPUT_PATH}")