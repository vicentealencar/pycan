# -*- coding: utf-8 -*-
import exceptions
import inspect
import operator

_permissions = {}

def allow_to_all(user, context, resource):
     return True

def can(action_set, target_set, authorization, load_before=lambda _, __: None,
        load_after=lambda _, __: None, exception=None):
    assert authorization, "An authorization procedure must be specified"
    assert getattr(load_before, '__call__'), "load_before must be callable"
    assert getattr(load_after, '__call__'), "load_after must be callable"
    assert getattr(authorization, '__call__'), "load_after must be callable"

    assert len(inspect.getargspec(load_before).args) == 2, \
        "load_before must accept 2 parameters"
    assert len(inspect.getargspec(load_after).args) == 2, "load_after must accept 2 parameters"
    _assert_authorization_parameters(authorization)

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
            raise exceptions.ContextAlreadyHasAsteriskError("The target \"%s\" already has an \"*\"" % target)

        for action in action_set:
            if action == "*" and len(_permissions[target]) > 0:
                raise exceptions.ContextAlreadyHasActionsError(
                    "Can't register \"*\" cause the target \"%s\" already has action_set" % target)

            if action in _permissions[target]:
                raise exceptions.ActionAlreadyExistsError(
                    "The \"%s\" permission for this target resource has already been specified" % action)

            _permissions[target][action] = {
                'exception': exception,
                'authorization': authorization,
                'load_before': load_before,
                'load_after': load_after,
            }


def can_i(action, target, user=None, context=None):
    result = False
    auth_resource = None
    resource = None
    exception = False

    target_action_set = _permissions.get(target, {})
    authorization_data = target_action_set.get(action) or target_action_set.get("*")

    if authorization_data is not None:
        auth_resource = authorization_data.get('load_before')(user, context)
        
        result = authorization_data.get('authorization')(
            user,
            context,
            auth_resource)

        if result:
            resource = authorization_data.get('load_after')(user, context)

    return result, auth_resource, resource, 


def authorize(action, target, user, context=None):
    go_ahead, auth_resource, resource= can_i(action, target, user, context)

    if go_ahead:
        return auth_resource, resource
    else:
         exception = ((_permissions.get(target, {})).get(action, {})).get("exception")
         raise exception(
            action=action,
            target=target,
            user=user,
            context=context,
            resource=resource
         ) if exception else exceptions.UnauthorizedResourceError(action, target, user, context, resource)


def and_(*args):
    assert len(args) > 0, "List of authorization methods cannot be empty"
    map(_assert_authorization_parameters, args)
    return lambda u, c, r: reduce(lambda prev, current: prev and current(u, c, r), args, True)


def or_(*args):
    assert len(args) > 0, "List of authorization methods cannot be empty"
    map(_assert_authorization_parameters, args)
    return lambda u, c, r: reduce(lambda prev, current: prev or current(u, c, r), args, False)


def not_(method):
    _assert_authorization_parameters(method)
    return lambda u, c, r: not method(u, c, r)


def _assert_authorization_parameters(method):
    assert inspect.isfunction(method), "Authorization must be a callable"
    assert len(inspect.getargspec(method).args) == 3, "Authorization must accept 3 parameters"


def _is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))


def revoke(action_set, target_set):
    if(not _is_sequence(action_set)):
        action_set = [action_set]

    if(not _is_sequence(target_set)):
        target_set = [target_set]

    for target in target_set:
        if target  in _permissions:
            for action in action_set:
                _permissions[target].pop(action)

