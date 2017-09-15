from osc.osc_info import *
from util.ins_util import *
from osc.osc_state import *
from osc.osc_checkforupdate import *
from osc.osc_execute import *
from camera_server.camera_command import *


class execute:

    def __init__(self):
        self.api = OrderedDict({"info": self.info_execute,
                                "state": self.state_execute,
                                "checkForUpdates": self.checkforupdates})

    def osc_api_execute(self, path, data=OrderedDict()):
        res = self.api[path](data)
        return res

    def info_execute(self, parameters=OrderedDict()):
        res = service_osc_info.get_osc_info()
        return res

    def state_execute(self, parameters=OrderedDict()):
        res = service_osc_state.get_osc_state()
        return res

    def checkforupdates(self, parameters=OrderedDict()):
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

    def osc_cmd_execute(self, data=OrderedDict()):
        if "name" in data:
            if "parameters" in data:
                res = service_osc_cmd_execute.get_cmd_response(data["name"], data["parameters"])
            else:
                res = service_osc_cmd_execute.get_cmd_response(data["name"])
        else:
            print("no name")
            res = set_error("camera.execute", "noCommandname", "")
        return res


