from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2

# Argüman ayrıştırıcı oluştur
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=int, default=-1,
                help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# Video başlat
vs = VideoStream(usePiCamera=args["image"] > 0).start()
time.sleep(2.0)

# Video akışındaki kareleri döngü ile al
while True:
    # Thread tabanlı video akışından kareyi al ve maksimum genişliği 400 piksele boyutlandır
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    
    # Zaman damgası
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)
    
    # Kareyi göster
    cv2.imshow("frame", frame)
    
    # Klavyeden tuşu al
    key = cv2.waitKey(1) & 0xFF
    
    # "q" tuşuna basıldığında döngüyü sonlandır
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()



