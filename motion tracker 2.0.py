
import serial
import time
import cv2
from ultralytics import YOLO

# --------------------------------------------------
# Load YOLO model
# --------------------------------------------------

model = YOLO("yolov8s.pt")

# --------------------------------------------------
# Camera
# --------------------------------------------------

cap = cv2.VideoCapture(0)

# --------------------------------------------------
# ESP32 Serial
# --------------------------------------------------

ser = serial.Serial("COM3", 115200)
time.sleep(2)

# --------------------------------------------------
# Target variables
# --------------------------------------------------

selected_id = None

# Time when the selected target was last seen
last_seen_time = None

# How long to keep the target locked when temporarily lost
GRACE_PERIOD = 5.0


# --------------------------------------------------
# Mouse click function
# --------------------------------------------------

def select_target(event, x, y, flags, param):

    global selected_id
    global last_seen_time

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    results = param

    if results is None:
        return

    boxes = results[0].boxes

    # No tracking IDs available
    if boxes.id is None:
        return

    ids = boxes.id

    for i, box in enumerate(boxes):

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

        # Check if click is inside this person's bounding box
        if x1 <= x <= x2 and y1 <= y <= y2:

            selected_id = int(ids[i].item())

            last_seen_time = time.time()

            print(f" Locked onto person ID: {selected_id}")

            break


# --------------------------------------------------
# Create window
# --------------------------------------------------

cv2.namedWindow("Person Detection", cv2.WINDOW_NORMAL)

# Current YOLO results
current_results = None

cv2.setMouseCallback(
    "Person Detection",
    select_target,
    current_results
)

print("======================================")
print(" CLICK A PERSON TO LOCK ONTO THEM")
print(" U = Unlock target")
print(" Q = Quit")
print("======================================")


# --------------------------------------------------
# Main loop
# --------------------------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))

    # --------------------------------------------------
    # YOLO tracking
    # --------------------------------------------------

    results = model.track(
        frame,
        classes=[0],
        conf=0.6,
        persist=True
    )

    current_results = results

    # Update mouse callback with latest detections
    cv2.setMouseCallback(
        "Person Detection",
        select_target,
        current_results
    )

    annotated_frame = results[0].plot()

    boxes = results[0].boxes

    count = len(boxes)

    target_found = False

    # --------------------------------------------------
    # Track selected person
    # --------------------------------------------------

    if selected_id is not None and boxes.id is not None:

        ids = boxes.id

        for i, box in enumerate(boxes):

            person_id = int(ids[i].item())

            # Is this our selected person?
            if person_id == selected_id:

                target_found = True

                # Update last-seen time
                last_seen_time = time.time()

                x1, y1, x2, y2 = (
                    box.xyxy[0].cpu().numpy()
                )

                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                # --------------------------------------------------
                # Send selected person's coordinates to ESP32
                # --------------------------------------------------

                ser.write(
                    f"{center_x},{center_y}\n".encode()
                )

                print(
                    f"Target ID {selected_id}: "
                    f"{center_x}, {center_y}"
                )

                # --------------------------------------------------
                # Highlight selected target
                # --------------------------------------------------

                cv2.rectangle(
                    annotated_frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    4
                )

                cv2.putText(
                    annotated_frame,
                    "LOCKED TARGET",
                    (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                break

    # --------------------------------------------------
    # Target temporarily lost
    # --------------------------------------------------

    if selected_id is not None and not target_found:

        if last_seen_time is not None:

            time_missing = time.time() - last_seen_time

            if time_missing < GRACE_PERIOD:

                # Keep target locked
                cv2.putText(
                    annotated_frame,
                    f"TARGET LOST - SEARCHING "
                    f"({GRACE_PERIOD - time_missing:.1f}s)",
                    (20, 75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )

            else:

                # Target has been gone too long
                print(
                    f"Target ID {selected_id} "
                    "lost. Unlocking."
                )

                selected_id = None
                last_seen_time = None

    # --------------------------------------------------
    # Display information
    # --------------------------------------------------

    cv2.putText(
        annotated_frame,
        f"Persons: {count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        2
    )

    # Target status
    if selected_id is not None:

        if target_found:

            cv2.putText(
                annotated_frame,
                f"Target ID: {selected_id}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

    else:

        cv2.putText(
            annotated_frame,
            "Click a person to lock target",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

    # --------------------------------------------------
    # Show frame
    # --------------------------------------------------

    cv2.imshow(
        "Person Detection",
        annotated_frame
    )

    # --------------------------------------------------
    # Keyboard controls
    # --------------------------------------------------

    key = cv2.waitKey(1) & 0xFF

    # Unlock target manually
    if key == ord("u"):

        selected_id = None
        last_seen_time = None

        print(" Target unlocked.")

    # Quit
    elif key == ord("q"):

        break


# --------------------------------------------------
# Cleanup
# --------------------------------------------------

cap.release()
ser.close()
cv2.destroyAllWindows()

