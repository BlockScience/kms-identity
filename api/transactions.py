from api.queries import CREATE_OBJECT_REFERENCE

def create_object_reference(tx, obj):
    result = tx.run(CREATE_OBJECT_REFERENCE, props=obj)
    return list(result)