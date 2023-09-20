import cv2
import argparse
import imutils

# Ayristirici olustur ve ayristir
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())

# Goruntuyu yukle, grilestir, bulaniklastir, esikle
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# Konturlari bul
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Konturlar üzerinde döngü yap
for c in cnts:
    # Konturun alanini hesapla
    area = cv2.contourArea(c)

    # Alan sifirsa veya cok küçükse (gürültü gibi), atla
    if area < 100:
        continue

    # Konturun momentlerini hesapla
    M = cv2.moments(c)
    # Konturun merkezini hesapla
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # Resmin üzerine şeklin konturunu ve merkezini çiz
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, "merkez", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# Görüntüyü göster
cv2.imshow("Threshold Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()





