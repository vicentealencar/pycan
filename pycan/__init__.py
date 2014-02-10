# -*- coding: utf-8 -*-
import inspect
import exceptions

_permissions = {}

def allow_to_all(user, app_context, resource):
     return True

def can(action_set, context_set, authorization, get_authorization_resource=lambda _, __: None,
        get_resource=lambda _, __: None, exception=None):
    assert action_set, "At least one action must be specified"
    assert authorization, "An authorization procedure must be specified"
    assert getattr(get_authorization_resource, '__call__'), "get_authorization_resource must be callable"
    assert getattr(get_resource, '__call__'), "get_resource must be callable"
    assert getattr(authorization, '__call__'), "get_resource must be callable"

    assert len(inspect.getargspec(get_authorization_resource).args) == 2, \
        "get_authorization_resource must accept 2 parameters"
    assert len(inspect.getargspec(get_resource).args) == 2, "get_resource must accept 2 parameters"
    assert len(inspect.getargspec(authorization).args) == 3, "authorization must accept 3 parameters"

    if not _is_sequence(context_set):
        context_set = [context_set]

    if not _is_sequence(action_set):
        action_set = [action_set]
    elif "*" in action_set and len(action_set) > 1:
        raise exceptions.ActionListWithAsteriskError("* must be a solo action")

    for context in context_set:
        if context not in _permissions:
            _permissions[context] = {}

        if "*" in _permissions[context]:
            raise exceptions.ContextAlreadyHasAsteriskError("The context \"%s\" already has an \"*\"" % context)

        for action in action_set:
            if action == "*" and len(_permissions[context]) > 0:
                raise exceptions.ContextAlreadyHasActionsError(
                    "Can't register \"*\" cause the context \"%s\" already has action_set" % context)

            if action in _permissions[context]:
                raise exceptions.ActionAlreadyExistsError(
                    "A permission for this context resource has already been specified")

            _permissions[context][action] = {
                'exception': exception,
                'authorization': authorization,
                'get_authorization_resource': get_authorization_resource,
                'get_resource': get_resource,
            }


def can_i(action, context, user=None, app_context=None):
    assert action, "An action must be specified"

    result = False
    auth_resource = None
    resource = None

    context_action_set = _permissions.get(context) or {}
    authorization_data = context_action_set.get(action) or context_action_set.get("*")

    if authorization_data is not None:
        auth_resource = authorization_data.get('get_authorization_resource')(user, app_context)

        result = authorization_data.get('authorization')(
            user,
            app_context,
            auth_resource)

        if result:
            resource = authorization_data.get('get_resource')(user, app_context)

    return result, auth_resource, resource


def authorize(action, context, user, app_context=None):
    go_ahead, auth_resource, resource = can_i(action, context, user, app_context)

    if go_ahead:
        return auth_resource, resource
    else:
        raise ((_permissions.get(context) or {}).get(action) or {}).get("exception") or \
            exceptions.UnauthorizedResourceError(action, context, user, app_context, resource)


def _is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))
