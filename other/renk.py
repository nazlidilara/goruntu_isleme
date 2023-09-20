import cv2
import argparse
import imutils

# Değişken ayrıştırıcı oluşturup ayrıştır
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# Görüntüyü oku
image = cv2.imread(args["image"])

# Görüntüyü gri tonlamaya çevir
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Eşikleme işlemi
thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]

# Eşiklenmiş görüntüde konturları bul
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Konturları çiz
for c in cnts:
    cv2.drawContours(image, [c], -1, (240, 0, 159), 3)

# Erozyon uygula: Ön plan nesnelerinin boyutunu küçültmek için
mask = thresh.copy()
mask = cv2.erode(mask, None, iterations=5)

# Girdi görüntüsüne maske uygula
output = cv2.bitwise_and(image, image, mask=mask)

# Sonucu göster
cv2.imshow("Output", output)
cv2.waitKey(0)
cv2.destroyAllWindows()