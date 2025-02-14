from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
from flask import Flask, jsonify
import json
import re

app = Flask(__name__)

@app.route('/user/<userID>')
def user_data(userID):
    url = f'http://www.imdb.com/user/{userID}/ratings'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

    soup = BeautifulSoup(response.content, "html.parser")
    user = []

    for item in soup.find_all("div", {"class": "lister-item-content"}):
        film = {}
        name = item.find_all('a')[0].get_text()
        episode = item.find_all('a')[1].get_text().strip('\n').strip()
        if episode == '':
            link = item.find('a', href=True)['href']
            key = str(item.find('a', href=True)['href'][7:16])
            year = item.find_all(class_="lister-item-year")[0].get_text()
            year = find_between(year)
        else:
            name = name[1:] + ", (" + episode + ")"
            link = item.find_all('a', href=True)[1]['href']
            key = str(item.find_all('a', href=True)[1]['href'][7:16])
            year = item.find_all(class_="lister-item-year")[1].get_text()
            year = find_between(year)
        
        link = 'http://www.imdb.com' + link[:16]
        my_rate = item.find_all(class_="ipl-rating-star__rating")[1].get_text()
        imdb_rate = item.find_all(class_="ipl-rating-star__rating")[0].get_text()
        date = dt.strptime(item.find_all("p", {"class": "text-muted"})[1].get_text()[9:], '%d %b  %Y')
        rate_date = date.strftime('%Y-%m-%d')

        film["NameID"] = key
        film["Name"] = name
        film["Year"] = year.replace("\u2013", "-")
        film["Link"] = link
        film["MyRate"] = my_rate
        film["imdbRate"] = imdb_rate
        film["RateDate"] = rate_date
        user.append(film)

    return jsonify(user)

def find_between(s):
    match = re.search(r'\((\d{4})\)', s)
    return match.group(1) if match else ""

if __name__ == '__main__':
    app.run()
