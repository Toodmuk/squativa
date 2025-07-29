import cv2
import mediapipe as mp
import numpy as np
import math

# Set up MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # Shoulder
    b = np.array(b)  # Elbow
    c = np.array(c)  # Wrist

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Thresholds for good form
UPPER_THRESHOLD = 40     # Good contraction angle
LOWER_THRESHOLD = 160    # Arm fully extended

# Set desired screen resolution
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

cap = cv2.VideoCapture(1)

# Set the capture resolution if supported by the camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)

# Rep counting variables
stage = None
counter = 0

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to fit 1920x1080
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Flip for mirror view and convert to RGB
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make pose detection
        results = pose.process(image)

        # Draw the results back on image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            if results.pose_landmarks is not None:
                landmarks = results.pose_landmarks.landmark

                # Get left arm coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                # Get right arm coordinates
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Get angles
                left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Get image dimensions
                h, w, _ = image.shape

                # Draw angle visuals for both elbows
                left_coords = tuple(np.multiply(left_elbow, [w, h]).astype(int))
                right_coords = tuple(np.multiply(right_elbow, [w, h]).astype(int))
                left_color = (0, 255, 0) if UPPER_THRESHOLD < left_angle < LOWER_THRESHOLD else (0, 0, 255)
                right_color = (0, 255, 0) if UPPER_THRESHOLD < right_angle < LOWER_THRESHOLD else (0, 0, 255)
                cv2.putText(image, str(int(left_angle)),
                            left_coords,
                            cv2.FONT_HERSHEY_SIMPLEX, 1, left_color, 2, cv2.LINE_AA)
                cv2.putText(image, str(int(right_angle)),
                            right_coords,
                            cv2.FONT_HERSHEY_SIMPLEX, 1, right_color, 2, cv2.LINE_AA)

                # Rep counting logic (either arm)
                # Use separate stages for each arm to avoid double counting
                global left_stage, right_stage
                if 'left_stage' not in globals():
                    left_stage = None
                if 'right_stage' not in globals():
                    right_stage = None

                # Left arm logic
                if left_angle > LOWER_THRESHOLD:
                    left_stage = "down"
                if left_angle < UPPER_THRESHOLD and left_stage == "down":
                    left_stage = "up"
                    counter += 1

                # Right arm logic
                if right_angle > LOWER_THRESHOLD:
                    right_stage = "down"
                if right_angle < UPPER_THRESHOLD and right_stage == "down":
                    right_stage = "up"
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

                # Render pose landmarks
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            else:
                # Optionally, display a message if no person is detected
                cv2.putText(image, "No person detected", (int(SCREEN_WIDTH/2)-250, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4, cv2.LINE_AA)
        except Exception as e:
            print("Tracking error:", e)

        # --- Improved Rep Counter UI ---
        # Draw a semi-transparent rectangle at the center-top
        overlay = image.copy()
        rep_box_width, rep_box_height = 400, 180
        rep_box_x = int((SCREEN_WIDTH - rep_box_width) / 2)
        rep_box_y = 40
        cv2.rectangle(overlay, (rep_box_x, rep_box_y), (rep_box_x + rep_box_width, rep_box_y + rep_box_height), (0, 0, 0), -1)
        alpha = 0.5  # Transparency factor
        image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

        # Draw "REPS" label
        cv2.putText(image, 'REPS', (rep_box_x + 30, rep_box_y + 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 255), 5, cv2.LINE_AA)
        # Draw rep count (large and bold)
        cv2.putText(image, str(counter), (rep_box_x + 180, rep_box_y + 150),
                    cv2.FONT_HERSHEY_DUPLEX, 4.5, (0, 255, 255), 10, cv2.LINE_AA)
        cv2.putText(image, str(counter), (rep_box_x + 180, rep_box_y + 150),
                    cv2.FONT_HERSHEY_DUPLEX, 4.5, (50, 50, 255), 3, cv2.LINE_AA)

        cv2.imshow('Bicep Curl Tracker', image)

        # Set OpenCV window size to 1920x1080
        cv2.namedWindow('Bicep Curl Tracker', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Bicep Curl Tracker', SCREEN_WIDTH, SCREEN_HEIGHT)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
