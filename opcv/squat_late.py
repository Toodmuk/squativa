import cv2
import mediapipe as mp
import numpy as np
import math
import time
import threading

class SquatDetector:
    def __init__(self, rhythm_pattern=None):
        # Initialize MediaPipe Pose with multi-person detection
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1)  # Higher model complexity for better accuracy
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize MediaPipe Holistic
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            min_detection_confidence=0.6,
            min_tracking_confidence=0.5)
        
        # Squat detection parameters
        self.knee_angle_threshold = 70  # Angle threshold for squat detection
        self.hip_angle_threshold = 90   # Hip angle threshold for posture
        
        # Rhythm-based scoring
        self.start_time = time.time()
        self.rhythm_pattern = rhythm_pattern if rhythm_pattern else {
            "squat1": 12.3,
            "squat2": 15.6,
            "squat3": 18.1,
            "squat4": 20.5,
            "squat5": 23.2
        }
        self.next_target_times = {"player1": [], "player2": []}
        self.current_target_idx = {"player1": 0, "player2": 0}
        
        # Players data
        self.players = {
            "player1": {
                "squat_count": 0,
                "squat_state": False,
                "score": 0,
                "last_squat_time": 0,
                "correct_form": True,
                "position": "left",
                "last_detected": 0,
                "rhythm_score": 0,
                "total_rhythm_squats": 0,
                "next_target_time": 0
            },
            "player2": {
                "squat_count": 0,
                "squat_state": False, 
                "score": 0,
                "last_squat_time": 0,
                "correct_form": True,
                "position": "right",
                "last_detected": 0,
                "rhythm_score": 0,
                "total_rhythm_squats": 0,
                "next_target_time": 0
            }
        }
        
        # Update next targets after initializing players
        self.update_next_targets()
        
        # Visual feedback
        self.countdown_active = False
        self.countdown_start = 0
        self.countdown_duration = 3
        
        # Start a separate thread for pose processing to improve performance
        self.frame_queue = []
        self.results_queue = []
        self.threading_active = True
        self.pose_thread = threading.Thread(target=self.process_pose_thread)
        self.pose_thread.daemon = True
        self.pose_thread.start()
    
    def update_next_targets(self):
        """Update the next target times for each player"""
        current_time = time.time() - self.start_time
        
        for player in ["player1", "player2"]:
            rhythm_times = list(self.rhythm_pattern.values())
            
            # Find all future target times
            future_targets = []
            
            # Add multiple cycles of the rhythm pattern
            for cycle in range(5):  # Support 5 cycles of the pattern
                cycle_offset = cycle * (max(rhythm_times) + 2)  # Add 2 seconds between cycles
                for t in rhythm_times:
                    target_time = t + cycle_offset
                    if target_time > current_time:
                        future_targets.append(target_time)
            
            self.next_target_times[player] = sorted(future_targets)
            
            # Set the next target time
            if self.next_target_times[player]:
                self.players[player]["next_target_time"] = self.next_target_times[player][0]
    
    def process_pose_thread(self):
        """Process pose detection in a separate thread"""
        while self.threading_active:
            if self.frame_queue:
                frame = self.frame_queue.pop(0)
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.pose.process(image_rgb)
                self.results_queue.append(results)
            time.sleep(0.01)  # Small sleep to prevent CPU overload
    
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

    def detect_players(self, results, frame_width):
        """
        Detects and assigns landmarks to player1 (left) and player2 (right)
        """
        if not results.pose_landmarks:
            return {"player1": None, "player2": None}
        
        # Process multiple people if detected
        player1_landmarks = None
        player2_landmarks = None
        
        # MediaPipe Pose in this configuration provides a single person's landmarks
        # We'll determine if this person is on the left or right side
        landmarks = results.pose_landmarks
        
        # Use the nose landmark to determine position
        if landmarks and landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].visibility > 0.5:
            nose_x = landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].x
            
            # Check visibility of core landmarks to ensure detection is valid
            key_landmarks = [
                self.mp_pose.PoseLandmark.LEFT_HIP,
                self.mp_pose.PoseLandmark.LEFT_KNEE, 
                self.mp_pose.PoseLandmark.LEFT_ANKLE,
                self.mp_pose.PoseLandmark.LEFT_SHOULDER
            ]
            
            valid_detection = all(landmarks.landmark[lm].visibility > 0.5 for lm in key_landmarks)
            
            # Assign to appropriate player based on position in frame
            if valid_detection:
                midpoint = 0.5  # Center of frame
                
                if nose_x < midpoint:
                    player1_landmarks = landmarks
                    self.players["player1"]["last_detected"] = time.time()
                else:
                    player2_landmarks = landmarks
                    self.players["player2"]["last_detected"] = time.time()
        
        # Return detected players
        return {"player1": player1_landmarks, "player2": player2_landmarks}

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
        current_time = time.time() - self.start_time
        
        # Detect if in squat position (knee angle below threshold)
        if knee_angle < self.knee_angle_threshold and not current_squat_state:
            self.players[player_key]["squat_state"] = True
            self.players[player_key]["correct_form"] = correct_form
            
        # Detect if returning from squat position
        elif knee_angle > self.knee_angle_threshold and current_squat_state:
            # Only count if the person was previously squatting
            if self.players[player_key]["squat_state"]:
                self.players[player_key]["squat_state"] = False
                
                # Count the squat
                self.players[player_key]["squat_count"] += 1
                squat_time = current_time
                self.players[player_key]["last_squat_time"] = squat_time
                
                # Calculate form score (0-100)
                form_score = 100 if correct_form else 50
                
                # Calculate rhythm score if we have target times
                rhythm_score = 0
                if self.next_target_times[player_key]:
                    # Find the closest target time
                    closest_target = min(self.next_target_times[player_key], 
                                        key=lambda x: abs(x - squat_time))
                    
                    # Calculate time difference
                    time_diff = abs(closest_target - squat_time)
                    
                    # Score based on timing accuracy (100 for perfect, 0 for off by 1 second or more)
                    if time_diff < 1.0:
                        rhythm_score = int(100 * (1 - time_diff))
                    
                    # If this was close to a target, remove it from the list
                    if time_diff < 1.0:
                        if closest_target in self.next_target_times[player_key]:
                            self.next_target_times[player_key].remove(closest_target)
                            self.players[player_key]["total_rhythm_squats"] += 1
                            
                            # Update the next target time
                            if self.next_target_times[player_key]:
                                self.players[player_key]["next_target_time"] = self.next_target_times[player_key][0]
                
                # Store the rhythm score for this squat
                self.players[player_key]["rhythm_score"] = rhythm_score
                
                # Add to total score (form score + rhythm score)
                total_squat_score = (form_score + rhythm_score) / 2
                self.players[player_key]["score"] += total_squat_score
            
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
        # Split the frame into left and right halves
        h, w, _ = frame.shape
        midpoint = w // 2
        left_frame = frame[:, :midpoint]
        right_frame = frame[:, midpoint:]

        # Process each half with MediaPipe Holistic
        left_results = self.holistic.process(cv2.cvtColor(left_frame, cv2.COLOR_BGR2RGB))
        right_results = self.holistic.process(cv2.cvtColor(right_frame, cv2.COLOR_BGR2RGB))

        # Create a blank frame for visualization
        large_frame = np.zeros((h, w, 3), dtype=np.uint8)

        # Draw landmarks and evaluate squats for Player 1 (left)
        if left_results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                left_frame,
                left_results.pose_landmarks,
                self.mp_holistic.POSE_CONNECTIONS,
                self.mp_drawing_styles.get_default_pose_landmarks_style())
            evaluation = self.evaluate_squat(left_results.pose_landmarks, "player1")
            self.display_player_info(left_frame, evaluation, "player1")
            self.apply_overlay(left_frame, evaluation)

        # Draw landmarks and evaluate squats for Player 2 (right)
        if right_results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                right_frame,
                right_results.pose_landmarks,
                self.mp_holistic.POSE_CONNECTIONS,
                self.mp_drawing_styles.get_default_pose_landmarks_style())
            evaluation = self.evaluate_squat(right_results.pose_landmarks, "player2")
            self.display_player_info(right_frame, evaluation, "player2")
            self.apply_overlay(right_frame, evaluation)

        # Combine the left and right frames into the large frame
        large_frame[:, :midpoint] = left_frame
        large_frame[:, midpoint:] = right_frame

        # Add player labels
        cv2.putText(large_frame, "Player 1", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(large_frame, "Player 2", (midpoint + 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Draw the split line in the center
        cv2.line(large_frame, (midpoint, 0), (midpoint, h), (255, 255, 255), 2)

        return large_frame

    def apply_overlay(self, frame, evaluation):
        """
        Apply a translucent red or green overlay based on the player's posture correctness.
        """
        if evaluation:
            overlay = frame.copy()
            color = (0, 255, 0) if evaluation["correct_form"] else (0, 0, 255)  # Green for correct, red for incorrect
            alpha = 0.3  # Transparency factor

            # Apply overlay if the player is squatting or has incorrect posture
            if evaluation["is_squatting"] or not evaluation["correct_form"]:
                cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), color, -1)
                cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    def display_player_info(self, frame, evaluation, player_key):
        """Display squat count, score, and feedback for a player"""
        if evaluation:
            # Display squat count
            count_text = f"Squats: {self.players[player_key]['squat_count']}"
            cv2.putText(frame, count_text, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display score
            score_text = f"Score: {int(self.players[player_key]['score'])}"
            cv2.putText(frame, score_text, (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display feedback if form is incorrect
            if not evaluation["correct_form"] and evaluation["form_feedback"]:
                cv2.putText(frame, evaluation["form_feedback"], (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Visualize squat state
            if evaluation["is_squatting"]:
                squat_color = (0, 255, 0) if evaluation["correct_form"] else (0, 0, 255)
                squat_text = "SQUATTING"
                cv2.putText(frame, squat_text, (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, squat_color, 2)

def main():
    # Define a rhythm pattern (in seconds from start)
    rhythm_pattern = {
        "squat1": 12.3,
        "squat2": 15.6,
        "squat3": 18.1,
        "squat4": 20.5,
        "squat5": 23.2
    }
    
    cap = cv2.VideoCapture(0)  # Use default webcam
    detector = SquatDetector(rhythm_pattern)
    
    # Get original frame dimensions
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from webcam")
        return
    
    height, width, _ = frame.shape
    
    # Calculate new dimensions for 4:3 aspect ratio
    new_width = int(height * (4 / 3))
    new_height = height  # Keep the height the same
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to read from webcam")
            break
            
        # Process the frame
        processed_frame = detector.process_frame(frame)
        
        # Resize the frame to 4:3 aspect ratio
        resized_frame = cv2.resize(processed_frame, (new_width*2, new_height*2))
        
        # Display the resized frame
        cv2.imshow('Rhythm Squat Challenge', resized_frame)
        
        # Reset game if 'r' is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            detector = SquatDetector(rhythm_pattern)
            
    # Clean up
    detector.threading_active = False
    if detector.pose_thread.is_alive():
        detector.pose_thread.join(timeout=1.0)
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()