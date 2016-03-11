import os
import json


from sdklib.util.urlvalidator import urlsplit


class SwaggerReader(object):

    def __init__(self, folder):
        files = os.listdir(folder)

        self.apis = []
        for file_elem in files:
            print '%s/%s' % (folder, file_elem)
            f = open('%s/%s' % (folder, file_elem), 'r')
            read_file = f.read().replace('\n', '')
            f.close()

            load_json = json.loads(read_file)
            self.apis.append(load_json)


    def read_json_apis(self):
        json_model = dict()
        for api in self.apis:
            scheme, host, port = urlsplit(api["basePath"])
            if scheme and "scheme" not in json_model:
                json_model["scheme"] = scheme
            if host and "apiHost" not in json_model:
                json_model["apiHost"] = host
            if port and "port" not in json_model:
                json_model["port"] = port

            for method in api["apis"]:
                if "urls" not in json_model:
                    json_model["urls"] = dict()

                methods = dict()
                operations = method["operations"]
                for operation in operations:
                    methods[operation["method"]] = operation["parameters"]
                json_model["urls"][method["path"]] = methods

        return json_model


if __name__ == "__main__":
    r = SwaggerReader('json/swagger')
    s = r.read_json_apis()

    f = open('json/swaggerApi.json', "w")
    f.write(json.dumps(s))
    f.close()
    print json.dumps(s)

