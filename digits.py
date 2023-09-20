from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2

# Rakamları tanımla
DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 1, 0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}

# Resmi yükle
image = cv2.imread("C:/Users/Lenovo/Desktop/example.jpg")

# Resmi yeniden boyutlandır, gri tonlamaya dönüştür, bulanıklaştır ve kenarları tespit et
image = imutils.resize(image, height=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 50, 200, 255)

# Kenar haritasındaki konturları bul
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)  # Kontur listesini al

# Konturları alanlarına göre sırala ve en büyük konturu seç
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None  # Termostat ekranının konturu

# Konturlar üzerinde döngü yap
for c in cnts:
    # Konturu yaklaşıklaştır
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # Kontur 4 köşe noktasına sahipse, termostat ekranını bulduk
    if len(approx) == 4:
        displayCnt = approx  # Termostat ekranının konturunu kaydet
        break  # Diğer konturları kontrol etmeyi durdur

warped = four_point_transform(gray, displayCnt.reshape(4, 2))
output = four_point_transform(image, displayCnt.reshape(4, 2))

# Warped görüntüyü eşikleyerek, ardından eşiklenmiş görüntüyü temizlemek için dizi morfolojik işlem uygula
thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Morfolojik işlem yapmak için bir kernel oluştur (genellikle dairesel şekiller kullanılır)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))

# Açma işlemi ile görüntüyü temizle
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# Eşiklenmiş görüntüdeki konturları bul
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
digitCnts = []  # Sayı kontur listesi

# Konturlar üzerinde döngü yap
for c in cnts:
    # Konturun kutusunu hesapla
    (x, y, w, h) = cv2.boundingRect(c)

    # Eğer kontur belirli boyutlarda ise sayı konturu
    if w >= 15 and (h >= 30 and h <= 40):
        digitCnts.append(c)

# Sayı konturlarını sırala
digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]
digits = []

# Her bir sayı üzerinde döngü yap
for c in digitCnts:
    # Sayı ROI'sini çıkart
    (x, y, w, h) = cv2.boundingRect(c)
    roi = thresh[y:y + h, x:x + w]

    # Her bir 7 segmentin genişliğini ve yüksekliğini hesapla
    (roiH, roiW) = roi.shape
    (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
    dHC = int(roiH * 0.05)

    # 7 segmentin koordinatlarını tanımla
    segments = [
        ((0, 0), (w, dH)),  # üst
        ((0, 0), (dW, h // 2)),  # sol üst
        ((w - dW, 0), (w, h // 2)),  # sağ üst
        ((0, (h // 2) - dHC), (w, (h // 2) + dHC)),  # orta
        ((0, h // 2), (dW, h)),  # sol alt
        ((w - dW, h // 2), (w, h)),  # sağ alt
        ((0, h - dH), (w, h))  # alt
    ]

    on = [0] * len(segments)  # Her bir segmentin yanıp sönme durumunu depolamak için liste oluştur

   
# Sonuçları ekrana yazdır
print("Recognized digits:", digits)

cv2.imshow("Input", image)
cv2.imshow("Output", output)
cv2.waitKey(0)
cv2.destroyAllWindows()






