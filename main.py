from coronavirus_monitor import request_corona
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

    return render_template('dashboard.html', titulo = 'Dashboards')
if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')