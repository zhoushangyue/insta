
from collections import OrderedDict
from util.ins_util import dict_to_jsonstr


class service_osc_info():
    @classmethod
    def get_sn(cls):
        return 'sn123456'

    @classmethod
    def get_version(cls):
        return [1, 2]

    @classmethod
    def get_http_port(cls):
        return 80

    @classmethod
    def get_http_update_port(cls):
        return 20001

    @classmethod
    def get_osc_info(cls):
        osc_info = OrderedDict()
        osc_info['manufacturer'] = 'insta360'
        osc_info['model'] = '360pro'
        osc_info['serialNumber'] = cls.get_sn()
        osc_info['firmwareVersion'] = cls.get_version()
        osc_info['supportUrl'] = '127.0.0.1'
        osc_info['endpoints'] = {'httpPort':cls.get_http_port(), 'httpUpdatePort':cls.get_http_update_port()}
        osc_info['gps'] = True
        osc_info['gyro'] = False
        osc_info['uptime'] = 600

        osc_info['api'] = [
            '/osc/info',
            '/osc/state',
            '/osc/checkForUpdates',
            '/osc/commands/execute',
            '/osc/commands/status'
        ]
        osc_info['apiLevel'] = [2]
        _vendorSpecific = OrderedDict()
        osc_info['_vendorSpecific'] = _vendorSpecific
        return dict_to_jsonstr(osc_info)

