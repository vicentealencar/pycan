# -*- coding: utf-8 -*-
import inspect

_permissions = {}

def _default_exception():
  return Exception("Unauthorized access")

def can(action, target, authorization, get_authorization_resource=lambda _,__: None,
  get_resource=lambda _,__: None, exception=None):
  assert action, "An action must be specified"
  assert target, "A target must be specified"
  assert authorization, "An authorization procedure must be specified"
  assert getattr(get_authorization_resource, '__call__'), "get_authorization_resource must be callable"
  assert getattr(get_resource, '__call__'), "get_resource must be callable"
  assert getattr(authorization, '__call__'), "get_resource must be callable"

  assert len(inspect.getargspec(get_authorization_resource).args) == 2, "get_authorization_resource must accept 2 parameters"
  assert len(inspect.getargspec(get_resource).args) == 2, "get_resource must accept 2 parameters"
  assert len(inspect.getargspec(authorization).args) == 3, "authorization must accept 3 parameters"

  if target not in _permissions:
    _permissions[target] = {}

  if action in _permissions[target] or "*" in _permissions[target]:
    raise Exception("A permission for this target resource has already been specified")

  _permissions[target][action] = {
      'exception': exception or _default_exception(),
      'authorization': authorization,
      'get_authorization_resource': get_authorization_resource,
      'get_resource': get_resource,
    }

def can_i(action, target, user, context=None):
  assert action, "An action must be specified"
  assert target, "A target must be specified"
  assert user, "A user must be specified"

  result = False
  auth_resource = None
  resource = None

  target_actions = _permissions.get(target) or {}
  authorization_data = target_actions.get(action) or target_actions.get("*")

  if authorization_data is not None:
    auth_resource = authorization_data.get('get_authorization_resource')(user, context)

    result = authorization_data.get('authorization')(
      user,
      context,
      auth_resource)

    if result:
      resource = authorization_data.get('get_resource')(user, context)

  return result, auth_resource, resource

def authorize(action, target, user, context=None):
  go_ahead, auth_resource, resource = can_i(action, target, user, context)

  if go_ahead:
    return auth_resource, resource
  else:
    raise ((_permissions.get(target) or {}).get(action) or {}).get("exception") or _default_exception()
