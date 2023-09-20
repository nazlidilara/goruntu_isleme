import numpy as np
import cv2
import argparse
 #bagimsiz degisken olustur ve ayristir
ap=argparse.ArgumentParser()
ap.add_argument("-i" , "--image" , help = "path to the image" )
args=vars(ap.parse_args())
#goruntu yukle
image=cv2.imread(args["image"])
# Yeni boyutları belirle
new_width = 600
new_height = 600

# Görüntüyü yeni boyutlara boyutlandır
resized_image = cv2.resize(image, (new_width, new_height))


# Renk sınırlarını tanımla
sınırlar = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])
]


# Renk sınırları üzerinde döngü yap
for (lower, upper) in sınırlar:
    # NumPy dizilerini sınırlardan oluştur
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    
    # Belirtilen sınırlar arasındaki renkleri içeren maskeyi oluştur
    mask = cv2.inRange(resized_image, lower, upper)
    
    # Maskeyi görüntü üzerine uygula
    output = cv2.bitwise_and(resized_image, resized_image, mask=mask)
    
    # Orijinal ve sonuç görüntülerini birleştirip göster
    cv2.imshow("Images", np.hstack([resized_image, output]))
    cv2.waitKey(0)

cv2.destroyAllWindows()