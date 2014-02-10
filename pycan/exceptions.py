class UnauthorizedResourceError(Exception):
    def __init__(self, action, target, user, context, resource):
        self.action = action
        self.target = target
        self.user = user
        self.context = context
        self.resource = resource


class ActionNotFoundError(Exception):
    def __init__(self, value):
        self.value = value


class ContextNotFoundError(Exception):
    def __init__(self, value):
        self.value = value


class ActionAlreadyExistsError(Exception):
    def __init__(self, value):
        self.value = value


class ContextAlreadyHasAsteriskError(Exception):
    def __init__(self, value):
        self.value = value


class ContextAlreadyHasActionsError(Exception):
    def __init__(self, value):
        self.value = value


class ActionListWithAsteriskError(Exception):
    def __init__(self, value):
        self.value = value
