import argparse
import cv2
import imutils

# Argüman ayrıştırıcı oluştur
ap = argparse.ArgumentParser()
ap.add_argument("--video", help="path to the video file")
args = vars(ap.parse_args())

# Video yolunu al
video_path = args.get("video")

if video_path:
    # Videoyu yükle
    camera = cv2.VideoCapture(video_path)

    while True:
        (grabbed, frame) = camera.read()
        if not grabbed:
            break

              # Kareyi yeniden boyutlandırın (örneğin 800x600)
        resized_frame = imutils.resize(frame, width=500, height=300)

        # Yeniden boyutlandırılmış kare üzerinde işlemleri yapın
        gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 50, 150)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.01 * peri, True)

            if len(approx) >= 4 and len(approx) <= 6:
                cv2.drawContours(resized_frame, [approx], -1, (0, 0, 255), 4)
                status = "Hedef(ler) Tespit Edildi"

        cv2.putText(resized_frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow("Resized Frame", resized_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
else:
    print("Video path is not provided.")
