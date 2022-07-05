import grequests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.environ.get("BASE_URL")
headers = {
    "GROCY-API-KEY": os.environ.get("API_KEY")
}

urls = [
    "/objects/shopping_list",
    "/objects/quantity_units",
    "/objects/products",
    "/objects/product_groups"
]

rs = (grequests.get(f"{BASE_URL}{u}", headers=headers) for u in urls)
map = grequests.map(rs)

shopping_list = map[0].json()
units = map[1].json()
products = map[2].json()
product_groups = map[3].json()

parsed_units = {}
for item in units:
    parsed_units[item["id"]] = item["name"]

parsed_products = {}
for item in products:
    parsed_products[item["id"]] = {"name": item["name"], "product_group_id": item["product_group_id"],
                                   "conversion_rate": item["qu_factor_purchase_to_stock"],
                                   "qu_id_purchase": item["qu_id_purchase"]}

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
    amount = item[1]["amount"] / float(product["conversion_rate"])
    unit = parsed_units[product["qu_id_purchase"]]

    pretty_list[name] = {"amount": amount, "unit": unit, "product_group": product_group}

data = ""
for item in pretty_list.items():
    data = data + item[0] + "," + str(round(item[1]["amount"])) + "," + item[1]["unit"] + "," + item[1]["product_group"] + "\n"

with open("shopping_list.csv", "w") as f:
    f.write(data)
    f.close()
