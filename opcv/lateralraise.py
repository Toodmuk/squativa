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

# UX/UI constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Lateral raise thresholds (for horizontal plane)
HORIZONTAL_MIN = 170
HORIZONTAL_MAX = 180
DOWN_MIN = 150  # below this, arm is considered "down"

def lateral_raise_tracker():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)

    counter = 0
    stage = "down"

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

                    # Get left and right arm coordinates
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                    # Calculate angles
                    left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                    right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                    h, w, _ = image.shape

                    # Draw angles
                    left_coords = tuple(np.multiply(left_elbow, [w, h]).astype(int))
                    right_coords = tuple(np.multiply(right_elbow, [w, h]).astype(int))
                    left_color = (0, 255, 0) if HORIZONTAL_MIN <= left_angle <= HORIZONTAL_MAX else (0, 0, 255)
                    right_color = (0, 255, 0) if HORIZONTAL_MIN <= right_angle <= HORIZONTAL_MAX else (0, 0, 255)
                    cv2.putText(image, str(int(left_angle)), left_coords, cv2.FONT_HERSHEY_SIMPLEX, 1, left_color, 2, cv2.LINE_AA)
                    cv2.putText(image, str(int(right_angle)), right_coords, cv2.FONT_HERSHEY_SIMPLEX, 1, right_color, 2, cv2.LINE_AA)

                    # Improved rep counting: Only count when both arms go from "down" to "horizontal" and then back "down"
                    if stage == "down":
                        if HORIZONTAL_MIN <= left_angle <= HORIZONTAL_MAX and HORIZONTAL_MIN <= right_angle <= HORIZONTAL_MAX:
                            stage = "up"
                    elif stage == "up":
                        if left_angle < DOWN_MIN and right_angle < DOWN_MIN:
                            stage = "down"
                            counter += 1

                    # Draw arm paths
                    left_shoulder_point = tuple(np.multiply(left_shoulder, [w, h]).astype(int))
                    left_elbow_point = tuple(np.multiply(left_elbow, [w, h]).astype(int))
                    left_wrist_point = tuple(np.multiply(left_wrist, [w, h]).astype(int))
                    right_shoulder_point = tuple(np.multiply(right_shoulder, [w, h]).astype(int))
                    right_elbow_point = tuple(np.multiply(right_elbow, [w, h]).astype(int))
                    right_wrist_point = tuple(np.multiply(right_wrist, [w, h]).astype(int))

                    cv2.line(image, left_shoulder_point, left_elbow_point, left_color, 4)
                    cv2.line(image, left_elbow_point, left_wrist_point, left_color, 4)
                    cv2.line(image, right_shoulder_point, right_elbow_point, right_color, 4)
                    cv2.line(image, right_elbow_point, right_wrist_point, right_color, 4)

                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                else:
                    cv2.putText(image, "No person detected", (int(SCREEN_WIDTH/2)-250, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4, cv2.LINE_AA)
            except Exception as e:
                print("Tracking error:", e)

            # --- Rep Counter UI (same as before) ---
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

            cv2.imshow('Lateral Raise Tracker', image)
            cv2.namedWindow('Lateral Raise Tracker', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Lateral Raise Tracker', SCREEN_WIDTH, SCREEN_HEIGHT)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    lateral_raise_tracker()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    lateral_raise_tracker()
