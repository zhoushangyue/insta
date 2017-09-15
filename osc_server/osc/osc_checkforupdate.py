from collections import OrderedDict
from util.ins_util import dict_to_jsonstr
from osc.osc_state import service_osc_state
import time

class service_osc_checkforupdate:
    @classmethod
    def check_parameters(cls, parameters):
        if type(parameters["stateFingerprint"]) is not str:
            return False
        if type(parameters["waitTimeout"]) is not int or parameters["waitTimeout"] < 0:
            return False
        return True

    @classmethod
    def get_throttleTimeout(cls):
        return 0


    @classmethod
    def get_response_checkforupdate(cls, parameters):
        res = OrderedDict()
        tt = cls.get_throttleTimeout()
        if tt == 0:
            if service_osc_state.get_osc_state() == parameters["stateFingerprint"]:
                time.sleep(parameters["waitTimeout"])
            res["stateFingerprint"] = service_osc_state.get_fingerprint()
            res["throttleTimeout"] = 0
        else:
            res["stateFingerprint"] = service_osc_state.get_fingerprint()
            res["throttleTimeout"] = tt
            #server error define here
        return dict_to_jsonstr(res)
