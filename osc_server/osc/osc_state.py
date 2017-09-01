from collections import OrderedDict
from util.ins_util import dict_to_jsonstr

class service_osc_state:
    @classmethod
    def get_fingerprint(cls):
        return '1234567890'

    @classmethod
    def get_batteryLevel(cls):
        return 1.0

    @classmethod
    def get_storageUri(cls):
        return "/"


    @classmethod
    def get_osc_state(cls):
        osc_state = OrderedDict()
        osc_state["fingerprint"] = cls.get_fingerprint()
        osc_state["state"] = OrderedDict({"batteryLevel": cls.get_batteryLevel(),
                                         "storageUri": cls.get_storageUri()})

        _vendorSpecific = OrderedDict()
        osc_state["state"]['_vendorSpecific'] = _vendorSpecific
        return dict_to_jsonstr(osc_state)