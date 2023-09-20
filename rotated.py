import cv2
import imutils
# Görüntüyü yükleme
image = cv2.imread("C:/Users/Lenovo/Desktop/the-100.jpg")

# Görüntünün boyutlarını al
(h, w) = image.shape[:2]

# Görüntünün merkezini hesapla
center = (w // 2, h // 2)

# Dönüş matrisini hesapla
M = cv2.getRotationMatrix2D(center, -45, 1.0)

# Görüntüyü döndür
rotated = cv2.warpAffine(image, M, (w, h))
#yeni boyut
new_width = 800
new_height = 500
#goruntuyu boyutlandir 
resized_image = imutils.resize(image, width=new_width, height=new_height)
# Döndürülmüş görüntü
cv2.imshow("Rotated and Resized Image", resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()