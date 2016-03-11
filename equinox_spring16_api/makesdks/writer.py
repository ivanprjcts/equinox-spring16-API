import re


class SdkWriter(object):

    def __init__(self, json_obj):
        self.json_model = json_obj


class PythonSdkWriter(SdkWriter):

    @staticmethod
    def _get_pythonic_name(name):
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
        clean_path = re.sub(r"{(?P<var>\w+)}", "%s", path)
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
            url_var = self._generate_url_name_var(url)
            if url_var not in url_vars:
                url_val = self._generate_url_string_value(url)
                urls_as_string += PYTHON_SDK_URL_TEMPLATE % (url_var, url_val)
                url_vars.append(url_var)

            path_params = self._get_vars_from_url(url)
            final_url = "self.%s" % url_var
            if path_params:
                final_url += ' % ('
                for param in path_params:
                    final_url += param
                    final_url += ', '
                final_url = final_url[0:-2] + ')'

            for method in self.json_model["urls"][url]:
                parameters = self.json_model["urls"][url][method]

                input_args = PythonSdkWriter._get_args_parameters_as_string(parameters)
                form_params = PythonSdkWriter._get_form_parameters_as_string(parameters)
                query_params = PythonSdkWriter._get_query_parameters_as_string(parameters)
                extra_args = ''
                if form_params:
                    extra_args += ', form_params=form_params'
                if query_params:
                    extra_args += ', query_params=query_params'

                methods_as_string += PYTHON_SDK_METHOD_TEMPLATE % (
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
            if parameter["paramType"] == 'path' and parameter["required"]:
                args_as_string += "%s, " % PythonSdkWriter._get_pythonic_name(parameter["name"])
        for parameter in parameters:
            if parameter["paramType"] == 'form' and parameter["required"]:
                args_as_string += "%s, " % PythonSdkWriter._get_pythonic_name(parameter["name"])
        for parameter in parameters:
            if parameter["paramType"] == 'path' and not parameter["required"]:
                args_as_string += "%s=None, " % PythonSdkWriter._get_pythonic_name(parameter["name"])
        for parameter in parameters:
            if parameter["paramType"] == 'form' and not parameter["required"]:
                args_as_string += "%s=None, " % PythonSdkWriter._get_pythonic_name(parameter["name"])
        for parameter in parameters:
            if parameter["paramType"] == 'query':
                args_as_string += "%s=None, " % PythonSdkWriter._get_pythonic_name(parameter["name"])
        return ", %s" % args_as_string[0:-2]

    @staticmethod
    def _get_form_parameters_as_string(parameters):
        parameters_as_string = ''
        if not parameters:
            return ''

        has_no_required_parameters = False
        for parameter in parameters:
            if parameter["paramType"] == "form" and "required" in parameter and  parameter["required"]:
                parameters_as_string += '"%s": %s, ' % (parameter["name"], PythonSdkWriter._get_pythonic_name(parameter["name"]))
        if parameters_as_string:
            has_required_parameters = True
            parameters_as_string = parameters_as_string[0:-2]
            parameters_as_string = PYTHON_SDK_FORM_PARAMETERS_TEMPLATE % (parameters_as_string)
        else:
            has_required_parameters = False

        for parameter in parameters:
            if parameter["paramType"] == "form" and "required" in parameter and not parameter["required"]:
                has_no_required_parameters = True
                parameters_as_string += '        if %s is not None:\n' % (PythonSdkWriter._get_pythonic_name(parameter["name"]))
                parameters_as_string += '            form_params["%s"] = %s\n' % (parameter["name"], PythonSdkWriter._get_pythonic_name(parameter["name"]))

        if not has_required_parameters and has_no_required_parameters:
            parameters_as_string = "        form_params = dict()\n" + parameters_as_string
        return parameters_as_string

    @staticmethod
    def _get_query_parameters_as_string(parameters):
        parameters_as_string = ''
        if not parameters:
            return ''

        for parameter in parameters:
            if parameter["paramType"] == 'query':
                parameters_as_string += '        if %s is not None:\n' % (
                    PythonSdkWriter._get_pythonic_name(parameter["name"])
                )
                parameters_as_string += '            query_params["%s"] = %s' % (
                    parameter["name"],
                    PythonSdkWriter._get_pythonic_name(parameter["name"])
                )
        if parameters_as_string:
            parameters_as_string = "        query_params = dict()\n" + parameters_as_string
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
        return PYTHON_SDK_TEMPLATE % (
            api_name,
            self.json_model["apiHost"],
            urls_string,
            methods_string
        )


PYTHON_SDK_FORM_PARAMETERS_TEMPLATE = """        form_params = {%s}\n"""

PYTHON_SDK_URL_TEMPLATE = """    %s = "%s"\n"""

PYTHON_SDK_METHOD_PARAMETERS_TEMPLATE = """, %s"""
PYTHON_SDK_METHOD_TEMPLATE = '''    def %s_%s(self%s):
%s%s
        return self._http("%s", %s%s)

'''


PYTHON_SDK_LIST_METHOD_TEMPLATE = '''    def list_%s(self):
        return self._http("GET", %s)'''


PYTHON_SDK_TEMPLATE = '''from sdklib import SdkBase


class %sApi(SdkBase):

    API_HOST = "%s"

%s
%s'''