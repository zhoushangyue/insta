from collections import OrderedDict
from util.ins_util import dict_to_jsonstr
from camera_server import camera_command
from camera_server import camera_state

class service_osc_state:
    @classmethod
    def get_fingerprint(cls):
        global c
        camera_command.check_state()
        return str(camera_state)

    @classmethod
    def get_batteryLevel(cls):
        camera_command.check_state()
        return camera_state.c_battery

    @classmethod
    def get_storageUri(cls):
        camera_command.check_state()
        return camera_state.c_storage


    @classmethod
    def get_osc_state(cls):
        osc_state = OrderedDict()
        osc_state["fingerprint"] = cls.get_fingerprint()
        osc_state["state"] = OrderedDict({"batteryLevel": cls.get_batteryLevel(),
                                         "storageUri": cls.get_storageUri()})

        _vendorSpecific = OrderedDict()
        osc_state["state"]['_vendorSpecific'] = _vendorSpecific
        return dict_to_jsonstr(osc_state)