import cv2
import imutils
#resmi oku
image=cv2.imread("C:/Users/Lenovo/Desktop/the-100.jpg")
#resmi kopyala
output=image.copy()
#cizgi olustur
cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 10)
#yeniden boyutlandir
new_width = 400
new_height = 400
output=imutils.resize(output, width=new_width, height=new_height)
#goruntule
cv2.imshow("output",output)
cv2.waitKey()
cv2.destroyAllWindows()