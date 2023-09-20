import cv2
import imutils

#goruntu yukle bulaniklastir grilestir
image=cv2.imread("C:/Users/Lenovo/Desktop/hand.jpg")
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blurred=cv2.GaussianBlur(gray,(5,5),0)

#goruntuyu esik,erozyon ve genişletme işlemleri ile kontur bulmaya calisilir
thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)

#konturlari bul,en buyugunu al
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)
 
# kontur boyunca en uç noktaları belirle
extLeft = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])


# Konturu çiz
cv2.drawContours(image, [c], -1, (0, 255, 255), 2)

# Sol ucunu belirtmek icin bir daire çiz
cv2.circle(image, extLeft, 8, (0, 0, 255), -1)

# Sağ ucunu belirtmek icin bir daire çiz
cv2.circle(image, extRight, 8, (0, 255, 0), -1)

# Üst ucunu belirtmek icin bir daire çiz
cv2.circle(image, extTop, 8, (255, 0, 0), -1)

# Alt ucunu belirtmek icin bir daire çiz
cv2.circle(image, extBot, 8, (255, 255, 0), -1)

# Çıktı görüntüyü göster
cv2.imshow("Image", image)
cv2.waitKey(0)