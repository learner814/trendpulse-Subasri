import pandas as pd
import glob

# Find the JSON file created in Task 1
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in the data folder.")
    exit()

json_file = sorted(json_files)[-1]

# 1. Load JSON into a Pandas DataFrame
df = pd.read_json(json_file)

print("Loaded", len(df), "stories from", json_file)

# 2. Remove duplicate stories using post_id
df = df.drop_duplicates(subset="post_id")
print("After removing duplicates:", len(df))

# 3. Remove rows missing post_id, title, or score
df = df.dropna(subset=["post_id", "title", "score"])
print("After removing nulls:", len(df))

# 4. Convert score and num_comments to integers
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

df = df.dropna(subset=["score", "num_comments"])

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# 5. Remove stories with score less than 5
df = df[df["score"] >= 5]
print("After removing low scores:", len(df))

# 6. Remove extra spaces from titles
df["title"] = df["title"].str.strip()

# 7. Save the cleaned data as CSV
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print()
print("Saved", len(df), "rows to", output_file)

# 8. Print stories per category
print()
print("Stories per category:")
print(df["category"].value_counts())