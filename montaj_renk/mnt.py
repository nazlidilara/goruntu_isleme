from imutils import build_montages
from imutils import paths
import argparse
import random
import cv2

# Argüman ayrıştırıcısını oluştur ve ayrıştır
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input image directory")
ap.add_argument("-s", "--sample", type=int, default=21,   
	help="# of images to sample")   # Örnek alınacak görüntü sayısını belirtir
args = vars(ap.parse_args())    #komut satırından verilen argümanları ayrıştırır ve bunları bir sözlüğe (args) yerleştirir


# Görüntü yollarını al ve rastgele örnek seç
imagePaths = list(paths.list_images(args["images"]))
random.shuffle(imagePaths)
imagePaths = imagePaths[:args["sample"]]

# Seçilen görüntüleri depolamak için liste oluştur
images = []

# Seçilen görüntülerin yollarını dönerek görüntüleri listeye ekle
for imagePath in imagePaths:
    # Görüntüyü yükle ve listeye ekle
    image = cv2.imread(imagePath)
    images.append(image)

# Montajları oluştur
montages = build_montages(images, (128, 196), (7, 3))

# Oluşturulan montajları dönerek göster
for montage in montages:
    cv2.imshow("Montage", montage)
    cv2.waitKey(0)