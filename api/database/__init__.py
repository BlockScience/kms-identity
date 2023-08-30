from . import (
    utils,
    objects,
    relations,
    assertions
)

@utils.execute_write
def drop(tx):
    DROP = "MATCH (n) DETACH DELETE n"
    tx.run(DROP)