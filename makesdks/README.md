# makesdks

Tool for auto-generate sdks from a Django rest framework API.


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
