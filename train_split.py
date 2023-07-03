import json
import pandas as pd
from sklearn.model_selection import train_test_split


data = []
with open("sentence_data copy.jsonl", "r") as file:
    for line in file:
        try:
            line = line.strip()
            item = json.loads(line)
            if 'sentence' in item and 'type' in item:
                data.append(item)
        except json.JSONDecodeError as e:
            print(f"Skipping problematic line: {line}")
            print(f"Error message: {e}")
            continue

if not data:
    print("No data has been loaded. Please check your dataset.")
    exit()

df = pd.DataFrame(data)

# Remove duplicates
df = df.drop_duplicates()

# Splitting the data
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

# Saving
train_df.to_json("train.jsonl", orient="records", lines=True)
val_df.to_json("val.jsonl", orient="records", lines=True)

