import pandas as pd

INPUT_PATH = "data/processed/amazonhelp_conversations.csv"

df = pd.read_csv(
    INPUT_PATH,
    encoding="utf-8",
    low_memory=False
)

print(f"Total conversation pairs: {len(df):,}")

print("\nSample customer messages and responses")
print("--------------------------------------")

sample = df.sample(
    n=min(30, len(df)),
    random_state=42
)

for index, row in sample.iterrows():
    print("\n" + "=" * 80)
    print("CUSTOMER:")
    print(row["customer_message"])

    print("\nAMAZONHELP:")
    print(row["brand_response"])