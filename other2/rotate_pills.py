import cv2
import imutils
import argparse

# Argüman ayrıştırıcısı oluştur ve ayrıştır
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# Görüntüyü oku
image = cv2.imread(args["image"])

# Gri tonlama, Gauss filtresi ve kenar algılama uygula
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(gray, 20, 100)

# Görüntüleri göster
cv2.imshow("Original", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

