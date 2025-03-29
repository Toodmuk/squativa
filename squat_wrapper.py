# Save this as squat_wrapper.py
import cv2
import pygame
import numpy as np
import sys
import os

# Add opcv folder to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), 'opcv'))

# Import the SquatDetector
from squat_new import SquatDetector

class SquatGameDetector:
    def __init__(self, game):
        """
        Wrapper class to connect OpenCV squat detection with Pygame
        """
        self.game = game
        self.detector = SquatDetector()
        self.camera = cv2.VideoCapture(0)
        self.pygame_surface = None
        
        # Check if camera opened successfully
        if not self.camera.isOpened():
            print("Error: Could not open camera. Using fallback.")
    
    def update(self):
        """Update detector and handle squat detection"""
        if not self.camera.isOpened():
            return False
            
        # Read a frame
        ret, frame = self.camera.read()
        if not ret:
            return False
            
        # Process frame and get squat detection
        processed_frame = self.detector.process_frame(frame)
        
        # Convert to PyGame surface
        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        processed_frame = np.rot90(processed_frame)
        self.pygame_surface = pygame.surfarray.make_surface(processed_frame)
        
        # Check for squats
        for player_key, player_data in self.detector.players.items():
            # If a squat was detected
            if player_data["squat_state"]:
                # Check against game targets
                for graphic in self.game.squat_graphics[:]:
                    if not graphic["reached_target"] and abs(graphic["x"] - self.game.target_position[0]) < self.game.target_zone_radius:
                        graphic["reached_target"] = True
                        graphic["shine"] = 10
                        # Add points based on form quality
                        if player_data["correct_form"]:
                            self.game.score += 100
                        else:
                            self.game.score += 50
                        break
        
        return True
        
    def get_surface(self):
        """Return the pygame surface with the processed camera feed"""
        return self.pygame_surface
        
    def cleanup(self):
        """Release resources"""
        if self.camera.isOpened():
            self.camera.release()