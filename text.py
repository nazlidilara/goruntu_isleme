import cv2
#resim oku
image=cv2.imread("C:/Users/Lenovo/Desktop/the-100.jpg")
#resmi kopyala
output = image.copy()
#yazi yaz
cv2.putText(output,"openCV + Bellamy Blake", (650, 450), 
	cv2.FONT_ITALIC , 0.7, (200, 100, 180), 3)

#goruntule
cv2.imshow("text",output)
cv2.waitKey()



