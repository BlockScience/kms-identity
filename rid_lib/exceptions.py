class IncompleteRIDError(Exception):
    pass

class MissingRIDError(Exception):
    pass

class MissingContextError(Exception):
    pass

class InvalidContextError(Exception):
    pass

class MissingContextSchemaError(Exception):
    pass

class ContextSchemaValidationError(Exception):
    pass

class MeansNotFoundError(Exception):
    pass

class ActionNotFoundError(Exception):
    pass

class ActionTypeError(Exception):
    pass