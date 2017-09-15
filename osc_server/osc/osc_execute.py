from collections import OrderedDict
from util.ins_util import *
from osc.osc_statu import *
from osc.osc_options import service_osc_option
from camera_server import camera_command
import time
from osc.osc_files import *


fl = filelist()
op = service_osc_option()

class service_osc_cmd_execute:

    @classmethod
    def cmd_takepictures(cls,parameters=OrderedDict()):
        if camera_command.check_state() != 0:
            return set_error("camera.takePicture", "disabledCommand", "Command is currently disabled.")
        if len(parameters) != 0:
            return set_error("camera.takePicture", "invalidParameterName", "Parameter options contains unsupported")
        else:
            resp = camera_command.camera_takepicture()
            if resp['state'] == 'error':
                return set_error("camera.takePicture", "disabledCommand", "Command is currently disabled.")
            else:
                if type(resp["sequence"]) is not str:
                    cmd_id = str(resp["sequence"])
                else:
                    cmd_id = resp["sequence"]
                service_osc_statu.insert_id(cmd_id, {"fileUrls":"http://192.168.43.1:8000/sdcard/pano.jpg"})
                res = OrderedDict()
                res["name"] = "camera.takePicture"
                res["state"] = "inProgress"
                res["id"] = cmd_id
            res = dict_to_jsonstr(res)
            fl.insert_file('pano',22008,op.date_time_zone)
        return res

    @classmethod
    def cmd_setoption(cls, parameters=OrderedDict()):
        try:
            res = None
            if "options" not in parameters.keys():
                print(1)
                res = set_error("camera.setOptions","missingParameter","One or more required parameters is missing")
            else:
                for e in parameters["options"].keys():
                    print(str(e)+":"+str(parameters["options"][e]))
                    if e not in op.default_index.keys() and e not in op.support_index.keys():
                        print(e)
                        res = set_error("camera.setOption", "invalidParameterName","Parameter options contains unsupported option "+e+".")
                        break
                    elif op.check_value(e, parameters["options"][e]) is False:
                        print(e)
                        res = set_error("camera.setOptions","invalidParameterValue","Parameter options contains unsupported option value "+e+".")
                        break
                    op.default_index[e] = parameters["options"][e]
                 # change options
        except Exception as err:
            print("setoptions error "+str(err))
            res = None
        return res


    @classmethod
    def cmd_getoption(cls, parameters):
        print
        try:
            res = None
            if "optionNames" not in parameters.keys():
                res = set_error("camera.getOptions", "missingParameter", "One or more required parameters is missing")
            else:

                for e in parameters["optionNames"]:
                    if e not in op.default_index.keys() and e not in op.support_index.keys():
                        print(2)
                        res = set_error("camera.getOption", "invalidParameterName", "Parameter options contains unsupported option"+e)
                if res is None:
                    options = OrderedDict()
                    for e in parameters["optionNames"]:
                        if e in op.default_index.keys():
                            options[e] = op.default_index[e]
                        elif e in op.support_index.keys():
                            options[e] = op.support_index[e]
                    resp = OrderedDict()
                    resp["name"] = "camera.getOptions"
                    resp["state"] = "done"
                    resp["results"] = OrderedDict({"options": options})
                    res = dict_to_jsonstr(resp)
        except Exception as err:
            print("getoptions error "+str(err))
            res = None
        return res

    @classmethod
    def cmd_list_file(cls,parameters = OrderedDict()):
        pa = ['fileType','startPosition','entryCount','maxThumbSize']
        if "entryCount" not in parameters.keys() or "maxThumbSize" not in parameters.keys():
            res = set_error("camera.listFiles","missingParameter","miss Parameter entryCount or maxThumbSize")
            return res
        for e in parameters.keys():
            if e not in pa:
                res = set_error("camera.listFiles", "invalidParameterName","invalidParameterName "+e)
                return res

        print("file_type:{}".format(parameters['fileType']))
        L = []
        for e in fl.filelist:
            i = {
            "name":e.f_name,
            "fileUrl":e.fileUrl,
            "size":e.f_size,
            "dateTimeZone": e.dateTimeZone,
            "lat": e.lat,
            "lng": e.lng,
            "width": e.width,
            "height": e.height,
            "thumbnail": e.thumbnail,
            "isProcessed": e.isProcessed,
            "previewUrl": e.previewUrl
            }
            L.append(i)

        resp = OrderedDict()
        resp["state"] = "done"
        resp["name"] = "camera.listFiles"
        resp["results"]={"entries": L,
                        "totalEntries": fl.get_len()
                        }
        return dict_to_jsonstr(resp)

    @classmethod
    def cmd_startcapture(cls,parameters=None):
        # judge camera working disable
        if parameters != None:
            res = set_error("camera.startCapture", "invalidParameterName")
        elif op.capture_mode == 'vedio' or op.capture_num == 0:
            res =None
        else:
            # <capture_num takepictures
            # return res
            resp = OrderedDict()
            resp["state"] = "done"
            resp["name"] = "camera.startCapture"
            resp["results"] = {
                                "fileUrls":[
                                            "http://192.168.43.1:8000/sdcard/origin_2.jpg",
                                            "http://192.168.43.1:8000/sdcard/origin_3.jpg"
                                            ]
                              }
            res = dict_to_jsonstr(resp)
        return res

    @classmethod
    def cmd_stopcapture(cls, parameters=None):
        #judge camera working disable
        if parameters == None:
            res = set_error("camara.stopCapture", "invalidParameterName")
        elif op.capture_mode != 'interval':
            res = set_error("camera.stopCapture", "disabledCommand")
        else:
            resp = OrderedDict()
            resp["state"] = "done"
            resp["name"] = "camera.listFiles"
            resp["results"] = {
                "fileUrls": [
                    "http://192.168.43.1:8000/sdcard/origin_2.jpg",
                    "http://192.168.43.1:8000/sdcard/origin_3.jpg"
                ]
            }
            res = dict_to_jsonstr(resp)
        return res

    @classmethod
    def URI_resolve_path(cls, urimessage):
        _path = os.environ.get('HOME')
        urimes = urimessage.split('/')
        for i in range(3, len(urimes)):
            _path += '/'
            _path += urimes[i]
        return _path

    @classmethod
    def cmd_reset(cls,parameters=None):
        if parameters is not None:
            return set_error("camera.reset","invalidParameterName","invalid Parameters")
        #back to default
        return None

    @classmethod
    def cmd_delete(cls,parameters=None):
        if "fileUrls" not in parameters.keys:
                return set_error("camera.delete", "missingParameter")
        for e in parameters.keys():
            if e is not "fileUrls":
                return set_error("camera.delete", "invalidParameterName", "invalidParameterName:" + e)
        result=OrderedDict({"fileUrls":[]})
        for e in parameters["fileUrls"]:
            path1 = cls.URI_resolve_path(e)
            if os.path.exists(path1) is False:
                return set_error("camera.getImage", "invalidParameterValue")
            try:
                os.remove(path1)
            except Exception as err:
                result['fileUrls'].append(path1)
        if len(result['fileUrls'])==0:
            return None
        resp = OrderedDict()
        resp["state"] = "done"
        resp["name"] = "camera.listFiles"
        resp["results"] = result
        res = dict_to_jsonstr(resp)
        return res


    @classmethod
    def get_cmd_response(cls, name, parameters=OrderedDict()):

        cmd_CONFIG = OrderedDict({"camera.takePicture": cls.cmd_takepictures,
                                "camera.setOptions": cls.cmd_setoption,
                                "camera.getOptions": cls.cmd_getoption,
                                "camera.listFiles": cls.cmd_list_file,
                                "camera.startCapture":cls.cmd_startcapture,
                                "camera.stopCapture":cls.cmd_stopcapture,
                                "camera.reset":cls.cmd_reset,
                                "camera.delete":cls.cmd_delete})

        print("cmdname: "+name)

        res = cmd_CONFIG[name](parameters)

        check = jsonstr_to_dic(res)
        for e in check.keys():
            print(check[e])
        return res
