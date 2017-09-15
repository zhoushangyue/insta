import requests
import os
from collections import OrderedDict
from util.ins_util import *
from osc.osc_execute import *
from camera_server.camera_state import *
import json


takepicture_seq = OrderedDict({"name": "camera._takePicture",
                                   "parameters":{
                                                 "origin":{"mime":"jpeg", "width":4000, "height":3000, "saveOrigin": False},
                                                 "stiching":{"mode":"pano", "mime":"jpeg", "width":7680, "height":3840, "map":"flat", "algorithm": "normal"},
                                                 "delay":op.exposure_delay,
                                                 "storagePath":'/sdcard/'
                                                  }
                                  })
#"burst":{"enable":False,"count":3},
#"hdr":{"enable":False, "count":3, "min_ev":-32, "max_ev":32},


cameraReq = OrderedDict({"camera.takePicture": takepicture_seq})

class Connect_to_camera():
    def __init__(self):
        self.addr = 'http://127.0.0.1:20000'
        self.Fingerprint = self.connect_to_cameraserver()
        self.keep_alive =True
        self.head = {"Content-Type": "application/json", "Accept": "application/json", "Fingerprint": self.Fingerprint}

    def connect_to_cameraserver(self):
        try:
            heads = {"Content-Type": "application/json", "Accept": "application/json"}
            data_connect = OrderedDict({'name': 'camera._connect'})
            res_connect = requests.post(self.addr+'/osc/commands/execute', headers=heads, json=data_connect).json()
            Fp = res_connect['results']['Fingerprint']
            return Fp
        except Exception as err:
            print("Connect failed:{}".format(err))

    def diconnect_to_cameraserver(self):
        try:
            data_disconnect = OrderedDict({'name': 'camera._disconnect'})
            res_disconnect = requests.post(self.addr + '/osc/commands/execute', headers=self.head, json=data_disconnect).json()
            print('response.status_code {}'.format(res_disconnect))
        except Exception as err:
            print("disConnect failed:{}".format(err))

c = Connect_to_camera()

def camera_takepicture():
    req = cameraReq['camera.takePicture']
    res = requests.post(c.addr + '/osc/commands/execute', headers=c.head, json=req).json()
    print('response.status_code {}'.format(res))
    return res


def update_state():
    res_state = requests.post(c.addr + '/osc/state', headers=c.head).json()
    #print('response.status_code {}'.format(res_state))
    _state = res_state['state']
    # battery
    global c_state,c_battery,c_entries,c_tl_info,c_idRes
    c_state = _state['_cam_state']
    c_battery = 1.0
    c_entries = _state['_external_dev']['entries']
    c_tl_info = _state['_tl_info']
    c_idRes = _state['_idRes']


def check_state():
    update_state()
    return c_state

def http_state():
    while c.keep_alive:
        update_state()
        print("update successful")
        time.sleep(1)
    c.diconnect_to_cameraserver()



    #
    #
    #
    # def camera_take_picture():
    #     Fingerprint = http_connect()
    #     heads = {"Content-Type": "application/json", "Accept": "application/json", "Fingerprint": Fingerprint}
    #     req = cameraReq['camera.takePicture']
    #     res = requests.post(dest_addr + '/osc/commands/execute', headers=heads, json=req).json()
    #     print('response.status_code {}'.format(res))
    #     if res['state'] == 'error':
    #         res['state'] == 'inProgress'
    #     diconnect_to_cameraserver(Fingerprint)
    #     return res

        # def search_options(options=OrderedDict()):
        #     res = OrderedDict()
        #     for e in options.keys():
        #         if e in op.default_index.keys():
        #             res[e] = op.default_index[e]
        #         else:
        #             res[e] = None
        #     return res
        #
        # def set_fingerprint(fp):
        #     global fingerprint
        #     fingerprint = fp
        #
        # def get_fingerprint():
        #     return fingerprint


        # def http_connect(url='/osc/commands/execute', param=None):
        #     try:
        #         heads = {"Content-Type": "application/json", "Accept": "application/json"}
        #         if "Fingerprint" in heads:
        #             print("exi:"+heads["Fingerprint"])
        #         data_connect = OrderedDict({'name': 'camera._connect'})
        #         data_disconnect = OrderedDict({'name': "camera._disconnect"})
        #         res_connect = requests.post(dest_addr + url, headers=heads, json=data_connect).json()
        #         set_fingerprint(res_connect['results']["Fingerprint"])
        #         print('Fingerprint{}'.format(fingerprint))
        #         print('response.status_code {}'.format(res_connect))
        #         heads["Fingerprint"] = get_fingerprint()
        #
        #         res = requests.post(dest_addr + url, headers=heads, json=param).json()
        #         print('response.status_code {}'.format(res))
        #         print('res '+res['state'])
        #
        #         res_disconnect = requests.post(dest_addr + url, headers=heads, json=data_disconnect)
        #         print('response.status_code {}'.format(res_disconnect))
        #         # if response.status_code == requests.codes.ok:
        #         #     resp = response.json()
        #         # return jsonstr_to_dic(resp)
        #         return res
        #     except Exception as err:
        #         print('err ', err)
        # def check_state():
        #     Fingerprint = http_connect()
        #     heads = {"Content-Type": "application/json", "Accept": "application/json", "Fingerprint": Fingerprint}
        #     update_state(heads)
        #     diconnect_to_cameraserver(Fingerprint)
        #     if camera_state.c_state == 0:
        #         return True
        #     else:
        #         print("c_state:{}".format(camera_state.c_state))
        #         return False
        #
        #
        #
        # def camera_take_picture():
        #     Fingerprint = http_connect()
        #     heads = {"Content-Type": "application/json", "Accept": "application/json", "Fingerprint": Fingerprint}
        #     req = cameraReq['camera.takePicture']
        #     res = requests.post(dest_addr + '/osc/commands/execute', headers=heads, json=req).json()
        #     print('response.status_code {}'.format(res))
        #     if res['state'] == 'error':
        #         res['state'] == 'inProgress'
        #     diconnect_to_cameraserver(Fingerprint)
        #     return res

    #diconnect_to_cameraserver(Fingerprint)



