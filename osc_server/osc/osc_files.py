
class onefile:
    def __init__(self,name,size,timeZone="2014:12:27 08:00:00+08:00"):
        self.f_name = name+".jpg"
        self.fileUrl = 'http://192.168.43.1:8000/sdcard/{}'.format(self.f_name)
        self.f_size = size * 1024
        self.dateTimeZone = timeZone
        self.lat = 50.5324
        self.lng = -120.2332
        self.width = 4000
        self.height = 3000
        self.thumbnail = "ENCODEDSTRING"
        self.isProcessed = False
        self.previewUrl = ""


class filelist:
    f1 = onefile("origin_0",4640,"2017:8:28 08:00:00+08:00")
    f2 = onefile("origin_1",4824,"2017:8:27 08:00:00+08:00")

    def __init__(self):
        self.filelist=[self.f1,self.f2]

    def insert_file(self,name,size,timeZone):
        f = onefile(name,size,timeZone)
        self.filelist.insert(0, f)

    def get_len(self):
        return len(self.filelist)
