# -*- coding: utf-8 -*-
import inspect
import exceptions

_permissions = {}


def can(action_set, target_set, authorization, get_authorization_resource=lambda _, __: None,
        get_resource=lambda _, __: None, exception=None):
    assert action_set, "At least one action must be specified"
    assert target_set, "At least one target must be specified"
    assert authorization, "An authorization procedure must be specified"
    assert getattr(get_authorization_resource, '__call__'), "get_authorization_resource must be callable"
    assert getattr(get_resource, '__call__'), "get_resource must be callable"
    assert getattr(authorization, '__call__'), "get_resource must be callable"

    assert len(inspect.getargspec(get_authorization_resource).args) == 2, \
        "get_authorization_resource must accept 2 parameters"
    assert len(inspect.getargspec(get_resource).args) == 2, "get_resource must accept 2 parameters"
    assert len(inspect.getargspec(authorization).args) == 3, "authorization must accept 3 parameters"

    if not _is_sequence(target_set):
        target_set = [target_set]

    if not _is_sequence(action_set):
        action_set = [action_set]
    elif "*" in action_set and len(action_set) > 1:
        raise exceptions.ActionListWithAsteriskError("* must be a solo action")

    for target in target_set:
        if target not in _permissions:
            _permissions[target] = {}

        if "*" in _permissions[target]:
            raise exceptions.TargetAlreadyHasAsteriskError("The target \"%s\" already has an \"*\"" % target)

        for action in action_set:
            if action == "*" and len(_permissions[target]) > 0:
                raise exceptions.TargetAlreadyHasActionsError(
                    "Can't register \"*\" cause the target \"%s\" already has action_set" % target)

            if action in _permissions[target]:
                raise exceptions.ActionAlreadyExistsError(
                    "A permission for this target resource has already been specified")

            _permissions[target][action] = {
                'exception': exception,
                'authorization': authorization,
                'get_authorization_resource': get_authorization_resource,
                'get_resource': get_resource,
            }


def can_i(action, target, user, context=None):
    assert action, "An action must be specified"
    assert target, "A target must be specified"
    assert user, "An user must be specified"

    result = False
    auth_resource = None
    resource = None

    target_action_set = _permissions.get(target) or {}
    authorization_data = target_action_set.get(action) or target_action_set.get("*")

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
        raise ((_permissions.get(target) or {}).get(action) or {}).get("exception") or \
            exceptions.UnauthorizedResourceError(action, target, user, context, resource)


def _is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))
