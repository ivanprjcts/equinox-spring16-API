#!/usr/bin/env python

import sys
import os
import json

from sdklib import SdkBase

from makesdks.writer import PythonSdkWriter
from makesdks.angularjs_writer import AngularJSServiceWriter
from makesdks.swagger_reader import SwaggerReader


def generate_sdks():
    f = open('json/swaggerApi.json', 'r')
    read_file = f.read().replace('\n', '')
    f.close()

    load_json = json.loads(read_file)

    render = PythonSdkWriter(load_json)
    s = render.as_string()

    f = open('outputs/sdk.py', 'w')
    f.write(s)
    f.close()

    render = AngularJSServiceWriter(load_json)
    s = render.as_string()

    f = open('outputs/angular-service.js', 'w')
    f.write(s)
    f.close()


def get_swagger_json_apis(host):

    api = SdkBase()
    api.set_host(host)

    s, res, _ = api._http("GET", "/docs/api-docs/")
    load_json = json.loads(res)

    if not os.path.isdir('json/swagger'):
        os.makedirs('json/swagger')

    for api_json in load_json["apis"]:
        s, res, _ = api._http("GET", "/docs/api-docs%s" % api_json["path"])
        f = open('json/swagger/%s.json'% api_json["path"][1:], 'w')
        f.write(res)
        f.close()


def transform_swagger_json():
    r = SwaggerReader('json/swagger')
    s = r.read_json_apis()

    f = open('json/swaggerApi.json', "w")
    f.write(json.dumps(s))
    f.close()
    print json.dumps(s)


if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == 'makesdks':
        generate_sdks()

    elif len(sys.argv) == 3 and sys.argv[1] == 'get_swagger_api':
        host = sys.argv[2]
        get_swagger_json_apis(host)

    elif len(sys.argv) == 2 and sys.argv[1] == 'transform_swagger_api':
        transform_swagger_json()

    else:
        print("USAGE: %s makesdks" % sys.argv[0])
        print("       %s get_swagger_api HOST_URL" % sys.argv[0])
        print("       %s transform_swagger_api" % sys.argv[0])
