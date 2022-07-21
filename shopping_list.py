import grequests
from requests import get
from datetime import datetime
from requests import post


def add_meal_plan_to_shopping_list(base_url, api_key, start_date, end_date):
    headers = {
        "GROCY-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "excludedProductIds": [
            0
        ]
    }

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        meal_plans = get(f"{base_url}/objects/meal_plan", headers=headers).json()

        for recipe in meal_plans:
            date = datetime.strptime(recipe["day"], "%Y-%m-%d")
            if end_date >= date >= start_date:
                if recipe["type"] == "recipe":
                    post(f"{base_url}/recipes/{recipe['id']}/add-not-fulfilled-products-to-shoppinglist", data=data, headers=headers)
                    print(f"added Recipe {recipe['id']} to shopping list!")

    except ValueError:
        return "Bad Date"
    return None


def export_shopping_list(base_url, api_key, store):
    headers = {
        "GROCY-API-KEY": api_key
    }

    urls = [
        "/objects/shopping_list",
        "/objects/quantity_units",
        "/objects/products",
        "/objects/product_groups"
    ]

    rs = (grequests.get(f"{base_url}{u}", headers=headers) for u in urls)
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
        name = "\"" + product["name"].replace("*", "") + "\""

        product_group = "None"
        product_group_id = product["product_group_id"]
        if product_group_id != "":
            product_group = parsed_product_groups[product_group_id]

        conversion_rate = float(product["conversion_rate"])
        amount = item[1]["amount"]
        unit = parsed_units[item[1]["unit"]]
        unit_store = parsed_units[product["qu_id_purchase"]]

        if unit != unit_store:
            amount = amount / conversion_rate
            unit = unit_store

        pretty_list[name] = {"amount": amount, "unit": unit, "product_group": product_group}

    data = ""
    for item in pretty_list.items():
        data = data + item[0] + "," + str(round(item[1]["amount"], 1)) + "," + item[1]["unit"] + "," + item[1]["product_group"] + "\n"

    return data
