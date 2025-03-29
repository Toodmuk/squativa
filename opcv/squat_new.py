import cv2
import mediapipe as mp
import numpy as np
import math
import time

class SquatDetector:
    def __init__(self):
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.6,
            min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Squat detection parameters
        self.knee_angle_threshold = 100  # Angle threshold for squat detection
        self.hip_angle_threshold = 110   # Hip angle threshold for posture
        
        # Players data
        self.players = {
            "player1": {
                "squat_count": 0,
                "squat_state": False,
                "score": 0,
                "last_squat_time": time.time(),
                "correct_form": True,
                "position": "left"
            },
            "player2": {
                "squat_count": 0,
                "squat_state": False, 
                "score": 0,
                "last_squat_time": time.time(),
                "correct_form": True,
                "position": "right"
            }
        }

    def calculate_angle(self, a, b, c):
        """
        Calculate the angle between three points
        Args:
            a, b, c: Points in [x, y] format
        Returns:
            Angle in degrees
        """
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle

    def detect_players(self, results):
        """
        Separates the detected poses into player1 and player2 based on position
        """
        if not results.pose_landmarks:
            return {"player1": None, "player2": None}
            
        # MediaPipe only returns one set of landmarks per person it detects
        # We'll determine if this person is on the left or right side
        landmarks = results.pose_landmarks
        
        # Get center x coordinate of the person
        nose_x = landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].x
        
        # Determine if the person is on the left or right half of the frame
        if nose_x < 0.5:  # Left side
            return {"player1": landmarks, "player2": None}
        else:  # Right side
            return {"player1": None, "player2": landmarks}

    def evaluate_squat(self, landmarks, player_key):
        """
        Evaluate squat form and count for a specific player
        """
        if landmarks is None:
            return None
            
        # Get relevant landmarks
        hip = [landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP].x,
               landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP].y]
        knee = [landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_KNEE].x,
                landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_KNEE].y]
        ankle = [landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE].x,
                 landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE].y]
        shoulder = [landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                    landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y]
        
        # Calculate angles
        knee_angle = self.calculate_angle(hip, knee, ankle)
        hip_angle = self.calculate_angle(shoulder, hip, knee)
        
        # Check form
        correct_form = True
        form_feedback = ""
        
        # Check forward lean (using hip angle)
        if hip_angle < self.hip_angle_threshold:
            correct_form = False
            form_feedback = "Leaning too far forward!"
        
        # Detect squat state
        current_squat_state = self.players[player_key]["squat_state"]
        
        # Detect if in squat position (knee angle below threshold)
        if knee_angle < self.knee_angle_threshold and not current_squat_state:
            self.players[player_key]["squat_state"] = True
            self.players[player_key]["correct_form"] = correct_form
            
        # Detect if returning from squat position
        elif knee_angle > self.knee_angle_threshold and current_squat_state:
            self.players[player_key]["squat_state"] = False
            
            # Only count squat if form was correct
            if self.players[player_key]["correct_form"]:
                self.players[player_key]["squat_count"] += 1
                
                # Calculate squat quality (bonus points for deep squats)
                quality_bonus = max(0, (self.knee_angle_threshold - knee_angle) / 10)
                # Award points based on speed and form
                time_since_last = time.time() - self.players[player_key]["last_squat_time"]
                if 1 < time_since_last < 3:  # Optimal squat timing
                    self.players[player_key]["score"] += 10 + quality_bonus
                else:
                    self.players[player_key]["score"] += 5 + quality_bonus
                    
                self.players[player_key]["last_squat_time"] = time.time()
            else:
                # Small points for trying
                self.players[player_key]["score"] += 2
                
        # Update correct form status (always tracking)
        self.players[player_key]["correct_form"] = correct_form
        
        return {
            "knee_angle": knee_angle,
            "hip_angle": hip_angle,
            "form_feedback": form_feedback,
            "is_squatting": self.players[player_key]["squat_state"],
            "correct_form": correct_form
        }

    def process_frame(self, frame):
        """
        Process a frame to detect and evaluate squats for both players
        """
        # Convert BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the image and get pose landmarks
        results = self.pose.process(image)
        
        # Convert back to BGR for OpenCV
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Draw split screen line
        h, w, _ = image.shape
        cv2.line(image, (w//2, 0), (w//2, h), (255, 255, 255), 2)
        
        # Add player labels
        cv2.putText(image, "Player 1", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(image, "Player 2", (w//2 + 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        if results.pose_landmarks:
            # Separate players based on position
            players_landmarks = self.detect_players(results)
            
            if players_landmarks:
                # Process each player
                for player_key, landmarks in players_landmarks.items():
                    if landmarks:
                        # Draw pose landmarks
                        self.mp_drawing.draw_landmarks(
                            image, landmarks, self.mp_pose.POSE_CONNECTIONS)
                        
                        # Evaluate squat for this player
                        evaluation = self.evaluate_squat(landmarks, player_key)
                        
                        if evaluation:
                            # Get player's display area (left or right half)
                            x_offset = 0 if player_key == "player1" else w//2
                            
                            # Display squat count
                            count_text = f"Squats: {self.players[player_key]['squat_count']}"
                            cv2.putText(image, count_text, (x_offset + 20, 100), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            
                            # Display score
                            score_text = f"Score: {int(self.players[player_key]['score'])}"
                            cv2.putText(image, score_text, (x_offset + 20, 150), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            
                            # Display feedback if form is incorrect
                            if not evaluation["correct_form"] and evaluation["form_feedback"]:
                                cv2.putText(image, evaluation["form_feedback"], 
                                          (x_offset + 20, 200), cv2.FONT_HERSHEY_SIMPLEX, 
                                          1, (0, 0, 255), 2)
                            
                            # Visualize squat state
                            if evaluation["is_squatting"]:
                                squat_color = (0, 255, 0) if evaluation["correct_form"] else (0, 0, 255)
                                squat_text = "SQUATTING"
                                cv2.putText(image, squat_text, 
                                           (x_offset + 20, 250), cv2.FONT_HERSHEY_SIMPLEX, 
                                           1, squat_color, 2)
        
        return image

def main():
    cap = cv2.VideoCapture(0)  # Use default webcam
    detector = SquatDetector()
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to read from webcam")
            break
            
        # Process the frame
        processed_frame = detector.process_frame(frame)
        
        # Display the frame
        cv2.imshow('Squat Detection Game', processed_frame)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()