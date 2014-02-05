class UnauthorizedResourceError(Exception):
  def __init__(self, action, target, user, context, resource, permission):
    self.action = action
    self.target = target
    self.user = user
    self.context = context
    self.resource = resource
    self.permission = permission


class ActionNotFoundError(Exception):
  def __init__(self, value):
    self.value = value


class TargetNotFoundError(Exception):
  def __init__(self, value):
    self.value = value


class ActionAlreadyExistsError(Exception):
  def __init__(self, value):
    self.value = value

    
class TargetAlreadyHasAsteriskError(Exception):
  def __init__(self, value):
    self.value = value


class TargetAlreadyHasActionsError(Exception):
  def __init__(self, value):
    self.value = value


class ActionListWithAsteriskError(Exception):
  def __init__(self, value):
    self.value = value
