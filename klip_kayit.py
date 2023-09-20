from collections import deque
from threading import Thread
from queue import Queue
import time
import cv2

class KeyClipWriter:
    def__init__(self, bufSize=64, timeout=1.0):
    # Bellekte tutulacak maksimum kare boyutunu ve iş parçacığı sırasında uyuma süresini sakla
        self.bufSize = bufSize
        self.timeout = timeout
        # dosyaya yazılması gereken karelerin kuyruğunu, video yazıcısını, yazıcı iş parçacığını
        # ve kaydın başlayıp başlamadığını belirten bir boolean değerini başlat
        self.frames = deque(maxlen=bufSize)
        self.Q = None
        self.writer = None
        self.thread = None
        self.recording = False
def update(self, frame):
    # Kare güncelle
    self.frames.appendleft(frame)
    
    # Eğer kayıt yapılıyorsa, kuyruğu da güncelle
    if self.recording:
        self.Q.put(frame)

def start (self,outputPath,fourcc,fps):
   # Kaydedilmekte olduğunu belirt, video yazıcısını başlat ve video dosyasına yazılması gereken karelerin kuyruğunu başlat 
self.recording = True
    self.writer = cv2.VideoWriter(outputPath,fourcc,fps,
                           (self.frames[0].shape[1], self.frames[0].shape[0]), True)       )

    self.Q = Queue()


# Tampon yapısındaki kareleri döngü ile gezip kuyruğa ekleyin
    for i in range(len(self.frames), 0, -1):
        self.Q.put(self.frames[i - 1])
        
    # Karelere video dosyasına yazmak için bir iş parçacığı başlat
    self.thread = Thread(target=self.write, args=())
    self.thread.daemon = True
    self.thread.start()

def write(self):
    # Sürekli döngüde kal
    while True:
        # Eğer kayıt işlemi tamamlandıysa, iş parçacığından çık
        if not self.recording:
            return
        # Kuyrukta girişlerin olup olmadığını kontrol et
        if not self.Q.empty():
            # Kuyruktaki sonraki kareyi al ve video dosyasına yaz
            kare = self.Q.get()
            self.writer.write(kare)
        # kuyruk boş,CPU  boşa harcamamak için uyu
        else:
            time.sleep(self.timeout)
def flush(self):
    # Kuyruğu boşaltarak tüm kalan kareleri dosyaya yaz
    while not self.Q.empty():
        kare = self.Q.get()
        self.writer.write(kare)

def finish(self):
    # Kaydın tamamlandığını belirt, iş parçacığını birleştir,
    # kuyruktaki tüm kalan kareleri dosyaya yaz ve yazıcıyı serbest bırak
    self.recording = False
    self.thread.join()
    self.flush()
    self.writer.release()

