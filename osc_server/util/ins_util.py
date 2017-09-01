import json
from collections import OrderedDict


def dict_to_jsonstr(d):
    return json.dumps(d)


def jsonstr_to_dic(jstr):
    return json.loads(jstr)


def set_error(name="", code="", message=""):
    res = OrderedDict()
    res["name"] = name
    res["state"] = "error"
    res["error"] = OrderedDict({"code": code, "messege": message})
    return dict_to_jsonstr(res)