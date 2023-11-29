# import json
# import os

from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS
from neo4j import GraphDatabase

app = Flask(__name__, template_folder="./templates", static_folder="./static")

CORS(app)


class Neo4jConnection:
    def __init__(self, uri=None, user=None, pwd=None):
        if uri is None and user is None and pwd is None:
            [uri, user, pwd] = (
                "bolt://44.197.239.196:7687",
                "neo4j",
                "recruit-presence-captain",
            )
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


@app.route("/api/rand_movies", methods=["POST"])
def get_rand_movies():
    answer = {"movies": "", "id": 200}  # Everything OK!

    if request.method != "POST":
        answer["id"] = 405  # Method Not Allowed
        return answer

    query = "MATCH (m:Movie) RETURN m.title, m.poster, m.plot, m.year ORDER BY RAND() LIMIT 5;"

    connection = Neo4jConnection()

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


@app.route("/aux")
def aux():
    return render_template("aux.html")


# data = users_data[logged_users[client_ip]]
# context = {"data": data, "products": products}
# return render_template("welcome.html", **context, user=data["username"], log=True)


# @app.route("/header")
# def header():
#     return render_template("app_simple_test.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method != "POST":
        return render_template("search.html", results=None)

    genre = request.form.get("genre", "")
    title = request.form.get("title", "")

    if genre:
        # Realiza la búsqueda por género
        cypher_query = (
            "MATCH (g:Genre)<-[:IN_GENRE]-(m:Movie) "
            "WHERE toLower(g.name) STARTS WITH toLower($genre) "
            "RETURN m.title, m.poster"
        )
    elif title:
        # Realiza la búsqueda por título
        cypher_query = (
            "MATCH (m:Movie) "
            "WHERE toLower(m.title) CONTAINS toLower($title) "
            "RETURN m.title, m.poster"
        )

    connection = Neo4jConnection()

    with connection.connect() as driver:
        with driver.session() as session:
            if genre or title:
                result = session.run(cypher_query, genre=genre, title=title)
                results = [
                    {"title": record["m.title"], "poster": record["m.poster"]}
                    for record in result
                ]
            else:
                results = []

    connection.close()
    if not results:
        return render_template("empty_search.html", results=results)

    return render_template("search.html", results=results)


# @app.route("/home")
# def test_end():
#     return render_template("home.html")


@app.route("/test_nested", methods=["GET", "POST"])
def test_nested():
    if request.method != "POST":
        return render_template("app_layout.html", results=None)

    genre = request.form.get("genre", "")
    title = request.form.get("title", "")

    if genre:
        # Realiza la búsqueda por género
        cypher_query = (
            "MATCH (g:Genre)<-[:IN_GENRE]-(m:Movie) "
            "WHERE toLower(g.name) STARTS WITH toLower($genre) "
            "RETURN m.title, m.poster"
        )
    elif title:
        # Realiza la búsqueda por título
        cypher_query = (
            "MATCH (m:Movie) "
            "WHERE toLower(m.title) CONTAINS toLower($title) "
            "RETURN m.title, m.poster"
        )

    connection = Neo4jConnection()

    with connection.connect() as driver:
        with driver.session() as session:
            if genre or title:
                result = session.run(cypher_query, genre=genre, title=title)
                results = [
                    {"title": record["m.title"], "poster": record["m.poster"]}
                    for record in result
                ]
            else:
                results = []

    connection.close()

    return render_template("app_layout.html", results=results)


@app.route("/execute_query", methods=["POST"])
def execute_query():
    query = flask.request.form["query"]
    connection = Neo4jConnection()

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
