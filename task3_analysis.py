import pandas as pd
import numpy as np

# Load the cleaned data created in Task 2
df = pd.read_csv("data/trends_clean.csv")

# 1. Load and explore the data
print("Loaded data:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

# Calculate average score and average comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print("\nAverage score   :", round(average_score, 2))
print("Average comments:", round(average_comments, 2))


# 2. Basic analysis using NumPy

scores = np.array(df["score"])

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print("Mean score   :", round(mean_score, 2))
print("Median score :", round(median_score, 2))
print("Std deviation:", round(std_score, 2))
print("Max score    :", max_score)
print("Min score    :", min_score)

# Find the category with the most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_category_count = category_counts.max()

print("\nMost stories in:", top_category,
      "(", top_category_count, "stories)")

# Find the story with the most comments
most_commented = df.loc[df["num_comments"].idxmax()]

print("\nMost commented story:",
      most_commented["title"],
      "—", most_commented["num_comments"], "comments")


# 3. Add the two required columns

# Engagement shows comments compared with the score
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# A story is popular when its score is above the average score
df["is_popular"] = df["score"] > average_score


# 4. Save the updated DataFrame
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print("\nSaved to", output_file)
