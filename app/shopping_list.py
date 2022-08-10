from requests import get, post, put
from datetime import datetime


def add_meal_plan_to_shopping_list(base_url, cookie, start_date, end_date):
    headers = {
        "Cookie": "grocy_session=" + cookie,
        "Content-Type": "application/json",
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
                    recipe_id = recipe["recipe_id"]
                    recipe_data = {"desired_servings": str(recipe['recipe_servings'])}

                    put(f"{base_url}/objects/recipes/{recipe_id}", json=recipe_data, headers=headers)
                    post(f"{base_url}/recipes/{recipe_id}/add-not-fulfilled-products-to-shoppinglist", data=data, headers=headers)
                    print(f"added Recipe {recipe_id} for {recipe_data['desired_servings']} servings to shopping list!")

    except ValueError:
        return "Bad Date"
    return None


def export_shopping_list(base_url, cookie, store):
    headers = {
        "Cookie": "grocy_session=" + cookie,
        "Content-Type": "application/json"
    }

    print(headers)

    shopping_list = get(f"{base_url}/objects/shopping_list", headers=headers).json()
    units = get(f"{base_url}/objects/quantity_units", headers=headers).json()
    products = get(f"{base_url}/objects/products", headers=headers).json()
    product_groups = get(f"{base_url}/objects/product_groups", headers=headers).json()

    parsed_units = {}
    for item in units:
        parsed_units[item["id"]] = item["name"]

    parsed_products = {}
    for item in products:

        if item["shopping_location_id"] == "":
            item["shopping_location_id"] = "1"

        parsed_products[item["id"]] = {"name": item["name"], "product_group_id": item["product_group_id"],
                                       "conversion_rate": item["qu_factor_purchase_to_stock"],
                                       "qu_id_purchase": item["qu_id_purchase"],
                                       "store_id": item["shopping_location_id"]}
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
        if product["store_id"] == store:
            name = product["name"].replace("*", "")
            if name.lower() != "water":
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


def get_stores(base_url, cookie):
    headers = {
        "Cookie": "grocy_session=" + cookie,
        "Content-Type": "application/json"
    }

    return get(f"{base_url}/objects/shopping_locations", headers=headers).json()
