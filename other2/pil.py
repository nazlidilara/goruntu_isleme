import cv2 
import imutils
import argparse
import numpy as np

# Argüman ayrıştırıcısını oluştur ve ayrıştır
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to input image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])

# Gri tonlamayı uygula
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(gray, 20, 100)

# Kenar haritasında konturları bul
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Eğer en az bir kontur bulunduysa devam et
if len(cnts) > 0:
    # En büyük konturu seç, ardından pillerin maskelemesi için bir maske çiz
    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(gray.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)
    
    # Konturun sınırlama kutusunu hesapla ve ROI(region of interest ilgi alani) çıkar
    (x, y, w, h) = cv2.boundingRect(c) #sinirlayici dortgen olusturur
    imageROI = image[y:y + h, x:x + w] #orijinal resmi temsil eder
    maskROI = mask[y:y + h, x:x + w]  #maskeli goruntu
    
    #x ve y değerleri, sınırlayıcı kutunun sol üst köşesinin koordinatlarını, w ve h ise sırasıyla genişlik ve yüksekliği temsil eder
    
    # Maskeyi uygula
    imageROI = cv2.bitwise_and(imageROI, imageROI, mask=maskROI)

    # Görüntüleri göster
    cv2.imshow("Original", image)
    cv2.imshow("Edged", edged)
    cv2.imshow("Masked", imageROI)
    cv2.waitKey(0)
    cv2.destroyAllWindows()






