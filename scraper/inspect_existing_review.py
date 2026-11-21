import csv
from collections import Counter

with open("outputs/landin_review.csv", "r", encoding="utf-8") as f:
    review_rows = list(csv.DictReader(f))

print(f"Total review rows currently: {len(review_rows)}")

# Let's inspect unique product names in landin_review.csv
rev_names = Counter(r["product_name"] for r in review_rows)
print("Product names in landin_review.csv:")
for name, cnt in rev_names.most_common():
    print(f"  {name}: {cnt}")
