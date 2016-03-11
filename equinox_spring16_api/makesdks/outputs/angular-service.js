
String.prototype.format = function()
{
   var content = this;
   for (var i=0; i < arguments.length; i++)
   {
        var replacement = '{' + i + '}';
        content = content.replace(replacement, arguments[i]);
   }
   return content;
};


var app = angular.module('Default', ['ngCookies']);

app.service('DefaultApi', ['$http', '$cookies', function($http, $cookies) {

    var API_USERS__PK__URL = "/users/{0}/";
    var API_USERS_URL = "/users/";
    var API_APPLICATIONS__PK__URL = "/applications/{0}/";
    var API_APPLICATIONS_URL = "/applications/";
    var API_INSTANCES__PK__URL = "/instances/{0}/";
    var API_OPERATIONS_URL = "/operations/";
    var API_OPERATIONS__PK__URL = "/operations/{0}/";
    var API_INSTANCES_URL = "/instances/";


    var X_CSRF_TOKEN_HEADER_NAME = "X-CSRFToken";
    var COOKIE_HEADER_NAME = "Cookie";

    var config = {
        host: 'api.spring16.equinox.local',
        headers:  {
            'Content-Type': 'application/json'
        }
    };

    var urlEncode = function(obj) {
        var str = [];
        for(var p in obj)
            if (obj.hasOwnProperty(p)) {
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
            }
        return str.join("&");
    };

    var defaultHeaders = function() {
        var csrftoken = $cookies.get("csrftoken") || "";

        var xHeaders = config.headers;
        xHeaders[X_CSRF_TOKEN_HEADER_NAME] = csrftoken;
        return xHeaders;
    };

    var _http = function(method, path, query_params, data, headers, transformRequest) {
        query_params = query_params || null;
        data = data || null;
        headers = headers || defaultHeaders();
        transformRequest = transformRequest || null;
        var url = config.host + path;

        if (transformRequest != null)
            var req = {
                method: method,
                url: url,
                headers: headers,
                params: query_params,
                data: data,
                transformRequest: transformRequest
            };
        else
            var req = {
                method: method,
                url: url,
                headers: headers,
                params: query_params,
                data: data,
            };

        return $http(req);
    };

    var put_users_pk = function(pk, username, email){
        var form_params = {"username": username};
        if (email != null)
            form_params["email"] = email;

        return _http("PUT", API_USERS__PK__URL.format(pk), null, form_params)
    };

    var delete_users_pk = function(pk){

        return _http("DELETE", API_USERS__PK__URL.format(pk), null, null)
    };

    var get_users_pk = function(pk){

        return _http("GET", API_USERS__PK__URL.format(pk), null, null)
    };

    var patch_users_pk = function(pk, username, email){
        var form_params = {};
        if (username != null)
            form_params["username"] = username;
        if (email != null)
            form_params["email"] = email;

        return _http("PATCH", API_USERS__PK__URL.format(pk), null, form_params)
    };

    var post_users = function(username, email){
        var form_params = {"username": username};
        if (email != null)
            form_params["email"] = email;

        return _http("POST", API_USERS_URL, null, form_params)
    };

    var get_users = function(page){
        var query_params = {};
        if (page != null)
            query_params["page"] = page;
        return _http("GET", API_USERS_URL, query_params, null)
    };

    var put_applications_pk = function(pk, name, open, description){
        var form_params = {"name": name};
        if (open != null)
            form_params["open"] = open;
        if (description != null)
            form_params["description"] = description;

        return _http("PUT", API_APPLICATIONS__PK__URL.format(pk), null, form_params)
    };

    var delete_applications_pk = function(pk){

        return _http("DELETE", API_APPLICATIONS__PK__URL.format(pk), null, null)
    };

    var get_applications_pk = function(pk){

        return _http("GET", API_APPLICATIONS__PK__URL.format(pk), null, null)
    };

    var patch_applications_pk = function(pk, name, open, description){
        var form_params = {};
        if (name != null)
            form_params["name"] = name;
        if (open != null)
            form_params["open"] = open;
        if (description != null)
            form_params["description"] = description;

        return _http("PATCH", API_APPLICATIONS__PK__URL.format(pk), null, form_params)
    };

    var post_applications = function(name, open, description){
        var form_params = {"name": name};
        if (open != null)
            form_params["open"] = open;
        if (description != null)
            form_params["description"] = description;

        return _http("POST", API_APPLICATIONS_URL, null, form_params)
    };

    var get_applications = function(page){
        var query_params = {};
        if (page != null)
            query_params["page"] = page;
        return _http("GET", API_APPLICATIONS_URL, query_params, null)
    };

    var put_instances_pk = function(pk, name, open, user){
        var form_params = {"name": name, "user": user};
        if (open != null)
            form_params["open"] = open;

        return _http("PUT", API_INSTANCES__PK__URL.format(pk), null, form_params)
    };

    var delete_instances_pk = function(pk){

        return _http("DELETE", API_INSTANCES__PK__URL.format(pk), null, null)
    };

    var get_instances_pk = function(pk){

        return _http("GET", API_INSTANCES__PK__URL.format(pk), null, null)
    };

    var patch_instances_pk = function(pk, name, open, user){
        var form_params = {};
        if (name != null)
            form_params["name"] = name;
        if (open != null)
            form_params["open"] = open;
        if (user != null)
            form_params["user"] = user;

        return _http("PATCH", API_INSTANCES__PK__URL.format(pk), null, form_params)
    };

    var post_operations = function(name, open, application){
        var form_params = {"name": name, "application": application};
        if (open != null)
            form_params["open"] = open;

        return _http("POST", API_OPERATIONS_URL, null, form_params)
    };

    var get_operations = function(page){
        var query_params = {};
        if (page != null)
            query_params["page"] = page;
        return _http("GET", API_OPERATIONS_URL, query_params, null)
    };

    var put_operations_pk = function(pk, name, open, application){
        var form_params = {"name": name, "application": application};
        if (open != null)
            form_params["open"] = open;

        return _http("PUT", API_OPERATIONS__PK__URL.format(pk), null, form_params)
    };

    var delete_operations_pk = function(pk){

        return _http("DELETE", API_OPERATIONS__PK__URL.format(pk), null, null)
    };

    var get_operations_pk = function(pk){

        return _http("GET", API_OPERATIONS__PK__URL.format(pk), null, null)
    };

    var patch_operations_pk = function(pk, name, open, application){
        var form_params = {};
        if (name != null)
            form_params["name"] = name;
        if (open != null)
            form_params["open"] = open;
        if (application != null)
            form_params["application"] = application;

        return _http("PATCH", API_OPERATIONS__PK__URL.format(pk), null, form_params)
    };

    var post_instances = function(name, open, user){
        var form_params = {"name": name, "user": user};
        if (open != null)
            form_params["open"] = open;

        return _http("POST", API_INSTANCES_URL, null, form_params)
    };

    var get_instances = function(page){
        var query_params = {};
        if (page != null)
            query_params["page"] = page;
        return _http("GET", API_INSTANCES_URL, query_params, null)
    };


}]);
