import requests
import pandas as pd
import os

os.makedirs("../datasets", exist_ok=True)

# Products
batch = int(input("Enter batch number: "))
skip = (batch - 1) * 100

products = requests.get(
    f"https://dummyjson.com/products?limit=100&skip={skip}"
).json()["products"]

users = requests.get(
    f"https://dummyjson.com/users?limit=100&skip={skip}"
).json()["users"]

carts = requests.get(
    f"https://dummyjson.com/carts?limit=100&skip={skip}"
).json()["carts"]

products_df = pd.DataFrame(products)
products_df = pd.concat([products_df] * 100, ignore_index=True)
products_df["id"] = range(
    skip * 100 + 1,
    skip * 100 + len(products_df) + 1
)
products_df.loc[0, "price"] = None      # null price
products_df.loc[1, "price"] = -50       # negative price
products_df.loc[2, "title"] = None      # null title
products_df.loc[3, "id"] = products_df.loc[4, "id"]   # duplicate id
users_df = pd.DataFrame(users)
carts_df = pd.DataFrame(carts)

print(f"Products: {len(products_df)}")
print(f"Users: {len(users_df)}")
print(f"Carts: {len(carts_df)}")

products_df.to_csv("../datasets/products.csv", index=False)
users_df.to_csv("../datasets/users.csv", index=False)
carts_df.to_csv("../datasets/carts.csv", index=False)