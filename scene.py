import argparse
import imutils
import cv2
import os

#arguman ayristirici olustur

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, type=str, #hareket tespiti yapılacak video
	help="path to input video file")
ap.add_argument("-o", "--output", required=True, type=str, #ayiklanan çerçevelerin nereye kaydedileceği
	help="path to output directory to store frames")
ap.add_argument("-p", "--min-percent", type=float, default=1.0, # Hareket tespiti için kabul edilen minimum yüzde
	help="lower boundary of percentage of motion")
ap.add_argument("-m", "--max-percent", type=float, default=10.0, #Hareket tespiti için kabul edilen maksimum yüzde
	help="upper boundary of percentage of motion")
ap.add_argument("-w", "--warmup", type=int, default=200,   # Bir arka plan modeli oluşturmak için kullanılan çerçeve sayısı
	help="# of frames to use to build a reasonable background model")
args = vars(ap.parse_args())

#arka plan cikarici baslat
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

#cercevenin yakalanma durumu
captured = False
total = 0
frames = 0

#video ac
vs = cv2.VideoCapture(args["video"])
(W, H) = (None, None) #cerceve genislik yukseklik 

# Video çerçeveleri üzerinde döngü oluştur
while True:
	# Videodan bir çerçeve al
	(grabbed, frame) = vs.read()

	#  video dosyasının sonuna geldi
	if frame is None:
		break

	# Orijinal çerçeveyi (sonradan kaydetmek için) klonla, çerçeveyi yeniden boyutlandır
	# ve ardından arkaplan çıkarıcı uygula
	orig = frame.copy()
	frame = imutils.resize(frame, width=600)
	mask = fgbg.apply(frame)

	# Gürültü için erozyon ve dilasyon uygula
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# genişlik ve yükseklik bilgileri boşsa, maske boyutlarını al
	if W is None or H is None:
		(H, W) = mask.shape[:2]

	#"foreground" olarak kabul edilen yüzdesini hesapla
	p = (cv2.countNonZero(mask) / float(W * H)) * 100


# Eğer çerçevenin "foreground"  yüzdesi N% değerinin altındaysa ve daha önce yakalanmamışsa
# ve çerçeve sayısı ısınma süresi  sonrası ise, o zaman çerçeveyi yakalamalıyız
if p < args["min_percent"] and not captured and frames > args["warmup"]:
	# Yakalanan çerçeveyi göster ve yakalama durumu değişkenini güncelle
	cv2.imshow("Captured", frame)
	captured = True

	# Çıkış çerçevesinin yolunu oluştur ve toplam çerçeve sayısını artır
	filename = "{}.png".format(total)
	path = os.path.sep.join([args["output"], filename])
	total += 1

	# Yüksek çözünürlüklü *orijinal* çerçeveyi diske kaydet
	print("[INFO] kaydediliyor {}".format(path))
	cv2.imwrite(path, orig)

# Aksi takdirde, ya sahne değişiyor ya da hala ısınma aşamasındayız,
# bu nedenle sahnenin sakinleşmesini veya arkaplan modelinin tamamlanmasını beklemeliyiz
# veya sıcaklık aşamasını  bitireceğimiz süreyi beklemeliyiz
elif captured and p >= args["max_percent"]:
	captured = False

cv2.imshow("Frame", frame)
cv2.imshow("Mask", mask)
key = cv2.waitKey(1) & 0xFF

if key == ord("q"):
    break

#kare sayacini arttir
frames += 1
vs.release()
