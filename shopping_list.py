from requests import get
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.environ.get("BASE_URL")
headers = {
    "GROCY-API-KEY": os.environ.get("API_KEY")
}

shopping_list = get(f"{BASE_URL}/objects/shopping_list", headers=headers).json()
units = get(f"{BASE_URL}/objects/quantity_units", headers=headers).json()
products = get(f"{BASE_URL}/objects/products", headers=headers).json()
product_groups = get(f"{BASE_URL}/objects/product_groups", headers=headers).json()

parsed_units = {}
for item in units:
    parsed_units[item["id"]] = item["name"]

parsed_products = {}
for item in products:
    parsed_products[item["id"]] = {"name": item["name"], "product_group_id": item["product_group_id"]}

parsed_product_groups = {}
for item in product_groups:
    parsed_product_groups[item["id"]] = item["name"]

compressed_list = {}
for item in shopping_list:
    product_id = item["product_id"]
    if product_id in compressed_list:
        compressed_list[product_id]["amount"] = compressed_list[product_id]["amount"] + float(item["amount"])
    else:
        compressed_list[product_id] = {"amount": float(item["amount"]), "unit": item["qu_id"]}

pretty_list = {}
for item in compressed_list.items():
    product = parsed_products[item[0]]
    name = product["name"].replace("*", "")
    product_group = parsed_product_groups[product["product_group_id"]]
    amount = item[1]["amount"]
    unit = parsed_units[item[1]["unit"]]

    pretty_list[name] = {"amount": amount, "unit": unit, "product_group": product_group}

data = ""
for item in pretty_list.items():
    data = data + item[0] + "," + str(item[1]["amount"]) + "," + item[1]["unit"] + "," + item[1]["product_group"] + "\n"

with open("shopping_list.csv", "w") as f:
    f.write(data)
    f.close()