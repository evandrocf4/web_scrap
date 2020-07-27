from flask import Flask
from coronavirus_monitor import response
import json
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():
    x = dict(json.loads(response.content))
    df = pd.DataFrame.from_dict(x['latest_stat_by_country'])
    df.to_csv('./data/csv/sheet.csv', index=False, sep=';')
    return df.to_html()


if __name__ == "__main__":
    app.run()
