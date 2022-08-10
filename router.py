import os
from datetime import date
from flask import Flask, render_template, Response, request, redirect, make_response
import app.login as lg
from app import shopping_list, inventory

BASE_URL = os.environ.get("BASE_URL") + "/api"
app = Flask("grocy-python", template_folder="web", static_folder="web")


@app.route("/")
def index():
    cookie = request.cookies.get("grocy_session")
    if cookie is None:
        return redirect("/login")
    return render_template("index.html", stores=shopping_list.get_stores(BASE_URL, cookie))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/api/login", methods=['POST'])
def do_login():
    cookie = lg.getCookie(BASE_URL, request.form["username"], request.form["password"])
    resp = make_response(redirect("/"))
    resp.set_cookie('grocy_session', cookie)
    return resp


@app.route("/api/logout")
def do_logout():
    resp = make_response(redirect("/login"))
    resp.set_cookie('grocy_session', '', expires=0)
    return resp


@app.route("/api/export_shopping_list", methods=['POST'])
def export_shopping_list():
    form_data = request.form["store_id"].split(":")
    cookie = request.cookies.get("grocy_session")
    data = shopping_list.export_shopping_list(BASE_URL, cookie, form_data[0])
    d = str(date.today())
    return Response(data, mimetype="text/plain",
                    headers={"Content-Disposition": f"attachment;filename={form_data[1]}_shopping_list_" + d + ".csv"})


@app.route("/api/add_meal_plan_to_shopping_list", methods=['POST'])
def add_meal_plan_to_shopping_list_raw():
    form_data = request.form
    cookie = request.cookies.get("grocy_session")
    result = shopping_list.add_meal_plan_to_shopping_list(BASE_URL, cookie, form_data["start-date"],
                                                          form_data["end-date"])
    if result == "Bad Date":
        return "You Must Enter a Valid Date"
    return redirect("/")


@app.route("/api/export_inventory_template")
def export_inventory_template():
    cookie = request.cookies.get("grocy_session")
    data = inventory.export_template(BASE_URL, cookie)

    return Response(data, mimetype="text/plain",
                    headers={"Content-Disposition": f"attachment;filename=inventory_template.csv"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
