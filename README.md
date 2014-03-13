#PyCan

PyCan is an open source authorization library designed to be very lightweight, easily installed and easlily used with any python application.



##Instalation

##Usage

PyCan uses a white-list approach. That means that every entry point of your application is, by default, denied. So, you are going to have to authorize the entry-points you want to be accessible in your application.

###User

An `user` is, generally, the entity that is trying to perform some `action` in the system. Like requesting a web page or inserting something in a database, download a file.


###Actions

An `action` is somthing that can be executed by a system, like a command, a function, a controller, a file, a web page or something else that suits your needs. 

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
