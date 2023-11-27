# How to start the project

## Prerequisites

Having installed Neo4j *VERSION 4.2*, follow these [instructions](https://neo4j.com/docs/operations-manual/current/installation/linux/debian/) if you haven't installed it yet.

## Setup the project

```bash
  sudo service neo4j start # start neo4j
```

## Pip3

```bash
  pip install neo4j-driver
  pip install graphdatascience
```


sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://debian.neo4j.com/neotechnolog.key | sudo apt-key add -

sudo add-apt-repository "deb https://debian.neo4j.com stable 4.1"

sudo apt install neo4j

sudo systemctl enable neo4j.service

sudo systemctl status neo4j.service

cypher-shell

sudo nano /etc/neo4j/neo4j.conf
CREATE (:Shark {name: 'Great White'});
