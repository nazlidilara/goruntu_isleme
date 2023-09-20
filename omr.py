from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

# Argüman ayrıştırıcı oluştur
ap = argparse.ArgumentParser()
ap.add_argument("--i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())

# Cevap anahtarını tanımla
ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}  # 0 anahtarı ilk soruyu belirtirken, 1 değeri doğru cevap olarak "B" yi belirtir

# Görüntüyü yükle, gri tonlamalı hale getir, bulanıklaştır, kenarları tespit et
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)
#kenar konturlarini bul
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
docCnt = None

if len(cnts) > 0:
    # Konturları büyüklüklerine göre sırala
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    
    # Sıralanmış konturlar üzerinde döngü yap
    for c in cnts:
        # Konturu yaklaşık olarak çiz
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        # Eğer kontur dört noktaya sahipse
        if len(approx) == 4:
            docCnt = approx
            # Döngüyü sonlandır
            break

#Dört noktalı bir perspektif dönüşümü uygulayarak hem orijinal görüntüye hem de gri tonlamalı görüntüye, kağıdın üstten görülen bir kuşbakışı görünüm
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))
#otsu(optimum eşik değerini otomatik olarak hesaplar) esikleme yontemiyle esikleme yap
thresh = cv2.threshold(warped, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1] #eşiklenmiş piksel değerlerini tersine çevirir (siyah ve beyazı ters) 

#kontur bul
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
questionCnts = []
for c in cnts:
	# Konturun sınırlayıcı kutusunu hesapla, ardından sınırlayıcı kutuyu kullanarak en-boy oranını türet
	(x, y, w, h) = cv2.boundingRect(c) 
	ar = w / float(h)
	# Konturu bir soru olarak etiketlemek için bölgenin yeterince geniş, yeterince yüksek ve
	# yaklaşık olarak 1'e eşit bir en-boy oranına sahip olması gerekir
	if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
		questionCnts.append(c)

# Soru konturlarını yukarıdan aşağıya doğru sırala, ardından doğru cevapların toplam sayısını başlat
questionCnts = contours.sort_contours(questionCnts,
	method="top-to-bottom")[0]
correct = 0
# Her bir sorunun 5 olası cevabı vardır, bu nedenle 5'lik gruplar halinde soruları döngü içinde gezeceğiz
for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
	# Geçerli soru için konturları soldan sağa doğru sırala, ardından kabarmış cevap indeksini başlat
	cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
	bubbled = None
        
# Sıralanmış konturları döngü ile gezip işlemleri yap
for (j, c) in enumerate(cnts):
	# Geçerli "kabarcık" için sadece o bölgenin görünmesini sağlayan bir maske oluştur
	mask = np.zeros(thresh.shape, dtype="uint8")
	cv2.drawContours(mask, [c], -1, 255, -1)
	# Maskeyi eşiklenmiş görüntüye uygula, sonra kabarcık alanındaki toplam sıfır olmayan pikselin sayısını say
	mask = cv2.bitwise_and(thresh, thresh, mask=mask)
	total = cv2.countNonZero(mask)
	# Eğer geçerli toplam daha büyük bir sıfır olmayan piksel sayısına sahipse,
	# o zaman şu an işaretlenmiş olan cevabı inceliyoruz
	if bubbled is None or total > bubbled[0]:
		bubbled = (total, j)

color = (0, 0, 255)  # Kontur rengi (kırmızı)
k = ANSWER_KEY[q]  # İncelenen sorunun doğru cevabının indeksi
# Eğer işaretlenen cevap doğru ise, rengi yeşil yap
if k == bubbled[1]:
	color = (0, 255, 0)  # Yeşil renk
	correct += 1  # Doğru cevap sayısını artır
# Test kağıdının üzerine doğru cevabın dış çizgisini çiz
cv2.drawContours(paper, [cnts[k]], -1, color, 3)

# Sonucu hesapla ve ekrana yazdır
score = (correct / 5.0) * 100  # Doğru cevap yüzdesini hesapla
print("[INFO] score: {:.2f}%".format(score))  # Yüzdeyi ekrana yazdır

# Sonucu test kağıdının üzerine yazdır
cv2.putText(paper, "{:.2f}%".format(score), (10, 30),
	cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

# Orijinal ve işlenmiş görüntüleri göster
cv2.imshow("Original", image)  # Orijinal görüntüyü göster
cv2.imshow("Exam", paper)  # İşlenmiş test kağıdını göster
cv2.waitKey(0)


