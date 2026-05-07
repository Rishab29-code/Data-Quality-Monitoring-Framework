import requests
import pandas as pd
import random

url = "https://fakestoreapi.com/products"

response = requests.get(url)
data = response.json()

all_data = []

# replicate data to create ~10,000 records
for i in range(500):
    for item in data:
        new_item = item.copy()
        new_item["id"] = item["id"] + (i * 1000)
        all_data.append(new_item)

df = pd.DataFrame(all_data)

# Inject validation errors

# 5% null prices
null_price_idx = random.sample(range(len(df)), int(len(df) * 0.05))
df.loc[null_price_idx, "price"] = None

# 3% negative prices
negative_price_idx = random.sample(range(len(df)), int(len(df) * 0.03))
df.loc[negative_price_idx, "price"] = -50

# 2% duplicate ids
duplicate_idx = random.sample(range(1, len(df)), int(len(df) * 0.02))
for idx in duplicate_idx:
    df.loc[idx, "id"] = df.loc[idx - 1, "id"]

# 4% blank titles
blank_title_idx = random.sample(range(len(df)), int(len(df) * 0.04))
df.loc[blank_title_idx, "title"] = ""

print(f"Generated {len(df)} records")
print(df.head())

df.to_csv("../datasets/raw_products.csv", index=False)