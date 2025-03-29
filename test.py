import pygame
import sys
import numpy as np
import os
from pygame.locals import *

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
        
        # Load custom fonts - modify these paths to match your font file location
        self.load_fonts()
        
        # Game states
        self.state = "MENU"  # MENU, SONG_SELECT, DIFFICULTY_SELECT, GAME
        
        # Music library - organize the songs with difficulties
        self.music_library = self.load_music_library()
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
    
    def load_fonts(self):
        """Load custom TTF fonts for the game"""
        try:
            # Font file paths - update these to your actual font paths
            font_path = "fonts/ARCADECLASSIC.ttf"  
            
            # Check if the font file exists
            if not os.path.exists(font_path):
                print(f"Warning: Font file not found at {font_path}")
                print("Using system fonts as fallback")
                # Fallback to system fonts if custom font not found
                self.font_large = pygame.font.SysFont("Arial", 72, bold=True)
                self.font_medium = pygame.font.SysFont("Arial", 48)
                self.font_small = pygame.font.SysFont("Arial", 32)
            else:
                # Create font objects with custom font in different sizes
                self.font_large = pygame.font.Font(font_path, 72)
                self.font_medium = pygame.font.Font(font_path, 48)
                self.font_small = pygame.font.Font(font_path, 32)
                print("Custom font loaded successfully!")
        except Exception as e:
            print(f"Error loading fonts: {e}")
            # Fallback to system fonts if there's an error
            self.font_large = pygame.font.SysFont("Arial", 72, bold=True)
            self.font_medium = pygame.font.SysFont("Arial", 48)
            self.font_small = pygame.font.SysFont("Arial", 32)
    
    def load_music_library(self):
        # In a real implementation, you'd scan directories or load from a config file
        # This is a placeholder structure for demonstration
        music_library = [
            {
                "title": "Swear",
                "file": "songs/song1.mp3",
                "difficulties": [
                    {"name": "Easy", "interval": 4000, "speed": 200},
                    {"name": "Medium", "interval": 3000, "speed": 300},
                    {"name": "Hard", "interval": 2000, "speed": 400}
                ]
            },
            {
                "title": "Mongkon",
                "file": "songs/song2.mp3",
                "difficulties": [
                    {"name": "Easy", "interval": 3500, "speed": 250},
                    {"name": "Medium", "interval": 2500, "speed": 350},
                    {"name": "Hard", "interval": 1800, "speed": 450}
                ]
            },
            {
                "title": "Love Song",
                "file": "songs/song3.mp3",
                "difficulties": [
                    {"name": "Easy", "interval": 5000, "speed": 150},
                    {"name": "Medium", "interval": 3800, "speed": 250},
                    {"name": "Hard", "interval": 2800, "speed": 350}
                ]
            }
        ]
        return music_library
    
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
    
    def draw_menu(self):
        # Draw background
        self.screen.fill(self.BLACK)
        
        # Draw title
        title_text = self.font_large.render("Fitness Dance Game", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//4))
        self.screen.blit(title_text, title_rect)
        
        # Draw start button
        button_width, button_height = 300, 80
        button_x = (self.WIDTH - button_width) // 2
        button_y = self.HEIGHT // 2
        
        pygame.draw.rect(self.screen, self.BLUE, (button_x, button_y, button_width, button_height), border_radius=15)
        pygame.draw.rect(self.screen, self.WHITE, (button_x, button_y, button_width, button_height), 3, border_radius=15)
        
        start_text = self.font_medium.render("START", True, self.WHITE)
        start_rect = start_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 + button_height//2))
        self.screen.blit(start_text, start_rect)
        
        # Draw instructions
        instructions_text = self.font_small.render("Click START to select a song", True, self.WHITE)
        instructions_rect = instructions_text.get_rect(center=(self.WIDTH//2, self.HEIGHT*3//4))
        self.screen.blit(instructions_text, instructions_rect)
        
        # Check for button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if (button_x <= mouse_pos[0] <= button_x + button_width and
            button_y <= mouse_pos[1] <= button_y + button_height and mouse_clicked):
            self.state = "SONG_SELECT"
    
    def draw_song_select(self):
        # Draw background
        self.screen.fill((30, 30, 50))
        
        # Draw title
        title_text = self.font_large.render("Select a Song", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//8))
        self.screen.blit(title_text, title_rect)
        
        # Draw song buttons
        button_width, button_height = 500, 80
        button_spacing = 30
        start_y = self.HEIGHT//4
        
        for i, song in enumerate(self.music_library):
            button_x = (self.WIDTH - button_width) // 2
            button_y = start_y + i * (button_height + button_spacing)
            
            # Button color
            button_color = self.BLUE
            
            pygame.draw.rect(self.screen, button_color, 
                            (button_x, button_y, button_width, button_height), 
                            border_radius=15)
            pygame.draw.rect(self.screen, self.WHITE, 
                            (button_x, button_y, button_width, button_height), 
                            3, border_radius=15)
            
            song_text = self.font_medium.render(song["title"], True, self.WHITE)
            song_rect = song_text.get_rect(center=(self.WIDTH//2, button_y + button_height//2))
            self.screen.blit(song_text, song_rect)
            
            # Check for button click
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            if (button_x <= mouse_pos[0] <= button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + button_height and mouse_clicked):
                self.selected_song = song
                self.state = "DIFFICULTY_SELECT"
        
        # Back button
        back_width, back_height = 200, 60
        back_x = 50
        back_y = self.HEIGHT - back_height - 50
        
        pygame.draw.rect(self.screen, self.RED, (back_x, back_y, back_width, back_height), border_radius=15)
        pygame.draw.rect(self.screen, self.WHITE, (back_x, back_y, back_width, back_height), 3, border_radius=15)
        
        back_text = self.font_small.render("Back", True, self.WHITE)
        back_rect = back_text.get_rect(center=(back_x + back_width//2, back_y + back_height//2))
        self.screen.blit(back_text, back_rect)
        
        # Check for back button click
        if (back_x <= mouse_pos[0] <= back_x + back_width and
            back_y <= mouse_pos[1] <= back_y + back_height and mouse_clicked):
            self.state = "MENU"
    
    def draw_difficulty_select(self):
        # Draw background
        self.screen.fill((30, 30, 50))
        
        # Draw title
        title_text = self.font_large.render(f"Select Difficulty: {self.selected_song['title']}", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//8))
        self.screen.blit(title_text, title_rect)
        
        # Draw difficulty buttons
        button_width, button_height = 400, 80
        button_spacing = 30
        start_y = self.HEIGHT//3
        
        for i, difficulty in enumerate(self.selected_song["difficulties"]):
            button_x = (self.WIDTH - button_width) // 2
            button_y = start_y + i * (button_height + button_spacing)
            
            # Button color based on difficulty
            if difficulty["name"] == "Easy":
                button_color = self.GREEN
            elif difficulty["name"] == "Medium":
                button_color = self.YELLOW
            else:  # Hard
                button_color = self.RED
            
            pygame.draw.rect(self.screen, button_color, 
                            (button_x, button_y, button_width, button_height), 
                            border_radius=15)
            pygame.draw.rect(self.screen, self.WHITE, 
                            (button_x, button_y, button_width, button_height), 
                            3, border_radius=15)
            
            diff_text = self.font_medium.render(difficulty["name"], True, self.WHITE)
            diff_rect = diff_text.get_rect(center=(self.WIDTH//2, button_y + button_height//2))
            self.screen.blit(diff_text, diff_rect)
            
            # Check for button click
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            if (button_x <= mouse_pos[0] <= button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + button_height and mouse_clicked):
                self.selected_difficulty = difficulty
                self.start_game()
        
        # Back button
        back_width, back_height = 200, 60
        back_x = 50
        back_y = self.HEIGHT - back_height - 50
        
        pygame.draw.rect(self.screen, self.RED, (back_x, back_y, back_width, back_height), border_radius=15)
        pygame.draw.rect(self.screen, self.WHITE, (back_x, back_y, back_width, back_height), 3, border_radius=15)
        
        back_text = self.font_small.render("Back", True, self.WHITE)
        back_rect = back_text.get_rect(center=(back_x + back_width//2, back_y + back_height//2))
        self.screen.blit(back_text, back_rect)
        
        # Check for back button click
        if (back_x <= mouse_pos[0] <= back_x + back_width and
            back_y <= mouse_pos[1] <= back_y + back_height and mouse_clicked):
            self.state = "SONG_SELECT"
    
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
    
    def draw_target_zone(self):
        # Draw the target zone where squat graphics should align
        pygame.draw.circle(self.screen, (50, 50, 50), self.target_position, self.target_zone_radius, 2)
        pygame.draw.circle(self.screen, (80, 80, 80), self.target_position, self.target_zone_radius - 5, 1)
    
    def draw_squat_graphic(self, graphic):
        # Draw the squat graphic (currently just a square, you'll replace with your own graphic)
        surface = pygame.Surface((graphic["width"], graphic["height"]), pygame.SRCALPHA)
        
        # If the graphic is at the target zone, make it shine
        if graphic["shine"] > 0:
            # Create a glow/shine effect - Fix the integer conversion error
            glow_radius = int(graphic["width"] // 2 + graphic["shine"] * 5)  # Convert to integer
            pygame.draw.rect(
                surface, 
                (255, 255, 100, int(100 - graphic["shine"] * 10)),  # Convert to integer
                (graphic["width"]//2 - glow_radius, graphic["height"]//2 - glow_radius, 
                 glow_radius * 2, glow_radius * 2),
                border_radius=glow_radius
            )
        
        # Draw the actual graphic with current opacity
        pygame.draw.rect(
            surface, 
            (255, 255, 255, int(graphic["opacity"])),  # Convert to integer
            (0, 0, graphic["width"], graphic["height"]),
            border_radius=15
        )
        
        pygame.draw.rect(
            surface, 
            (0, 150, 255, int(graphic["opacity"])),  # Convert to integer 
            (0, 0, graphic["width"], graphic["height"]), 
            3, 
            border_radius=15
        )
        
        # Draw a simple squat icon inside the square (placeholder)
        if graphic["opacity"] > 50:
            # Stick figure for squat
            pygame.draw.circle(
                surface, 
                (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
                (graphic["width"]//2, graphic["height"]//4), 
                10
            )
            pygame.draw.line(
                surface, 
                (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
                (graphic["width"]//2, graphic["height"]//4), 
                (graphic["width"]//2, graphic["height"]//2), 
                5
            )
            pygame.draw.line(
                surface, 
                (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
                (graphic["width"]//2, graphic["height"]//2), 
                (graphic["width"]//3, graphic["height"]*3//4), 
                5
            )
            pygame.draw.line(
                surface, 
                (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
                (graphic["width"]//2, graphic["height"]//2), 
                (graphic["width"]*2//3, graphic["height"]*3//4), 
                5
            )
            pygame.draw.line(
                surface, 
                (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
                (graphic["width"]//2, graphic["height"]//2), 
                (graphic["width"]//3, graphic["height"]*2//5), 
                5
            )
            pygame.draw.line(
                surface, 
                (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
                (graphic["width"]//2, graphic["height"]//2), 
                (graphic["width"]*2//3, graphic["height"]*2//5), 
                5
            )
        
        # Position and draw the graphic
        self.screen.blit(surface, (graphic["x"] - graphic["width"]//2, graphic["y"] - graphic["height"]//2))
    
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
    
    def draw_camera_feed(self):
        # Draw a placeholder for camera
        pygame.draw.rect(self.screen, (40, 40, 40), (self.WIDTH//2, 0, self.WIDTH//2, self.HEIGHT//2))
        text = self.font_small.render("Camera placeholder (OpenCV integration)", True, self.WHITE)
        text_rect = text.get_rect(center=(self.WIDTH*3//4, self.HEIGHT//4))
        self.screen.blit(text, text_rect)
    
    def draw_game_ui(self):
        # Draw score
        score_text = self.font_medium.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (20, 20))
        
        # Draw song and difficulty info
        song_text = self.font_small.render(f"Song: {self.selected_song['title']}", True, self.WHITE)
        self.screen.blit(song_text, (20, 80))
        
        diff_text = self.font_small.render(f"Difficulty: {self.selected_difficulty['name']}", True, self.WHITE)
        self.screen.blit(diff_text, (20, 120))
        
        # Add back to menu button
        menu_btn_width, menu_btn_height = 150, 50
        menu_btn_x = 20
        menu_btn_y = self.HEIGHT - menu_btn_height - 20
        
        pygame.draw.rect(self.screen, self.RED, 
                        (menu_btn_x, menu_btn_y, menu_btn_width, menu_btn_height), 
                        border_radius=10)
        
        menu_text = self.font_small.render("Menu", True, self.WHITE)
        menu_rect = menu_text.get_rect(center=(menu_btn_x + menu_btn_width//2, menu_btn_y + menu_btn_height//2))
        self.screen.blit(menu_text, menu_rect)
        
        # Check for button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if (menu_btn_x <= mouse_pos[0] <= menu_btn_x + menu_btn_width and
            menu_btn_y <= mouse_pos[1] <= menu_btn_y + menu_btn_height and mouse_clicked):
            self.state = "MENU"
            pygame.mixer.music.stop()
    
    def draw_game(self):
        # Clear screen with dark background
        self.screen.fill((20, 20, 30))
        
        # Draw camera feed
        self.draw_camera_feed()
        
        # Draw target zone
        self.draw_target_zone()
        
        # Draw all active squat graphics
        for graphic in self.squat_graphics:
            self.draw_squat_graphic(graphic)
        
        # Draw game UI elements
        self.draw_game_ui()
    
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
                self.draw_menu()
            elif self.state == "SONG_SELECT":
                self.draw_song_select()
            elif self.state == "DIFFICULTY_SELECT":
                self.draw_difficulty_select()
            elif self.state == "GAME":
                self.update_squat_graphics(dt)
                self.draw_game()
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(self.FPS)
        
        # Clean up
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = FitnessDanceGame()
    game.run()