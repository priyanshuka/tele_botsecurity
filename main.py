
import cv2
import time

from camera import MotionCamera
from telegram import send_message, send_photo

def main():
    cam = MotionCamera()

    print("?? Security bot started (motion based)...")

    while True:
        frame, face_count = cam.check_motion()

        # Motion detected and alert allowed
        if frame is not None:
            print("?? Motion detected!")

            alert_text = "?? Motion detected in camera!"
            if face_count and face_count > 0:
                alert_text += f"\n?? Faces detected: {face_count}"

            image_path = "alert.jpg"
            cv2.imwrite(image_path, frame)

            send_message(alert_text)
            send_photo(image_path)

        # Reduce CPU usage
        time.sleep(0.2)

if __name__ == "__main__":
    main()
