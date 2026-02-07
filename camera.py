import cv2
import time

# ========== OPENCV CONFIG ============
FACE_CASCADE_PATH = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

if face_cascade.empty():
    raise RuntimeError("Haar cascade not loaded. Install opencv-data.")

# ========== PARAMETERS ===============
CAMERA_INDEX = 0          # try 1 if 0 not working
MOTION_THRESHOLD = 5000  # lower = more sensitive
ALERT_COOLDOWN = 15      # seconds between alerts

# ====================================

class MotionCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        if not self.cap.isOpened():
            raise RuntimeError("? Webcam not accessible")

        print("? Setting up webcam...")
        time.sleep(3)

        # Capture initial background
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("? Failed to capture background frame")

        self.background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.background = cv2.GaussianBlur(self.background, (21, 21), 0)

        self.last_alert_time = 0
        print("?? Motion detection ready")

    def check_motion(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        diff = cv2.absdiff(self.background, gray)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        motion_pixels = cv2.countNonZero(thresh)

        # Slowly update background (adapts to light)
        self.background = cv2.addWeighted(self.background, 0.95, gray, 0.05, 0)

        # Check cooldown
        current_time = time.time()
        if motion_pixels > MOTION_THRESHOLD:
            if current_time - self.last_alert_time > ALERT_COOLDOWN:
                self.last_alert_time = current_time

                # Face detection
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                # Draw face boxes
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Timestamp
                cv2.putText(
                    frame,
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2
                )

                return frame, len(faces)

        return None, None
