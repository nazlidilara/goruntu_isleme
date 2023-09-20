import cv2 
import argparse
import imutils

# Değişken ayrıştırıcı oluşturup ayrıştır
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# Resim okunur
image = cv2.imread(args["image"])
# Gri tonlama uygulanır
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Eşikleme işlemi 
thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]

# Eşiklenmiş görüntüyü göster
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()