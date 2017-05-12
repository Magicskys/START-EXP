#coding:utf-8
from PIL import Image
from PIL.ExifTags import TAGS
import os,re,gpsimage
def ImgExif(imgFileName):

    try:
        exifDate={}
        imgFila=Image.open(imgFileName)
        info=imgFila._getexif()
        # print info
        if info:
            for (tag,value) in info.items():
                decoded=TAGS.get(tag,tag)
                exifDate[decoded]=value
            exifGPS=exifDate['GPSInfo']
            if exifGPS:
                print '[*] '+imgFileName+u' 包含GPS元数据'
                img=gpsimage.open(imgFileName)
                print "OK"
                print img.lat,img.lng,img.json
    except:
        print "error"
        pass

def filescan(FileName):
    fileList=[]
    hz=['jpg','png','bmp','gif','jpeg']
    files=os.walk(FileName)
    for path,dirs,file in files:
        print path,dirs,file
        for name in file:
            if re.search('jpg|bmp|jpeg|gif|png',name,re.I):
                fileList.append(path + name)
    for i in fileList:
        # print i
        ImgExif(i)

if __name__ == '__main__':
    # ImgExif("/Users/galan/Downloads/1.jpg")
    filescan("/Users/galan/Pictures/GP")
