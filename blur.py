from imutils import paths
import argparse
import cv2
#laplace varyansi hesapla
def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


#arguman ayristirici olustur
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images") # Görüntülerin bulundugu dizinin yolu
ap.add_argument("-t", "--threshold", type=float, default=100.0,
	help="focus measures that fall below this value will be considered 'blurry'") # Eşik değeri
args = vars(ap.parse_args()) 

#tum goruntu yollarini al
imagePaths = sorted(list(paths.list_images(args["images"])))

#dongu yap goruntuleri
#grilestir
for imagePath in imagePaths:
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

fm = variance_of_laplacian(gray) #laplace varyansini hesaplar

#esik degerine gore bulaniklik kontrolu
text = "Sharp"
	if fm < args["threshold"]:
		text = "Blurry"

cv2.putText(image, f"{text}: {fm:.2f}", (10, 30),
cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
cv2.imshow("Image", image)
key = cv2.waitKey(0)


