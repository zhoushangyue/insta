from osc.osc_info import *
from util.ins_util import *
from osc.osc_state import *
from osc.osc_checkforupdate import *


class execute:

    def __init__(self):
        self.api = OrderedDict({"info": self.info_execute,
                                "state": self.state_execute,
                                "checkForUpdates": self.checkforupdates})

    def osc_api_execute(self, path, data=None):
        if path is "checkForUpdates":
            res = self.api[path](data)
        else:
            if 'parameters' in data:
                res = self.api[path](data['parameters'])
            else:
                res = self.api[path]()
        return res

    def info_execute(self, parameters=None):
        res = service_osc_info.get_osc_info()
        return res

    def state_execute(self, parameters=None):
        res = service_osc_state.get_osc_state()
        return res

    def checkforupdates(self, parameters=None):
        if "stateFingerprint" in parameters and "waitTimeout" in parameters:
            if len(parameters) is 2:
                if service_osc_checkforupdate.check_parameters(parameters):
                    #severerror not define
                    res = service_osc_checkforupdate.get_response_checkforupdate(parameters)
                else:
                    res = set_error("camera.checkForUpdates", "invalidParameterValue", "")
            else:
                res = set_error("camera.checkForUpdates", "invalidParameterName", "")
        else:
            res = set_error("camera.checkForUpdates", "missingParameter", "")
        return res


