import cv2
import time

# Kamerayı aç
cap = cv2.VideoCapture(0)

# Kaydedilecek görüntülerin dizini
output_dir = "kaydedilen_goruntuler/"

# Görüntü numarası
frame_num = 1

while True:
    # Görüntüyü yakala
    ret, frame = cap.read()

    # Görüntüyü göster
    cv2.imshow('Kamera', frame)

    # Klavyeden bir tuşa basıldığında
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Görüntüyü kaydet
        filename = output_dir + time.strftime("%Y%m%d-%H%M%S") + ".jpg"
        cv2.imwrite(filename, frame)
        print(f"Görüntü kaydedildi: {filename}")
        frame_num += 1

    # Çıkış için 'q' tuşuna basıldığında döngüyü sonlandır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı kapat ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()