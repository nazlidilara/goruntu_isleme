import cv2
import imutils
import numpy as np
import argparse

# Argümanları ayır
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to image file")
args = ap.parse_args()

# Görüntüyü yükle
image = cv2.imread(args.image)

# Alt ve üst sınırlarını tanımla
lower = np.array([0, 0, 0])   # (BGR formatında)
upper = np.array([15, 15, 15])  

# Maske oluştur
shapeMask = cv2.inRange(image, lower, upper)

# Konturları bul
cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print("{} siyah şekil".format(len(cnts)))
cv2.imshow("mask", shapeMask)

# Konturlar için döngü
for c in cnts:
    # Kontur çizimi
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    
cv2.imshow("Resim", image)
cv2.waitKey(0)
cv2.destroyAllWindows()








