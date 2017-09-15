from collections import OrderedDict

c_state = 0
c_battery = 1.0
c_storage = '/sdcard/'
c_entries = []
c_tl_info = OrderedDict({})
c_idRes = []

c_default = OrderedDict({
                        "state":'',
                        "version":'',
                        "moduleVersion":'',
                        "origin":{"width":0, "height":0, "framerate":0, "bitrate":0, "mime":'', "saveOrigin":False},
                        "preview":{"width":0, "height":0, "framerate":0, "bitrate":0, "mime":''},
                        "live":{"width":0, "height":0, "framerate":0, "bitrate":0, "mime":'',"url":'', "timePast":0, "timeLeft":0, "liveOnHdmi":False},
                        "record":{"width":0, "height":0, "framerate":0, "bitrate":0, "mime":'', "url":'',"timePast":0, "timeLeft":0},
                        "audio":{"mime":'',"sampleFormat":'',"channelLayout":'',"samplerate":0,"bitrate":0},
                        "url_list":{"_liveUrl":'',"_previewUrl":'', "_recordUrl": ''}
})


