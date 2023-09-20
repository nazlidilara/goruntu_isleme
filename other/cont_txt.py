import cv2
import imutils
import argparse

# Değişken ayraç oluşturup ayrıştır
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# Resmi oku
image = cv2.imread(args["image"])
output = image.copy()

# Gri tonlama
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]

# Eşiklenen görüntüde konturları bul
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Konturları çiz
for c in cnts:
    cv2.drawContours(output, [c], -1, (240, 0, 159), 3)

# Bulunan nesnelerin sayısını mor renkte görüntüye yaz
text = "{} tane obje buldum!".format(len(cnts))
cv2.putText(output, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (240, 0, 159), 2)

# Sonuçları göster
cv2.imshow("Contours", output)
cv2.waitKey(0)
cv2.destroyAllWindows()