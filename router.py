import os
from datetime import date
from flask import Flask, render_template, Response
import shopping_list
from dotenv import load_dotenv

app = Flask("grocy-python", template_folder="web", static_folder="web")
load_dotenv()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/export_shopping_list")
def export_shopping_list():
    data = shopping_list.export_shopping_list(os.environ.get("BASE_URL"), os.environ.get("API_KEY"))
    d = str(date.today())
    return Response(data, mimetype="text/plain", headers={"Content-Disposition": f"attachment;filename=shopping_list_" + d + ".csv"})


if __name__ == '__main__':
    app.run(port=5000)
