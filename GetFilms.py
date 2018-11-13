om bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
from flask import Flask
app = Flask(__name__)


@app.route('/user/<userID>')
def UserData(userID):
    url = 'http://www.imdb.com/user/' + userID + '/ratings'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    user = []
    for item in soup.find_all("div", {"class": "lister-item-content"}):
        film = {}
        name = item.find_all('a')[0].get_text()
        episode = item.find_all('a')[1].get_text().strip('\n').strip()
        if (episode == ''):
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
        myRate = item.find_all(class_="ipl-rating-star__rating")[1].get_text()
        imdbRate = item.find_all(class_="ipl-rating-star__rating")[0].get_text()
        date = dt.strptime(item.find_all("p", {"class": "text-muted"})[1].get_text()[9:], '%d %b  %Y')
        rateDate = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
        film["NameID"] = key
        film["Name"] = name
        film["Year"] = year.replace("\u2013", "-")
        film["Link"] = link
        film["MyRate"] = myRate
        film["imdbRate"] = imdbRate
        film["RateDate"] = rateDate
        user.append(film)
    json_data = json.dumps(user)
    return json_data


def find_between(s):
    try:
        s = s[::-1]
        start = s.index("(") + 1
        s = s[::-1]
        return s[(start * -1) + 1:-1]
    except ValueError:
        return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0')
