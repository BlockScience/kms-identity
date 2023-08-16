class MissingMeansError(Exception):
    pass

class MissingContextError(Exception):
    pass

class MissingContextSchemaError(Exception):
    pass

class ContextSchemaValidationError(Exception):
    pass

class UnsupportedMeansError(Exception):
    pass

class NoAvailableActionsError(Exception):
    pass

class ActionNotFoundError(Exception):
    pass