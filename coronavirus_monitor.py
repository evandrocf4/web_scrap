import requests


def request_corona(querystring=None):
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/history_by_particular_country_by_date.php"

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "cc2202fb08mshce98b0dc9b7db7ap103456jsn1f7c9f0dbb98"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response

