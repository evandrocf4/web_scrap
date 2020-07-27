from flask import Flask, render_template
import requests

app = Flask(__name__)

url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/history_by_particular_country_by_date.php"

querystring = {"country":"Brazil","date":"2020-01-01"}

headers = {
    'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
    'x-rapidapi-key': "cc2202fb08mshce98b0dc9b7db7ap103456jsn1f7c9f0dbb98"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

@app.route('/')
def index():
    #print (response)
    return render_template('lista.html');

app.run(debug=True)