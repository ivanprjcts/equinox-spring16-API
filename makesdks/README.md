# makesdks

Tool for auto-generate sdks from a Django rest framework API.

## Description

Makesdks makes it possible to build automatically API clients from Swagger specification.

First, it retrieves swagger specification from public Swagger API Docs. You can see a Django Rest Swagger project example [here](https://github.com/ivanprjcts/equinox-spring16-API).  

Then, it transforms swagger specification files into a custom json model, which makesdks tool will be able to read.

Finally, makesdks tool generate all API Clients from transformed swagger models.


## Requirements

* Python 2.7.+.
* Django 1.9.4.
* django_rest_framework 3.3.2.
* django-rest-swagger 0.3.5.
* sdklib 0.5.2.


## USAGE

* Get Swagger API JSON.
```
tool.py get_swagger_api HOST_URL
```
* Transform Swagger API JSON to our JSON model.
```
tool.py transform_swagger_api
```
* Makesdks from JSON model.
```
tool.py makesdks
```

## Authors

* Iván Martín Vedriel (ivanprjcts@gmail.com).
