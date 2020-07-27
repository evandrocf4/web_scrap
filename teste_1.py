import json
import pandas as pd

from flask import Flask
from coronavirus_monitor import response

app = Flask(__name__)


@app.route("/")
def index():
    return response.text

with open('data.json', 'w') as outfile:
    json.dump(response.json(), outfile)

pd.read_json("data.json").to_excel("output.xlsx")

if __name__ == "__main__":
    app.run(debug = True)
