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

#####Helper functions

######and_

######or_

######not_

######allow_to_all


#####User

#####Resource

#####Application Context

####Resource Providers

####Exceptions


##Contributing

###Coding

###Tests

###Documentation
