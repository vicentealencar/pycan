#PyCan

PyCan is an open source authorization library designed to be very lightweight, easily installed and easlily used with any python application.



##Instalation

##Usage

PyCan uses a white-list approach. That means that every entry point of your application is, by default, denied. So, you are going to have to authorize the entry-points you want to be accessible in your application.

The following definitions were made thinking in the most general terms possible, so PyCan can be used in any kind of application or context.

###User

An `user` is, generally, the entity that is trying to perform some `action` on the system like: requesting a web page or inserting something in a database, download a file, etc.


###Actions

An `action` is something that can be executed by a system, like a command, a function, a controller, a file, a web page or something else that suits your needs. 


###Contexts

A `context` is some kind of container or namespace for an action like a class, a module, a sub-application, etc.


###Application Context

An `application context` is the current context your application is in the moment of the authorization. It could be the performed request, in case of a web application, or the screen that is shown currently, etc.


###Enabling PyCan

PyCan is enabled when you intercept your application entry points calling the method [`authorize`](https://github.com/jusbrasil/pycan/blob/master/pycan/__init__.py#L78).

```python
from pycan import authorize

try:
    authorize(action, context, application_context)
except UnauthorizedResourceError, e:
    #do nothing
  
#do that thing

```

Once PyCan is enabled, by default, every `action` whitin every `context` of your application is disabled/forbidden.


###Registering authorizations

For enabling the access to some `action` whitin some `context` you have to register it using the method [`can`](https://github.com/jusbrasil/pycan/blob/master/pycan/__init__.py#L11).

```python
from pycan import can

can('some_action', 'some_context', some_condition)
```

The [`can`](https://github.com/jusbrasil/pycan/blob/master/pycan/__init__.py#L11) method is defined as follows:

```python
can(
    List|String:action_set, 
    List:context_set, 
    Function(user, application_context, authorized_resource):authorization -> Boolean, 
    Function(user, application_context):authorization_resource_provider -> Anything, 
    Function():authorized_resource_provider -> Anything, 
    Exception(kwargs):custom_exception
) -> None
```

####Action set

The `action_set` parameter receives a list with strings or a single string.
It also accepts [`None`](http://docs.python.org/2/library/constants.html#None).
If you want to register the authorization for every `action` within a `context` you can use `'*'`.
If some context already have an `'*'` and someone try to register a new `action` for the same `context` a [`ContextAlreadyHasAsteriskError`](https://github.com/jusbrasil/pycan/blob/master/pycan/__init__.py#L36) exception will be raised

####Contexts

####Authorization Methods
 
#####User

#####Resource

#####Application Context

####Resource Providers

#####Authorization Resource Provider

#####Authorized Resource Provider

####Exceptions


####Helper functions

#####and_
This method combines n authorization methods with a boolean and, and returns a authorization method

```python
from pycan import can, and_

can('some_action', 'some_context', and_(one_condition, another_condition))
```

#####or_

#####not_

#####allow_to_all

###Revoking an authorization

##Contributing

###Coding

###Tests

###Documentation

##Who uses

* [JusBrasil](http://www.jusbrasil.com.br)
