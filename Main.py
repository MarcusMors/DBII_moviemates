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
            # previous
            [uri, user, pwd] = (
                "bolt://44.197.239.196:7687",
                "neo4j",
                "recruit-presence-captain",
            )

            # new
            # [uri, user, pwd] = (
            #     "bolt://44.192.99.46:7687",
            #     "neo4j",
            #     "tacks-waves-spiral",
            # )

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


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method != "POST":
        return render_template("search.html", results=None)

    print("POST method int home")
    search_text = request.form["search_text"]
    search_type = request.form["search_type"]

    print("search_text:", search_text)
    print("search_type:", search_type)

    if not search_text:
        return render_template("search.html", results=None)

    query_type = {
        "All": (
            "MATCH (m:Movie) "
            "WHERE toLower(m.title) CONTAINS toLower($title) "
            "RETURN m.title, m.poster"
        ),
        "Person": 1,
        "Community": 1,
        "Titles": (
            "MATCH (m:Movie) "
            "WHERE toLower(m.title) CONTAINS toLower($title) "
            "RETURN m.title, m.poster"
        ),
        "TV_eps": 1,
        "Celebs": (
            "MATCH (m:Person) "
            "WHERE toLower(m.name) CONTAINS toLower($name) "
            "RETURN m.name, m.poster"
        ),
        # "Companies": 1,  # productoras (Fox, Warner Brothers, Dosney)
        "Genre": (
            "MATCH (g:Genre)<-[:IN_GENRE]-(m:Movie) "
            "WHERE toLower(g.name) STARTS WITH toLower($genre) "
            "RETURN m.title, m.poster"
        ),
    }

    cypher_query = query_type[search_type]

    connection = Neo4jConnection()

    # All
    # Person
    # Community
    # Titles
    # TV_eps
    # Celebs
    # Companies
    # Genre

    with connection.connect() as driver:
        with driver.session() as session:
            genre = search_text if search_type == "Genre" else None
            title = None
            if search_type != "Genre":
                title = search_text

            if search_type == "Celebs":
                name = search_text
                result = session.run(cypher_query, name=name)
                results = [
                    {"title": record["m.name"], "poster": record["m.poster"]}
                    for record in result
                ]
            else:
                result = session.run(cypher_query, genre=genre, title=title)
                results = [
                    {"title": record["m.title"], "poster": record["m.poster"]}
                    for record in result
                ]

    connection.close()

    if not results:
        return render_template("empty_search.html", results=results)

    return render_template("search.html", results=results)


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
    query = request.form["query"]
    connection = Neo4jConnection()

    with connection.connect() as driver:
        with driver.session() as session:
            result = session.run(query)
            results = [
                {"title": record["m.title"], "poster": record["m.poster"]}
                for record in result
            ]

    connection.close()

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
