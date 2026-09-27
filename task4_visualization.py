import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the analysed data from Task 3
df = pd.read_csv("data/trends_analysed.csv")

# Create outputs folder
os.makedirs("outputs", exist_ok=True)


# Chart 1: Top 10 Stories by Score

top_stories = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

plt.figure(figsize=(10, 6))
plt.barh(top_stories["short_title"], top_stories["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("outputs/chart1_top_stories.png")
plt.close()


# Chart 2: Stories per Category

category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 6))
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.tight_layout()

plt.savefig("outputs/chart2_categories.png")
plt.close()


# Chart 3: Score vs Comments

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(10, 6))

plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular"
)

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()
plt.tight_layout()

plt.savefig("outputs/chart3_scatter.png")
plt.close()


# Bonus: Combined Dashboard

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle("TrendPulse Dashboard", fontsize=16)

# Dashboard Chart 1
axes[0, 0].barh(
    top_stories["short_title"],
    top_stories["score"]
)
axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")
axes[0, 0].invert_yaxis()

# Dashboard Chart 2
axes[0, 1].bar(
    category_counts.index,
    category_counts.values
)
axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")

# Dashboard Chart 3
axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular"
)

axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")
axes[1, 0].legend()

# Leave the fourth dashboard space empty
axes[1, 1].axis("off")

plt.tight_layout()

# Save dashboard
plt.savefig("outputs/dashboard.png")
plt.close()


print("Task 4 completed successfully!")
print("Created:")
print("outputs/chart1_top_stories.png")
print("outputs/chart2_categories.png")
print("outputs/chart3_scatter.png")
print("outputs/dashboard.png")
