from coronavirus_monitor import request_corona
from flask import Flask, render_template
import pandas as pd
import json
from date_list import date_list

app = Flask(__name__)
@app.route("/")

def main():
    df = pd.DataFrame()
    for item in date_list:
        querystring = {"country": "Brazil", "date": item}
        resposta = request_corona(querystring)

        if not resposta.text == '':
            x = dict(json.loads(resposta.content))
            frubas = pd.DataFrame.from_dict(x['stat_by_country'])
            df = pd.concat([frubas, df])

    df.to_csv('./data/csv/data.csv', index=False, sep=';')
    # df.to_xls('./data/xls/data.xls', index=False, sep=';')
    # with open('./data/json/data.json', 'w') as outfile:
    #   json.dump(response.json(), outfile)
        # pd.read_json("./data/json/data.json").to_excel("./data/xls/sheet.xlsx")

    # return df.to_html()
    # return response.text
    # return response.content
    return render_template('dashboard.html', titulo = 'Dashboards')
if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')