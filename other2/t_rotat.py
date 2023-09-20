# Gerekli kütüphaneleri içe aktar
import numpy as np
import argparse
import imutils
import cv2

# argüman ayrıştırıcısını oluştur ve ayrıştır
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the image file")
args = vars(ap.parse_args())

# görüntüyü yükle
image = cv2.imread(args["image"])

# görüntüyü belli açıyla döndür
for angle in np.arange(0, 360, 45):
    rotated = imutils.rotate(image, angle)
    cv2.imshow("Döndür (Sorunlu)", rotated)
    cv2.waitKey(0)

# görüntüyü belli açıyla döndür (doğru yöntem)
for angle in np.arange(0, 360,45 ):
    rotated = imutils.rotate_bound(image, angle)
    cv2.imshow("Döndürülmüş (Doğru)", rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
