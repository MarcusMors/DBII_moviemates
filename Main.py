import flask
from flask import render_template, request
from neo4j import GraphDatabase

app = flask.Flask(__name__)


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
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        return self._driver


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('app_layout__simpler.html')

@app.route('/test_nested', methods=['GET', 'POST'])
def test_nested():
<<<<<<< HEAD
    if request.method == 'POST':
        genre = request.form.get('genre', '')
        title = request.form.get('title', '')

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

        connection = Neo4jConnection("bolt://44.197.239.196:7687", "neo4j", "recruit-presence-captain")

        with connection.connect() as driver:
            with driver.session() as session:
                if genre or title:
                    result = session.run(cypher_query, genre=genre, title=title)
                    results = [{"title": record["m.title"], "poster": record["m.poster"]} for record in result]
                else:
                    results = []

        connection.close()

        return render_template('app_layout.html', results=results)

    return render_template('app_layout.html', results=None)
=======
    return render_template('app_layout.html')
>>>>>>> fd13fdd4ee0399eef2ecd9ef3551d8dc336bf4a3


@app.route('/execute_query', methods=['POST'])
def execute_query():
    query = flask.request.form['query']
    connection = Neo4jConnection("bolt://44.197.239.196:7687", "neo4j", "recruit-presence-captain")

    with connection.connect() as driver:
        with driver.session() as session:
            result = session.run(query)
            results = [{"title": record["title"], "poster": record["posterURL"]} for record in result]

    connection.close()

    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
