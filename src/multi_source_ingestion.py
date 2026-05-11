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
users_df = pd.DataFrame(users)
carts_df = pd.DataFrame(carts)

print(f"Products: {len(products_df)}")
print(f"Users: {len(users_df)}")
print(f"Carts: {len(carts_df)}")

products_df.to_csv("../datasets/products.csv", index=False)
users_df.to_csv("../datasets/users.csv", index=False)
carts_df.to_csv("../datasets/carts.csv", index=False)