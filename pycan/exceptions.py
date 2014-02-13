class UnauthorizedResourceError(Exception):
    def __init__(self, action, app_context, user, context, resource):
        Exception.__init__(self, 'Action %s of context %s unauthorized' % (action, app_context))

        self.action = action
        self.app_context = app_context
        self.user = user
        self.context = context
        self.resource = resource


class ActionNotFoundError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class ContextNotFoundError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class ActionAlreadyExistsError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class ContextAlreadyHasAsteriskError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class ContextAlreadyHasActionsError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class ActionListWithAsteriskError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
