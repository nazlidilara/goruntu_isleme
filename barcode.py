import numpy as np
import cv2
import imutils
import argparse

# Argüman ayrıştırıcı oluştur
ap = argparse.ArgumentParser()
ap.add_argument("--image", required=True,
                help="path to the image file")
args = vars(ap.parse_args())

# Resmi yükle
image = cv2.imread(args["image"])
if image is None:
    print("Error: Could not load image.")
    exit()

# Görüntüyü gri tonlamaya çevir
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Görüntünün Scharr gradyan büyüklük temsilini hesapla
ddepth = cv2.CV_32F if imutils.is_cv2() else cv2.CV_32F

# Görüntünün x ve y yönlendirmelerine göre Scharr gradyanını hesapla
gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

# x'ten y çıkar
gradient = cv2.subtract(gradX, gradY)

# Gradyanı mutlak değere çevir ve 8 bitlik ölçek aralığına dönüştür
gradient = cv2.convertScaleAbs(gradient)

# Görüntüyü blurla ve eşikle
blurred = cv2.blur(gradient, (9, 9))
(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

# MORPH_RECT ile kare şeklinde bir kernel oluştur
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))

# MORPH_CLOSE işlemi uygula
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Seri erozyon ve dilasyon işlemleri gerçekleştir
closed = cv2.erode(closed, None, iterations=4)
closed = cv2.dilate(closed, None, iterations=4)

# Konturları bul
cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

# En büyük konturun sınırlayıcı kutusunu hesapla
rect = cv2.minAreaRect(c)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(image, [box], -1, (0, 255, 0), 3)

# Sonuçları göster
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()