import pygame
import sys
import numpy as np
import os
from pygame.locals import *
from screens import MenuScreen, SongSelectScreen, DifficultySelectScreen, GameScreen
from utils import load_fonts, load_music_library

class FitnessDanceGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Set up display for fullscreen
        self.info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = self.info.current_w, self.info.current_h
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Fitness Dance Game")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.GREEN = (0, 255, 100)
        self.RED = (255, 50, 50)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (180, 0, 255)
        
        # Load custom fonts
        self.fonts = load_fonts()
        
        # Game states
        self.state = "MENU"  # MENU, SONG_SELECT, DIFFICULTY_SELECT, GAME
        
        # Music library - organize the songs with difficulties
        self.music_library = load_music_library()
        self.selected_song = None
        self.selected_difficulty = None
        
        # Squat graphic properties
        self.squat_graphics = []
        self.target_position = (self.WIDTH // 4, self.HEIGHT // 2 + 350)
        self.target_zone_radius = 50
        
        # Timing for squat graphics
        self.last_squat_time = 0
        self.squat_interval = 3000  # milliseconds between squat graphics (will be adjusted based on difficulty)
        
        # Game score
        self.score = 0
        
        # Clock for frame rate
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Initialize screens
        self.menu_screen = MenuScreen(self)
        self.song_select_screen = SongSelectScreen(self)
        self.difficulty_select_screen = DifficultySelectScreen(self)
        self.game_screen = GameScreen(self)
    
    def generate_squat_graphic(self):
        # Create a new squat graphic object that will move from right to left
        graphic = {
            "x": self.WIDTH + 100,  # Start off-screen to the right
            "y": self.HEIGHT // 2 + 350,
            "width": 100,
            "height": 100,
            "speed": self.selected_difficulty["speed"],  # Use difficulty-based speed
            "active": True,
            "opacity": 255,
            "shine": 0,
            "reached_target": False
        }
        self.squat_graphics.append(graphic)
    
    def start_game(self):
        # Change game state
        self.state = "GAME"
        
        # Reset game variables
        self.score = 0
        self.squat_graphics = []
        self.last_squat_time = 0
        self.squat_interval = self.selected_difficulty["interval"]
        
        # Start the music
        try:
            pygame.mixer.music.load(self.selected_song["file"])
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except Exception as e:
            print(f"Could not load music file: {self.selected_song['file']}")
            print(f"Error: {e}")
            # Use placeholder text for development
            print("Using placeholder music for development")
    
    def update_squat_graphics(self, dt):
        # Generate new squat graphics at intervals based on difficulty
        current_time = pygame.time.get_ticks()
        if current_time - self.last_squat_time > self.squat_interval:
            self.generate_squat_graphic()
            self.last_squat_time = current_time
        
        # Update existing squat graphics
        for graphic in self.squat_graphics[:]:
            # Move the graphic from right to left
            graphic["x"] -= graphic["speed"] * dt
            
            # Calculate distance to target zone
            distance_to_target = ((graphic["x"] - self.target_position[0])**2 + 
                                 (graphic["y"] - self.target_position[1])**2)**0.5
            
            # Check if the graphic is at the target position
            if distance_to_target < self.target_zone_radius and not graphic["reached_target"]:
                graphic["reached_target"] = True
                graphic["shine"] = 10  # Start the shine effect
                # This is where you would integrate with OpenCV to check squat position
                
                # For demo without OpenCV, randomly increase score
                if np.random.random() > 0.5:  # 50% chance of success
                    self.score += 100
            
            # Update shine effect
            if graphic["shine"] > 0:
                graphic["shine"] -= 0.5 * dt * 60
            
            # If the graphic has reached the target, start fading it out
            if graphic["reached_target"]:
                graphic["opacity"] -= 300 * dt  # Fade out over time
                
                if graphic["opacity"] <= 0:
                    graphic["active"] = False
            
            # Remove graphics that have moved off-screen or faded out
            if graphic["x"] + graphic["width"] < 0 or not graphic["active"]:
                self.squat_graphics.remove(graphic)
    
    def run(self):
        running = True
        last_time = pygame.time.get_ticks()
        
        while running:
            # Calculate delta time for smooth animations
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0  # Convert to seconds
            last_time = current_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if self.state == "GAME":
                            # Return to menu
                            self.state = "MENU"
                            pygame.mixer.music.stop()
                        else:
                            running = False
                    elif event.key == K_f:  # Toggle fullscreen with F key
                        pygame.display.toggle_fullscreen()
            
            # Update and draw the current state
            if self.state == "MENU":
                self.menu_screen.draw()
            elif self.state == "SONG_SELECT":
                self.song_select_screen.draw()
            elif self.state == "DIFFICULTY_SELECT":
                self.difficulty_select_screen.draw()
            elif self.state == "GAME":
                self.update_squat_graphics(dt)
                self.game_screen.draw()
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(self.FPS)
        
        # Clean up
        pygame.quit()
        sys.exit()