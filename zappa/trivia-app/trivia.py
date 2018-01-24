from flask import Flask
from flask import render_template
import json
from random import randint
import requests
app = Flask(__name__)

host = 'https://qriusity.com'


@app.route("/")
def categories():
    categories = []
    for i in [1, 2]:
        r = requests.get("{}/v1/categories?page={}&limit=20".format(host, i))
        categories.extend(json.loads(r.text))
    categories = sorted(categories, key=lambda cat: cat['name'])
    return render_template('categories.html', categories=categories)


@app.route("/question/<category_id>")
def question(category_id):
    base_url = "{}/v1/categories".format(host)
    url = "{}/{}/questions?page={}&limit=1".format(
        base_url,
        category_id,
        randint(1, 100)
    )
    r = requests.get(url)
    return render_template('question.html', question=json.loads(r.text)[0])
