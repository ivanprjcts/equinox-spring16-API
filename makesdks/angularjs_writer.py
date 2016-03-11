import re

from makesdks.writer import SdkWriter


class AngularJSServiceWriter(SdkWriter):

    @staticmethod
    def _get_camel_case_name(name):
        return name.lower()

    @staticmethod
    def _generate_url_name_var(path):
        clean_url = path
        if clean_url[0] == '/':
            clean_url = clean_url[1:]
        if clean_url[-1] == '/':
            clean_url = clean_url[0:-1]
        clean_url = clean_url.replace("/", "_")
        clean_url = clean_url.replace("{", "_")
        clean_url = clean_url.replace("}", "_")
        return "API_%s_URL" % clean_url.upper()

    @staticmethod
    def _generate_url_string_value(path):
        clean_path = re.sub(r"{(?P<var>\w+)}", "{X}", path)
        count = 0
        while "{X}" in clean_path:
            clean_path = clean_path.replace("{X}", "{%d}"%count, 1)
            count += 1
        return clean_path

    @staticmethod
    def _get_vars_from_url(path):
        find_all = re.findall(r"{\w+}", path)
        vars = []
        for var in find_all:
            clean_var = var.replace("{", "")
            clean_var = clean_var.replace("}", "")
            clean_var = clean_var.strip()
            if clean_var not in vars:
                vars.append(clean_var)
        return vars

    def _get_urls_and_methods_as_string(self):
        url_vars = []
        methods_as_string = ''
        urls_as_string = ''
        for url in self.json_model["urls"]:
            url_var = "%s" % self._generate_url_name_var(url)
            if url_var not in url_vars:
                url_val = self._generate_url_string_value(url)
                urls_as_string += ANGULAR_JS_URL_TEMPLATE % ("var %s"%url_var, url_val)
                url_vars.append(url_var)

            path_params = self._get_vars_from_url(url)
            final_url = "%s" % url_var
            if path_params:
                final_url += '.format('
                for param in path_params:
                    final_url += param
                    final_url += ', '
                final_url = final_url[0:-2] + ')'

            for method in self.json_model["urls"][url]:
                parameters = self.json_model["urls"][url][method]

                input_args = AngularJSServiceWriter._get_args_parameters_as_string(parameters)
                form_params = AngularJSServiceWriter._get_form_parameters_as_string(parameters)
                query_params = AngularJSServiceWriter._get_query_parameters_as_string(parameters)
                extra_args = ''
                if query_params:
                    extra_args += ', query_params'
                else:
                    extra_args += ', null'
                if form_params:
                    extra_args += ', form_params'
                else:
                    extra_args += ', null'

                methods_as_string += ANGULAR_JS_METHOD_TEMPLATE % (
                    method.lower(),
                    self._generate_method_name_var(url),
                    input_args,
                    form_params,
                    query_params,
                    method,
                    final_url,
                    extra_args
                )

        return urls_as_string, methods_as_string

    @staticmethod
    def _get_args_parameters_as_string(parameters):
        args_as_string = ''
        if not parameters:
            return ''

        for parameter in parameters:
            if parameter["paramType"] == 'path':
                args_as_string += "%s, " % AngularJSServiceWriter._get_camel_case_name(parameter["name"])
        for parameter in parameters:
            if parameter["paramType"] == 'form':
                args_as_string += "%s, " % AngularJSServiceWriter._get_camel_case_name(parameter["name"])
        for parameter in parameters:
            if parameter["paramType"] == 'query':
                args_as_string += "%s, " % AngularJSServiceWriter._get_camel_case_name(parameter["name"])
        return "%s" % args_as_string[0:-2]

    @staticmethod
    def _get_form_parameters_as_string(parameters):
        parameters_as_string = ''
        if not parameters:
            return ''

        has_no_required_parameters = False
        for parameter in parameters:
            if parameter["paramType"] == "form" and "required" in parameter and  parameter["required"]:
                parameters_as_string += '"%s": %s, ' % (parameter["name"], AngularJSServiceWriter._get_camel_case_name(parameter["name"]))
        if parameters_as_string:
            has_required_parameters = True
            parameters_as_string = parameters_as_string[0:-2]
            parameters_as_string = ANGULAR_JS_FORM_PARAMETERS_TEMPLATE % (parameters_as_string)
        else:
            has_required_parameters = False

        for parameter in parameters:
            if parameter["paramType"] == "form" and "required" in parameter and not parameter["required"]:
                has_no_required_parameters = True
                parameters_as_string += '        if (%s != null)\n' % (AngularJSServiceWriter._get_camel_case_name(parameter["name"]))
                parameters_as_string += '            form_params["%s"] = %s;\n' % (parameter["name"], AngularJSServiceWriter._get_camel_case_name(parameter["name"]))

        if not has_required_parameters and has_no_required_parameters:
            parameters_as_string = "        var form_params = {};\n" + parameters_as_string
        return parameters_as_string

    @staticmethod
    def _get_query_parameters_as_string(parameters):
        parameters_as_string = ''
        if not parameters:
            return ''

        for parameter in parameters:
            if parameter["paramType"] == 'query':
                parameters_as_string += '        if (%s != null)\n' % (
                    AngularJSServiceWriter._get_camel_case_name(parameter["name"])
                )
                parameters_as_string += '            query_params["%s"] = %s;' % (
                    parameter["name"],
                    AngularJSServiceWriter._get_camel_case_name(parameter["name"])
                )
        if parameters_as_string:
            parameters_as_string = "        var query_params = {};\n" + parameters_as_string
        return parameters_as_string

    def _generate_method_name_var(self, path):
        clean_url = path
        if clean_url[0] == '/':
            clean_url = clean_url[1:]
        if clean_url[-1] == '/':
            clean_url = clean_url[0:-1]
        clean_url = clean_url.replace("/", "_")
        clean_url = clean_url.replace("{", "")
        clean_url = clean_url.replace("}", "")
        return clean_url.lower()

    def as_string(self):
        api_name = self.json_model["apiName"] if "apiName" in self.json_model else "Default"
        urls_string, methods_string = self._get_urls_and_methods_as_string()
        return ANGULAR_JS_SERVICE_TEMPLATE % (
            api_name,
            api_name,
            urls_string,
            self.json_model["apiHost"],
            methods_string
        )


ANGULAR_JS_FORM_PARAMETERS_TEMPLATE = """        var form_params = {%s};\n"""

ANGULAR_JS_URL_TEMPLATE = """    %s = "%s";\n"""

ANGULAR_JS_METHOD_PARAMETERS_TEMPLATE = """%s, """
ANGULAR_JS_METHOD_TEMPLATE = '''    var %s_%s = function(%s){
%s%s
        return _http("%s", %s%s)
    };

'''


ANGULAR_JS_SERVICE_TEMPLATE = '''
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


var app = angular.module('%s', ['ngCookies']);

app.service('%sApi', ['$http', '$cookies', function($http, $cookies) {

%s

    var X_CSRF_TOKEN_HEADER_NAME = "X-CSRFToken";
    var COOKIE_HEADER_NAME = "Cookie";

    var config = {
        host: '%s',
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

%s
}]);
'''