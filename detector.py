import numpy as np
import imutils
import cv2

class SingleMotionDetector:
    def __init__(self, accumWeight=0.5):
        #agirlik faktoru hesaplama
        self.accumWeight = accumWeight
        #arkaplan baslat
        self.bg = None

    def update(self, image):
        #arkaplan yoksa baslat
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return
        #arkaplani agirlikli ortalama ile guncelle
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    def detect(self, image, tVal=25): 
        #arkaplan ile gelen goruntu arasindaki mutlak farki hesapla
        #delta goruntusunu esik deger ile esikle
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]
#kucuk bolgeleri kaldirmak icin erozyon ve genisleme islemi yap
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

#konturlari bulun hareketin minimum ve max
#sinirlayici kutulari baslat
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

#kontur bulunmadiysa none donsun
        if len(cnts) == 0:
            return None
        #degilse kontur uzeerinde dondur
        for c in cnts:
           #kontur sinirlayici kutusunu hesaplayin
           #hareketin min ve max kutu bolgelerini guncelle
            (x, y, w, h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x + w), max(maxY, y + h))

#esiklenmiş görüntü ve sınırlayıcı kutu bilgisi ile bir tuple döndürün
        return (thresh, (minX, minY, maxX, maxY))
    



