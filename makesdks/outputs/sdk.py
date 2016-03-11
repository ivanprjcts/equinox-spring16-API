from sdklib import SdkBase


class DefaultApi(SdkBase):

    API_HOST = "api.spring16.equinox.local"

    API_USERS__PK__URL = "/users/%s/"
    API_USERS_URL = "/users/"
    API_APPLICATIONS__PK__URL = "/applications/%s/"
    API_APPLICATIONS_URL = "/applications/"
    API_INSTANCES__PK__URL = "/instances/%s/"
    API_OPERATIONS_URL = "/operations/"
    API_OPERATIONS__PK__URL = "/operations/%s/"
    API_INSTANCES_URL = "/instances/"

    def put_users_pk(self, pk, username, email=None):
        form_params = {"username": username}
        if email is not None:
            form_params["email"] = email

        return self._http("PUT", self.API_USERS__PK__URL % (pk), form_params=form_params)

    def delete_users_pk(self, pk):

        return self._http("DELETE", self.API_USERS__PK__URL % (pk))

    def get_users_pk(self, pk):

        return self._http("GET", self.API_USERS__PK__URL % (pk))

    def patch_users_pk(self, pk, username=None, email=None):
        form_params = dict()
        if username is not None:
            form_params["username"] = username
        if email is not None:
            form_params["email"] = email

        return self._http("PATCH", self.API_USERS__PK__URL % (pk), form_params=form_params)

    def post_users(self, username, email=None):
        form_params = {"username": username}
        if email is not None:
            form_params["email"] = email

        return self._http("POST", self.API_USERS_URL, form_params=form_params)

    def get_users(self, page=None):
        query_params = dict()
        if page is not None:
            query_params["page"] = page
        return self._http("GET", self.API_USERS_URL, query_params=query_params)

    def put_applications_pk(self, pk, name, open=None, description=None):
        form_params = {"name": name}
        if open is not None:
            form_params["open"] = open
        if description is not None:
            form_params["description"] = description

        return self._http("PUT", self.API_APPLICATIONS__PK__URL % (pk), form_params=form_params)

    def delete_applications_pk(self, pk):

        return self._http("DELETE", self.API_APPLICATIONS__PK__URL % (pk))

    def get_applications_pk(self, pk):

        return self._http("GET", self.API_APPLICATIONS__PK__URL % (pk))

    def patch_applications_pk(self, pk, name=None, open=None, description=None):
        form_params = dict()
        if name is not None:
            form_params["name"] = name
        if open is not None:
            form_params["open"] = open
        if description is not None:
            form_params["description"] = description

        return self._http("PATCH", self.API_APPLICATIONS__PK__URL % (pk), form_params=form_params)

    def post_applications(self, name, open=None, description=None):
        form_params = {"name": name}
        if open is not None:
            form_params["open"] = open
        if description is not None:
            form_params["description"] = description

        return self._http("POST", self.API_APPLICATIONS_URL, form_params=form_params)

    def get_applications(self, page=None):
        query_params = dict()
        if page is not None:
            query_params["page"] = page
        return self._http("GET", self.API_APPLICATIONS_URL, query_params=query_params)

    def put_instances_pk(self, pk, name, user, open=None):
        form_params = {"name": name, "user": user}
        if open is not None:
            form_params["open"] = open

        return self._http("PUT", self.API_INSTANCES__PK__URL % (pk), form_params=form_params)

    def delete_instances_pk(self, pk):

        return self._http("DELETE", self.API_INSTANCES__PK__URL % (pk))

    def get_instances_pk(self, pk):

        return self._http("GET", self.API_INSTANCES__PK__URL % (pk))

    def patch_instances_pk(self, pk, name=None, open=None, user=None):
        form_params = dict()
        if name is not None:
            form_params["name"] = name
        if open is not None:
            form_params["open"] = open
        if user is not None:
            form_params["user"] = user

        return self._http("PATCH", self.API_INSTANCES__PK__URL % (pk), form_params=form_params)

    def post_operations(self, name, application, open=None):
        form_params = {"name": name, "application": application}
        if open is not None:
            form_params["open"] = open

        return self._http("POST", self.API_OPERATIONS_URL, form_params=form_params)

    def get_operations(self, page=None):
        query_params = dict()
        if page is not None:
            query_params["page"] = page
        return self._http("GET", self.API_OPERATIONS_URL, query_params=query_params)

    def put_operations_pk(self, pk, name, application, open=None):
        form_params = {"name": name, "application": application}
        if open is not None:
            form_params["open"] = open

        return self._http("PUT", self.API_OPERATIONS__PK__URL % (pk), form_params=form_params)

    def delete_operations_pk(self, pk):

        return self._http("DELETE", self.API_OPERATIONS__PK__URL % (pk))

    def get_operations_pk(self, pk):

        return self._http("GET", self.API_OPERATIONS__PK__URL % (pk))

    def patch_operations_pk(self, pk, name=None, open=None, application=None):
        form_params = dict()
        if name is not None:
            form_params["name"] = name
        if open is not None:
            form_params["open"] = open
        if application is not None:
            form_params["application"] = application

        return self._http("PATCH", self.API_OPERATIONS__PK__URL % (pk), form_params=form_params)

    def post_instances(self, name, user, open=None):
        form_params = {"name": name, "user": user}
        if open is not None:
            form_params["open"] = open

        return self._http("POST", self.API_INSTANCES_URL, form_params=form_params)

    def get_instances(self, page=None):
        query_params = dict()
        if page is not None:
            query_params["page"] = page
        return self._http("GET", self.API_INSTANCES_URL, query_params=query_params)

