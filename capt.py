from webcamvideostream import WebcamVideoStream
class VideoStream:
    def __init__(self, src=0, usePiCamera=False, resolution=(320, 240), framerate=32):
        # Eğer PiCamera kullanılması gerekiyorsa
        if usePiCamera:
            # Picamera modülü kullanılması gerektiğinde, 
            # sadece picamera paketlerini içe aktarın masaüstü veya dizüstü bilgisayarların hala `imutils` paketini kullanabileceği gereksinimini kaldırmaya yardımcı olur
            from pivideostream import PiVideoStream
            # Picamera akışını başlatın ve kameranın sensörünün ısınmasına izin verin
            self.stream = PiVideoStream(resolution=resolution, framerate=framerate)
        #  OpenCV kullanıyorsak
        else:
            self.stream = WebcamVideoStream(src=src)


 # çoklu iş parçacıklı video akışı            
 def start(self):
    return self.stream.start() #video baslat

def update(self):
    self.stream.update()  #sonraki goruntuyu al

def read(self):
    return.self.stream.read() #mevcut goruntu dondur

def stop(self):
    self.stream.stop()   #durdur 
           










