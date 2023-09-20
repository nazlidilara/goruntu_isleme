import cv2
import imutils

# Görüntüyü yükleme
image = cv2.imread("C:/Users/Lenovo/Desktop/the-100.jpg")

# Yeni boyutlar
new_width = 400
new_height = 400

# Boyutlandırma 
resized_image = imutils.resize(image, width=new_width, height=new_height)

# Yeniden boyutlandırılmış resim
cv2.imshow("Resized Image", resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()