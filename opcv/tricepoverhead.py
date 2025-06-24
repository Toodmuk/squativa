import cv2
import mediapipe as mp
import numpy as np
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Thresholds for triceps overhead extension
UPPER_THRESHOLD = 60    # Arm flexed (dumbbell down)
LOWER_THRESHOLD = 170   # Arm extended (dumbbell up)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

def triceps_overhead_tracker():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)

    counter = 0
    stage = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                if results.pose_landmarks is not None:
                    landmarks = results.pose_landmarks.landmark

                    # Use right arm for demonstration (can be adapted for left)
                    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                    # Get face center (average of nose and eyes)
                    nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                            landmarks[mp_pose.PoseLandmark.NOSE.value].y]
                    left_eye = [landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y]
                    right_eye = [landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y]
                    face_center = [
                        (nose[0] + left_eye[0] + right_eye[0]) / 3,
                        (nose[1] + left_eye[1] + right_eye[1]) / 3
                    ]

                    angle = calculate_angle(shoulder, elbow, wrist)
                    h, w, _ = image.shape
                    coords = tuple(np.multiply(elbow, [w, h]).astype(int))
                    color = (0, 255, 0) if UPPER_THRESHOLD < angle < LOWER_THRESHOLD else (0, 0, 255)
                    cv2.putText(image, str(int(angle)), coords, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

                    # Draw a circle at the face center for visualization
                    face_center_px = tuple(np.multiply(face_center, [w, h]).astype(int))
                    cv2.circle(image, face_center_px, 15, (255, 0, 255), -1)

                    # Rep counting logic: elbow must be above face center (y is less)
                    if elbow[1] < face_center[1]:
                        if angle > LOWER_THRESHOLD:
                            stage = "up"
                        if angle < UPPER_THRESHOLD and stage == "up":
                            stage = "down"
                            counter += 1

                    # Draw arm path
                    shoulder_point = tuple(np.multiply(shoulder, [w, h]).astype(int))
                    elbow_point = tuple(np.multiply(elbow, [w, h]).astype(int))
                    wrist_point = tuple(np.multiply(wrist, [w, h]).astype(int))
                    cv2.line(image, shoulder_point, elbow_point, color, 4)
                    cv2.line(image, elbow_point, wrist_point, color, 4)

                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                else:
                    cv2.putText(image, "No person detected", (int(SCREEN_WIDTH/2)-250, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4, cv2.LINE_AA)
            except Exception as e:
                print("Tracking error:", e)

            # --- Rep Counter UI ---
            overlay = image.copy()
            rep_box_width, rep_box_height = 400, 180
            rep_box_x = int((SCREEN_WIDTH - rep_box_width) / 2)
            rep_box_y = 40
            cv2.rectangle(overlay, (rep_box_x, rep_box_y), (rep_box_x + rep_box_width, rep_box_y + rep_box_height), (0, 0, 0), -1)
            alpha = 0.5
            image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
            cv2.putText(image, 'REPS', (rep_box_x + 30, rep_box_y + 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 255), 5, cv2.LINE_AA)
            cv2.putText(image, str(counter), (rep_box_x + 180, rep_box_y + 150),
                        cv2.FONT_HERSHEY_DUPLEX, 4.5, (0, 255, 255), 10, cv2.LINE_AA)
            cv2.putText(image, str(counter), (rep_box_x + 180, rep_box_y + 150),
                        cv2.FONT_HERSHEY_DUPLEX, 4.5, (50, 50, 255), 3, cv2.LINE_AA)

            cv2.imshow('Triceps Overhead Tracker', image)
            cv2.namedWindow('Triceps Overhead Tracker', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Triceps Overhead Tracker', SCREEN_WIDTH, SCREEN_HEIGHT)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    triceps_overhead_tracker()
