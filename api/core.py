from neo4j import GraphDatabase
from api.config import (
    NEO4J_URI,
    NEO4J_AUTH
)

driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)