import flask
from flask import render_template
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

@app.route('/test_nested')
def test_nested():
    return render_template('app_layout.html')


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
