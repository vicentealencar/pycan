#PyCan

##Instalation

##Usage

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


##Contributing

###Coding

###Tests

###Documentation
