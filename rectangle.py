import cv2
#goruntu oku
image=cv2.imread("C:/Users/Lenovo/Desktop/the-100.jpg")
#resmi kopyala
rectangle=image.copy()
#dikdortgen ciz
cv2.rectangle(rectangle, (250, 80), (440, 260), (0, 0, 255), 2)
# Mavi renkte içi dolu 20 piksel yarıçaplı bir daire çiz
cv2.circle(rectangle, (500, 150), 20, (	130 ,10 ,130), -1)


#son halini goster
cv2.imshow("rectangle",rectangle)
cv2.waitKey(0)
cv2.destroyAllWindows()