#PyCan

PyCan is an open source authorization library designed to be very lightweight, easily installed and easlily used with any python application.



##Instalation

##Usage

PyCan uses a white-list approach. That means that every entry point of your application is, by default, denied. So, you are going to have to authorize the entry-points you want to be accessible in your application.

###Actions

We are going to call `action` everything an `user` may be trying to perform in the system. 
Let's take as an example some web based [ERP](http://en.wikipedia.org/wiki/Enterprise_resource_planning).

###Contexts

###Application Context

###Enabling PyCan

```python
from pycan import authorize

try:
    authorize(action, context, application_context)
except UnauthorizedResourceError, e:
    #do nothing
  
#do that thing

```

###Registering authorizations



```python
from pycan import can

can('some_action', 'some_context', check_something)
```

####Actions

####Contexts


####Authorization Methods

#####User

#####Resource

#####Application Context

####Resource Providers

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
