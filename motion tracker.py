import serial
import time
import cv2
from ultralytics import YOLO
# Load YOLO model
model = YOLO("yolov8s.pt")

# Cameraq
cap = cv2.VideoCapture(0)

# ESP32 Serial
ser = serial.Serial("COM3", 115200)
time.sleep(2)

print("Press Q to quit")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))

    # Detect only persons
    results = model.track(frame, classes=[0], conf=0.8, persist=True)

    # Send first person's center to ESP32
    if len(results[0].boxes) > 0:
        box = results[0].boxes[0]

        x1, y1, x2, y2 = box.xyxy[0]

        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        print(center_x, center_y)

        ser.write(f"{center_x},{center_y}\n".encode())

    # Draw detections
    annotated_frame = results[0].plot()

    count = len(results[0].boxes)

    cv2.putText(
        annotated_frame,
        f"Persons: {count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        2
    )

    cv2.namedWindow("Person Detection", cv2.WINDOW_NORMAL)
    cv2.imshow("Person Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()