from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
# uri = "bolt://10.255.255.254:7687"
username = "neo4j"
password = "12345678"

driver = GraphDatabase.driver(uri, auth=(username, password))

try:
    with driver.session() as session:
        result = session.run("RETURN 1")
        print(result.single()[0])
    print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")
finally:
    driver.close()
