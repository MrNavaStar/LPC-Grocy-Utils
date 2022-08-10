from requests import get


def export_template(base_url, cookie):
    headers = {
        "Cookie": "grocy_session=" + cookie,
        "Content-Type": "application/json"
    }

    products = get(f"{base_url}/objects/products", headers=headers).json()
    product_groups = get(f"{base_url}/objects/product_groups", headers=headers).json()

    parsed_products = {}
    for item in products:
        parsed_products[item["id"]] = {"name": item["name"], "product_group_id": item["product_group_id"]}

    parsed_product_groups = {}
    for item in product_groups:
        parsed_product_groups[item["id"]] = item["name"]

    data = ""
    for product in parsed_products.values():
        data += product["name"].replace("*", "") + "\n"

    return data

