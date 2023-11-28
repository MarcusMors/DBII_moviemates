# import json
# import os

from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS
from neo4j import GraphDatabase

app = Flask(__name__, template_folder="./templates", static_folder="./static")

CORS(app)


class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self._uri = uri
        self._user = user
        self._password = pwd
        self._driver = None

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def connect(self):
        self._driver = GraphDatabase.driver(
            self._uri, auth=(self._user, self._password)
        )
        return self._driver


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test")
def test():
    return render_template("app_layout__simpler.html")


"""
"identity": 1215,
"labels": [
"Movie"
],
"properties": {
"languages": [
    "English"
],
"year": 1996,
"imdbId": "0118064",
"runtime": 100,
"imdbRating": 6.8,
"movieId": "1482",
"countries": [
    "UK",
    " Ireland",
    " USA"
],
"imdbVotes": 3407,
"title": "Van, The",
"url": "https://themoviedb.org/movie/11844",
"tmdbId": "11844",
"plot": "The third installment of Irish author Roddy Doyle's 'Barrytown Trilogy', following 'The Commitments' and 'The Snapper', depicts the hilarious yet poignant adventures of Bimbo. Upon being ...",
"poster": "https://image.tmdb.org/t/p/w440_and_h660_face/A2wxXFnie5gvm0o2UX5IEtzOgZ4.jpg",
"released": "1997-05-16"
},
"elementId": "1215"

"""


@app.route("/api/rand_movies", methods=["POST"])
def get_rand_movies():
    answer = {"movies": "", "id": 200}  # Everything OK!

    if request.method != "POST":
        answer["id"] = 405  # Method Not Allowed
        return answer

    query = "MATCH (m:Movie) RETURN m.title, m.poster, m.plot, m.year ORDER BY RAND() LIMIT 5;"

    connection = Neo4jConnection(
        "bolt://44.197.239.196:7687", "neo4j", "recruit-presence-captain"
    )

    results = []
    with connection.connect() as driver:
        with driver.session() as session:
            result = session.run(query)
            results = [
                {
                    "year": record["m.year"],
                    "plot": record["m.plot"],
                    "title": record["m.title"],
                    "poster": record["m.poster"],
                }
                for record in result
            ]

    connection.close()
    answer["movies"] = results
    return answer


@app.route("/header")
def header():
    # data = users_data[logged_users[client_ip]]
    # context = {"data": data, "products": products}
    # return render_template("welcome.html", **context, user=data["username"], log=True)
    return render_template("app_simple_test.html")


@app.route("/test_nested")
def test_nested():
    return render_template("app_layout.html")


@app.route("/home")
def test_end():
    return render_template("home.html")


@app.route("/execute_query", methods=["POST"])
def execute_query():
    query = request.form["query"]
    connection = Neo4jConnection(
        "bolt://44.197.239.196:7687", "neo4j", "recruit-presence-captain"
    )

    with connection.connect() as driver:
        with driver.session() as session:
            result = session.run(query)
            results = [
                {"title": record["title"], "poster": record["posterURL"]}
                for record in result
            ]

    connection.close()

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
