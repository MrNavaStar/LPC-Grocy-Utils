import os
from datetime import date
from flask import Flask, render_template, Response, request, redirect

import inventory
import shopping_list
#from dotenv import load_dotenv

#load_dotenv()
BASE_URL = os.environ.get("BASE_URL")
API_KEY = os.environ.get("API_KEY")
app = Flask("grocy-python", template_folder="web", static_folder="web")


@app.route("/")
def index():
    return render_template("index.html", stores=shopping_list.get_stores(BASE_URL, API_KEY))


@app.route("/api/export_shopping_list", methods=['POST'])
def export_shopping_list():
    form_data = request.form["store_id"].split(":")
    data = shopping_list.export_shopping_list(BASE_URL, API_KEY, form_data[0])
    d = str(date.today())
    return Response(data, mimetype="text/plain",
                    headers={"Content-Disposition": f"attachment;filename={form_data[1]}_shopping_list_" + d + ".csv"})


@app.route("/api/add_meal_plan_to_shopping_list", methods=['POST'])
def add_meal_plan_to_shopping_list_raw():
    form_data = request.form
    result = shopping_list.add_meal_plan_to_shopping_list(BASE_URL, API_KEY, form_data["start-date"],
                                                          form_data["end-date"])

    if result == "Bad Date":
        return "You Must Enter a Valid Date"
    return redirect("/")


@app.route("/api/export_inventory_template")
def export_inventory_template():
    data = inventory.export_template(BASE_URL, API_KEY)

    return Response(data, mimetype="text/plain",
                    headers={"Content-Disposition": f"attachment;filename=inventory_template.csv"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
