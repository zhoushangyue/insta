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


def unify_float(f, num=2):
    return round(f, num)

def set_result(name,res_from_camera=None):
    res = OrderedDict()
    res['name'] = name
    if res_from_camera is None:
        return None
    elif res_from_camera['state'] == 'error':
        res['state'] = 'error'
    else:
        res['result'] = res_from_camera['result']
    return res