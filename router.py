import os
from datetime import date
from flask import Flask, render_template, Response, request, jsonify
import shopping_list
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.environ.get("BASE_URL")
API_KEY = os.environ.get("API_KEY")
app = Flask("grocy-python", template_folder="web", static_folder="web")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/export_shopping_list", methods=['GET'])
def export_shopping_list():
    params = request.args
    store = params.get("store", default="none", type=str)

    data = shopping_list.export_shopping_list(BASE_URL, API_KEY, store)
    d = str(date.today())
    return Response(data, mimetype="text/plain", headers={"Content-Disposition": f"attachment;filename=shopping_list_" + d + ".csv"})


@app.route("/api/raw/add_meal_plan_to_shopping_list", methods=['GET'])
def add_meal_plan_to_shopping_list_raw():
    return jsonify(shopping_list.add_meal_plan_to_shopping_list(BASE_URL, API_KEY))


@app.route("/api/raw/export_shopping_list", methods=['GET'])
def export_shopping_list_raw():
    params = request.args
    store = params.get("store", default="none", type=str)

    return shopping_list.export_shopping_list(BASE_URL, API_KEY, store).replace('\n', '<br>')


if __name__ == '__main__':
    app.run(port=5000)
