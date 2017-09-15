from util.ins_util import *
import os
class service_osc_statu:
    id = OrderedDict({})

    @classmethod
    def insert_id(cls, ID, ret = OrderedDict):
        cls.id[ID] = ret

    @classmethod
    def delete_id(cls, ID):
        del cls.id[ID]

    @classmethod
    def osc_statu(cls, ID):
        if ID not in cls.id:
            res = set_error("status", "invalidParameterValue", "wrong id value")
        else:
            res = OrderedDict()
            res["name"] = "camera.takePictures"
            res["state"] = "done"
            res["result"] = cls.id[ID]
            res = dict_to_jsonstr(res)
        return res




