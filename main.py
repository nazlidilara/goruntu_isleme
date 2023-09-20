import cv2

# Görüntüyü yükleme
image = cv2.imread("C:/Users/Lenovo/Desktop/the-100.jpg")

# ROI (İlgilenilen Bölge) çıkarın
roi = image[10:300, 250:400]

# ROI'yu görselleştirme
cv2.imshow("ROI", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()