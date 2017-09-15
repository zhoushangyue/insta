
from collections import OrderedDict
from util.ins_util import *

class service_osc_option:
    def __init__(self):
        self.default_index = OrderedDict({"captureMode": self.capture_mode,
                                     "exposureProgram": self.exposure_program,
                                     "iso": self.iso,
                                     "shutterSpeed": self.shutter,
                                     "aperture": self.aperture,
                                     "whiteBalance": self.white_balance,
                                     "exposureCompensation": self.exposure_compensation,
                                     "fileFormat": self.file_format,
                                     "exposureDelay": self.exposure_delay,
                                     "sleepDelay": self.sleep_delay,
                                     "offDelay": self.off_delay,
                                     "totalSpace": self.total_space,
                                     "remainingSpace": self.remaining_space,
                                     "remainingPictures": self.remaining_pic,
                                     "gpsInfo": self.gps_info,
                                     "dateTimeZone": self.date_time_zone,
                                     "hdr": self.hdr,
                                     "exposureBracket": self.exposure_bracket,
                                     "gyro": self.gyro,
                                     "gps": self.gps,
                                     "imageStabilization": self.image_stabilization,
                                     "wifiPassword": self.wifi_pwd,
                                     "previewFormat": self.preview_format_support,
                                     "captureInterval": self.capture_interval,
                                     "captureNumber": self.capture_num,
                                     "remainingVideoSeconds": self.remain_video_sec,
                                     "pollingDelay": self.polling_delay,
                                     "delayProcessing": self.delay_processing,
                                     "clientVersion": self.client_version,
                                     })

        self.support_index = OrderedDict({"captureModeSupport": self.capture_mode_support,
                                     "exposureProgramSupport": self.exposure_program_support,
                                     "isoSupport": self.iso_support,
                                     "shutterSpeedSupport": self.shutter_support,
                                     "apertureSupport": self.aperture_support,
                                     "whiteBalanceSupport": self.white_balance_support,
                                     "exposureCompensationSupport": self.exposure_compensation_support,
                                     "fileFormatSupport": self.file_format_support,
                                     "exposureDelaySupport": self.exposure_delay_support,
                                     "sleepDelaySupport": self.sleep_delay_support,
                                     "offDelaySupport": self.off_delay_support,
                                     "hdrSupport": self.hdr_support,
                                     "exposureBracketSupport":self.exposure_bracket_support,
                                     "shotsSupport": self.shots_support,
                                     "incrementSupport": self.increment_support,
                                     "imageStabilizationSupport": self.image_stabilization,
                                     "_bitrateSupport": self.bitrate_support,
                                     "framerateSupport": self.framerate_support,
                                     "previewFormatSupport":self.preview_format_support,
                                     "captureIntervalSupport": self.capture_interval_support,
                                     "captureNumberSupport": self.capture_num_support,
                                     })

    def check_value(self, proper, value):
        try:
            if proper+"Support" in self.support_index:
                if proper == "exposureBracket" or proper == "previewFormat":
                    for e in self.support_index[proper+"Support"]:
                        notmatch = False
                        for i in e.keys():
                            if e[i] == "support" and self.check_value(i, value[i]) == False:
                                return False
                            elif e[i] != value[i]:
                                notmatch = True
                                break
                        if not notmatch:
                            return True
                    return False
                elif proper == "captureNumber":
                    if value >= self.capture_num_support["minNumber"] and value <=self.capture_num_support["maxNumber"]:
                        return True
                    return False
                elif proper == "captureInterval":
                    if value >= self.capture_interval_support["minInterval"] and value <self.capture_interval_support["maxInterval"]:
                        return True
                    return False
                else:
                    if value in self.support_index[proper+"Support"]:
                        return True
                    return False
            return True
        except Exception as err:
            print("checkvalueerror"+str(err))
            return False

    capture_mode = 'image'
    capture_mode_support = ['image', 'interval']

    exposure_program = 0
    exposure_program_support = ['Not defined','Manual','Normal program','Aperture priority','Shutter priority','ISO priority']

    iso = 0
    iso_support = [0, 100, 200, 400, 800, 1600]

    shutter = 0
    shutter_support = [0, 0.067, 0.033, 0.017, 0.008]

    aperture = 0
    aperture_support = [0, unify_float(1.4), 2, unify_float(2.8), 4, unify_float(5.6), 8, 11]
    # incandescent, around 3200K
    # fluorescent, around 4000K
    # datalight, around 5200K
    # cloudy-daylight, around 6000K
    # shade, around 7000K
    # twilight, around 12000K
    white_balance = "auto"
    white_balance_support = ["auto", "incandescent", "fluorescent", "daylight",
                             "cloudy-daylight", "shade", "twilight"]

    exposure_compensation = -1
    exposure_compensation_support = [-1, unify_float(-0.67), unify_float(-0.33), 0,
                             unify_float(0.33), unify_float(0.67), 1]

    file_format = {
                   "type": "jpeg",
                   "width": 2000,
                   "height": 1000
                  }
    file_format_support = [
        {
            "type": "jpeg",
            "width": 2000,
            "height": 1000
        },
        {
            "type": "jpeg",
            "width": 200,
            "height": 100
        }
    ]

    sleep_delay = 30
    sleep_delay_support = [30, 60, 120, 300, 600, 1800, 65535]

    exposure_delay = 0
    exposure_delay_support = [0, 1, 2, 5, 10, 30, 60]

    off_delay = 1800
    off_delay_support = [1800, 3600, 7200, 65535]

    total_space = 0

    remaining_space = 0

    remaining_pic = 0

    gps_info = {
        "lat": 0.00,
        "lng": 0.00}

    date_time_zone = '2014:05:18 01:04:29+08:00'

    hdr = 'off'
    hdr_support = ['off', 'hdr', 'hdr1', 'hdr2']

    # # {
    # #     "shots": 3,
    # #     "increment": 1.33
    # # }
    # # {
    # #     "autoMode": true
    # # }
    #
    exposure_bracket = {
                        "autoMode": True
                       }

    exposure_bracket_support = [{"autoMode": True},
                                {"shots": "support",
                                "incrementSupport": "support"}]
    shots_support = [1, 3, 5, 7]
    increment_support = [0.33, 0.67, 1, 1.33, 1.67, 2]

    gyro = False
    gps = False

    # gyro_sup = False
    # gps_sup = False

    image_stabilization = "off"
    image_stabilization_support = ["off", "_horizontal_stabilization", "_vibration_correction"]

    preview_format ={
                        "width": 1920,
                        "height": 960,
                        "framerate": 30,
                        "_bitrate": 2048
                    }
    
    bitrate_support = [2048, 1024]
    framerate_support = [30, 15]

    preview_format_support = [
        {
            "width": 1920,
            "height": 960,
            "framerate": "support",
            "_bitrate": "support",
        },
        {
            "width": 1440,
            "height": 720,
            "_bitrate": "support",
            "framerate": "support"
        },
        {
            "width": 960,
            "height": 480,
            "_bitrate": "support",
            "framerate": "support"
        }
    ]

    wifi_pwd = '66666666'

    capture_interval = 10
    capture_interval_support = {"minInterval": 10, "maxInterval": 60}

    capture_num = 2
    capture_num_support = {"minNumber": 2, "maxNumber": 50}

    remain_video_sec = 0
    polling_delay = 0
    delay_processing = True
    delay_processing_support =[True, False, [True, False]]
    client_version = 2

    # photoStitching
    # photoStitching_support

    # videoStitching
    # videoStitching_support

    # videoGPS
    # videoGPS_support


    # pano

    _vr_mode = "pano"
    _vr_mode_support = ["pano", "support"]

    _vendor_specific_support = {"_vr_mode":_vr_mode, "_vr_mode_support": _vr_mode_support}

    # cur_format_def = \
    # {
    #     'pano':
    #     {
    #         'preview':
    #         {
    #             "width": 1920,
    #             "height": 960,
    #             "framerate": 30,
    #             "_bitrate": 2048,
    #         },
    #         'live':
    #         {
    #             "width": 1920,
    #             "height": 960,
    #             "framerate": 30,
    #             "_bitrate": 2048
    #         },
    #         'record':
    #         {
    #             "width": 4096,
    #             "height": 2048,
    #             "framerate": 30,
    #             "_bitrate": 30 * 1024
    #         },
    #         'photo':
    #         {
    #             "width": 8192,
    #             "height": 4096,
    #         },
    #     },
    # }
    #
    # pic_format_def = \
    # OrderedDict({
    #     "type":"jpeg",
    #     "width":8192,
    #     "height":4096,
    # })
    #
    # live_format_def = \
    #     OrderedDict({'width': 1920, 'height': 960, 'framerate': 30, '_bitrate': 2048})
    #
    # rec_format_def = \
    #     OrderedDict({'width': 4096, 'height': 2048, 'framerate': 30, '_bitrate': 30 * 1024})
    #
    # all_format = \
    # {
    #     'pano':
    #     {
    #         'preview':
    #         [
    #         {
    #             "width": 1920,
    #             "height": 960,
    #             "framerate": framerate,
    #             "_bitrate": _bitrate
    #         },
    #         {
    #             "width": 1440,
    #             "height": 720,
    #             "framerate": framerate,
    #             "_bitrate": _bitrate
    #         },
    #         {
    #             "width": 1280,
    #             "height": 720,
    #             "framerate": framerate,
    #             "_bitrate": _bitrate
    #
    #         }],
    #         'live':
    #         [
    #         {
    #             "width": 1920,
    #             "height": 960,
    #             "framerate": framerate,
    #             "_bitrate": _bitrate
    #         },
    #         {
    #             "width": 1440,
    #             "height": 720,
    #             "framerate": framerate,
    #             "_bitrate": _bitrate
    #         },
    #         {
    #             "width": 1280,
    #             "height": 720,
    #             "framerate": framerate,
    #             "_bitrate": _bitrate
    #
    #         }],
    #         'record':
    #         [
    #             {
    #                 "width": 4096,
    #                 "height": 2048,
    #                 "framerate": [30],
    #                 "_bitrate": [30 * 1024]
    #             },
    #             {
    #                 "width": 2880,
    #                 "height": 1440,
    #                 "framerate": [30],
    #                 "_bitrate": [20 * 1024]
    #             },
    #             {
    #                 "width": 1920,
    #                 "height": 960,
    #                 "framerate": [30],
    #                 "_bitrate": [15 * 1024]
    #             }
    #         ],
    #         'photo':
    #         [
    #             {
    #                 "width": 8192,
    #                 "height": 4096,
    #             },
    #             {
    #                 "width": 4096,
    #                 "height": 2048,
    #             },
    #             {
    #                 "width": 2048,
    #                 "height": 1024,
    #             }
    #         ],
    #     },
    #     config.MODE_3D:
    #     {
    #         'preview':
    #         [
    #             {
    #                 "width": 960,
    #                 "height": 960,
    #                 "framerate": [15],
    #                 "_bitrate": [2048]
    #             },
    #             {
    #                 "width": 640,
    #                 "height": 640,
    #                 "framerate": [15],
    #                 "_bitrate": [2048]
    #             }
    #             ],
    #         'live':
    #         [
    #             {
    #                 "width": 1920,
    #                 "height": 1920,
    #                 "framerate": [30],
    #                 "_bitrate": [4*1024]
    #             },
    #             {
    #                 "width": 1440,
    #                 "height": 1440,
    #                 "framerate": [30],
    #                 "_bitrate": [3*1024]
    #             },
    #             {
    #                 "width": 960,
    #                 "height": 960,
    #                 "framerate": [30],
    #                 "_bitrate": [2*1024]
    #
    #             }],
    #         'record':
    #         [
    #             {
    #                 "width": 3840,
    #                 "height": 3840,
    #                 "framerate": [25],
    #                 "_bitrate": [50*1024]
    #             },
    #             {
    #                 "width": 1920,
    #                 "height": 1920,
    #                 "framerate": [30],
    #                 "_bitrate": [25 * 1024]
    #             },
    #             {
    #                 "width": 960,
    #                 "height": 960,
    #                 "framerate": [30],
    #                 "_bitrate": [15 * 1024]
    #             }
    #         ],
    #         'photo':
    #         [
    #             {
    #                 "width": 8192,
    #                 "height": 8192,
    #             },
    #             {
    #                 "width": 4096,
    #                 "height":4096,
    #             },
    #             {
    #                 "width": 2048,
    #                 "height": 2048,
    #             }
    #         ],
    #     }
    # }
    #
    # _shutter_vo_support = {'min': 0, 'max': 10}
    #
    # def_k_v = \
    # {
    #     'captureMode':capture_mode[0],
    #     'captureModeSupport':capture_mode,
    #     'exposureProgram':exposure_prog[0],
    #     'exposureProgramSupport': exposure_prog,
    #     'iso':iso[0],
    #     'isoSupport': iso,
    #     'shutterSpeed':shutter[0],
    #     'shutterSpeedSupport':shutter,
    #     'aperture':aperture[0],
    #     'apertureSupport': aperture,
    #     'whiteBalance':white_balance[0],
    #     'whiteBalanceSupport':white_balance,
    #     'exposureCompensation':exposure_compensation[0],
    #     'exposureCompensationSupport':exposure_compensation,
    #     'fileFormat':file_format[0],
    #     'fileFormatSupport': file_format,
    #     'exposureDelay':exposure_delay[0],
    #     'exposureDelaySupport': exposure_delay,
    #     'sleepDelay':sleep_delay[0],
    #     'sleepDelaySupport': sleep_delay,
    #     'offDelay':off_delay[0],
    #     'offDelaySupport': off_delay,
    #     'totalSpace':total_space,
    #     'remainingSpace':remaining_space,
    #     'remainingPictures':remaining_pic,
    #     'gpsInfo':gps_info,
    #     'dateTimeZone':date_time_zone,
    #     'hdr':hdr_sup[0],
    #     'hdrSupport':hdr_sup,
    #     # 'shots_index':shots_index,
    #     # 'increment_index':increment_index,
    #     #start
    #     'gyro': gyro,
    #     'gyroSupport': gyro_sup,
    #     'gps': gps,
    #     'gpsSupport':gps_sup,
    #     'imageStabilization': image_stabilization,
    #     'imageStabilizationSupport': image_stabilization,
    #     'wifiPassword': wifi_pwd,
    #     config.PREVIEW_FORMAT: preview_format_def,
    #     'previewFormatSupport': preview_format,
    #     'captureInterval': 0,
    #     'captureIntervalSupport':capture_interval,
    #
    #     'captureNumber': capture_num_def,
    #     'captureNumberSupport': capture_num,
    #     'remainingVideoSeconds':remain_video_sec,
    #
    #     'pollingDelay':polling_delay,
    #     'delayOrocessing':delay_processing,
    #     'delayProcessingSupport':delay_processing_sup,
    #     'clientVersion':client_version,
    #
    #     #sepcial while setOption
    #     'exposureBracket': exposure_bracket_def,
    #     '_vendorSpecific':_vendor_specific,
    #     '_cur_format':cur_format_def,
    #     '_all_format':all_format,
    #     '_wifi_state':0,
    #     #0 - 10
    #     '_shutter_vol': 0,
    #     '_shutter_vo_support':_shutter_vo_support,
    #     config.PIC_FORMAT:pic_format_def,
    #     config.LIVE_FORMAT: live_format_def,
    #     config.REC_FORMAT: rec_format_def,
    #     config.VR_MODE:vr_mode_def
    # }
