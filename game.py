import pygame
import sys
import numpy as np
import os
from pygame.locals import *

class Squativa:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Set up display for windowed mode
        self.WIDTH, self.HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Squativa")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.GREEN = (0, 255, 100)
        self.RED = (255, 50, 50)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (180, 0, 255)
        
        # Direct background loading - REPLACE the existing background loading
        self.background_image = None
        self.scaled_background = None
        
        # Try to load background directly
        bg_path = "graphics/bg.png"
        if os.path.exists(bg_path):
            try:
                print("DIRECT BACKGROUND LOADING: Loading background...")
                self.background_image = pygame.image.load(bg_path).convert()
                
                # Scale it
                scale_factor = max(self.WIDTH / self.background_image.get_width(), 
                                self.HEIGHT / self.background_image.get_height())
                new_width = int(self.background_image.get_width() * scale_factor)
                new_height = int(self.background_image.get_height() * scale_factor)
                scaled_bg = pygame.transform.scale(self.background_image, (new_width, new_height))
                
                # Crop if needed
                crop_x = max(0, (new_width - self.WIDTH) // 2)
                crop_y = max(0, (new_height - self.HEIGHT) // 2)
                self.scaled_background = scaled_bg.subsurface((crop_x, crop_y, self.WIDTH, self.HEIGHT))
                print("DIRECT BACKGROUND LOADING: Background loaded successfully!")
            except Exception as e:
                print(f"DIRECT BACKGROUND LOADING: Error loading background: {e}")
        else:
            print(f"DIRECT BACKGROUND LOADING: Background file not found at: {bg_path}")
        
        # Load fonts
        self.fonts = self.load_fonts()
        
        # Game states
        self.state = "MENU"  # MENU, SELECTION, COUNTDOWN, GAME, RESULTS
        
        # Music library
        self.music_library = self.load_music_library()
        self.selected_song = None
        self.selected_difficulty = None
        self.selected_song_index = 0
        self.selected_difficulty_index = 0
        
        # Squat graphic properties
        self.squat_graphics = []
        self.target_position = (self.WIDTH // 4, self.HEIGHT // 2 + 200)
        self.target_zone_radius = 50
        
        # Load squat image
        self.squat_image = self.load_squat_image()
        
        # Timing for squat graphics
        self.last_squat_time = 0
        self.squat_interval = 3000  # milliseconds between squat graphics
        
        # Game score
        self.score = 0
        
        # Clock for frame rate
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Countdown variables
        self.countdown = 3
        self.countdown_start_time = 0
        self.countdown_started = False
        
        # Game timer
        self.game_duration = 60000  # 1 minute in milliseconds
        self.game_start_time = 0
        
        # Initialize screen objects
        from screens import MenuScreen, CountdownScreen, GameScreen, ResultsScreen
        self.menu_screen = MenuScreen(self)
        self.countdown_screen = CountdownScreen(self)
        self.game_screen = GameScreen(self)
        self.results_screen = ResultsScreen(self)
        
        print("Game initialized successfully")
        
    # Add this method to the FitnessDanceGame class
    def load_background_image(self):
        """Load the custom background image"""
        from utils import load_background_image, scale_background
        
        # Load the background image
        self.background_image = load_background_image()
        
        # Scale it to fit the screen
        if self.background_image:
            self.scaled_background = scale_background(
                self.background_image, self.WIDTH, self.HEIGHT)
            print("Background image loaded and scaled successfully")
        else:
            print("Using fallback background color")
            
    # When you need to update the background scale (for example, when changing resolution)
    def update_background_scale(self):
        """Update the background scale if the screen size changes"""
        from utils import scale_background
        
        if self.background_image:
            self.scaled_background = scale_background(
                self.background_image, self.WIDTH, self.HEIGHT)
    
    
    
    def load_fonts(self):
        fonts = {}
        try:
            # Default to system fonts for reliability
            fonts["large"] = pygame.font.SysFont("Arial", 72, bold=True)
            fonts["medium"] = pygame.font.SysFont("Arial", 48, bold=True)
            fonts["small"] = pygame.font.SysFont("Arial", 32)
            
            # Try to load custom font if available
            font_path = "fonts/ARCADECLASSIC.ttf"
            if os.path.exists(font_path):
                fonts["large"] = pygame.font.Font(font_path, 72)
                fonts["medium"] = pygame.font.Font(font_path, 48)
                fonts["small"] = pygame.font.Font(font_path, 32)
                print("Custom font loaded successfully!")
        except Exception as e:
            print(f"Error loading fonts: {e}")
        
        return fonts
    
    def load_music_library(self):
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
    
    def load_squat_image(self):
        # Define the image path
        image_path = "graphics/Squat.png"
        
        # Check if the file exists
        if os.path.exists(image_path):
            print(f"Found squat image at: {image_path}")
            try:
                # Load the actual image file
                squat_image = pygame.image.load(image_path).convert_alpha()
                print(f"Successfully loaded Squat.png: {squat_image.get_size()}")
                return squat_image
            except Exception as e:
                print(f"Error loading squat image: {e}")
                return None
        else:
            print(f"Squat image not found at: {image_path}")
            return None
    
    def generate_squat_graphic(self):
        # Get speed from selected difficulty or use default
        speed = 300
        if self.selected_difficulty:
            speed = self.selected_difficulty["speed"]
        
        # Skip graphic generation if no squat image is available
        if self.squat_image is None:
            print("Cannot generate squat graphic - no image available")
            return
        
        graphic = {
            "x": self.WIDTH + 100,  # Start off-screen to the right
            "y": self.HEIGHT // 2 + 200,
            "width": 100,
            "height": 100,
            "speed": speed,
            "active": True,
            "opacity": 255,
            "shine": 0,
            "reached_target": False,
            "image": self.squat_image  # Pass the image directly
        }
        self.squat_graphics.append(graphic)
        print(f"Generated new squat graphic, total: {len(self.squat_graphics)}")
    
        # Get speed from selected difficulty or use default
        speed = 300
        if self.selected_difficulty:
            speed = self.selected_difficulty["speed"]
        
        graphic = {
            "x": self.WIDTH + 100,  # Start off-screen to the right
            "y": self.HEIGHT // 2,
            "width": 100,
            "height": 100,
            "speed": speed,
            "active": True,
            "opacity": 255,
            "shine": 0,
            "reached_target": False
        }
        self.squat_graphics.append(graphic)
        print(f"Generated new squat graphic, total: {len(self.squat_graphics)}")
    
    def draw_squat_graphic(self, graphic):
        # Create a temporary surface
        temp_surface = pygame.Surface((graphic["width"], graphic["height"]), pygame.SRCALPHA)
        
        # If the graphic is shining (reached target)
        if graphic["shine"] > 0:
            glow_radius = int(graphic["width"] // 2 + graphic["shine"] * 5)
            pygame.draw.rect(
                temp_surface, 
                (255, 255, 0, int(100 - graphic["shine"] * 10)),
                (0, 0, graphic["width"], graphic["height"]),
                border_radius=glow_radius
            )
        
        # Scale the image
        scaled_image = pygame.transform.scale(self.squat_image, (graphic["width"], graphic["height"]))
        
        # Apply opacity
        if graphic["opacity"] < 255:
            alpha_image = scaled_image.copy()
            alpha_value = max(0, min(255, int(graphic["opacity"])))
            alpha_image.fill((255, 255, 255, alpha_value), None, pygame.BLEND_RGBA_MULT)
            scaled_image = alpha_image
        
        # Draw the image
        temp_surface.blit(scaled_image, (0, 0))
        
        # Draw to the screen
        self.screen.blit(temp_surface, (graphic["x"] - graphic["width"]//2, graphic["y"] - graphic["height"]//2))

    def start_game(self):
        print("===== ATTEMPTING TO START GAME =====")
        print(f"Current state before starting game: {self.state}")
        
        # Debugging song and difficulty selection
        if self.selected_song is None:
            print("WARNING: No song selected, using default")
            self.selected_song = self.music_library[0]
        
        if self.selected_difficulty is None:
            print("WARNING: No difficulty selected, using default")
            self.selected_difficulty = self.selected_song["difficulties"][0]
        
        print(f"Selected Song: {self.selected_song['title'] if self.selected_song else 'None'}")
        print(f"Selected Difficulty: {self.selected_difficulty['name'] if self.selected_difficulty else 'None'}")
        
        # Reset game variables
        self.score = 0
        self.squat_graphics = []
        self.last_squat_time = pygame.time.get_ticks()
        
        # Set up difficulty parameters
        self.squat_interval = self.selected_difficulty["interval"]
        
        # Generate first squat graphic
        print("Generating first squat graphic")
        self.generate_squat_graphic()
        
        # Set game timer
        self.game_start_time = pygame.time.get_ticks()
        
        # Load and play the selected song
        try:
            print(f"Attempting to load music: {self.selected_song['file']}")
            pygame.mixer.music.load(self.selected_song["file"])
            pygame.mixer.music.play()
            print(f"Playing song: {self.selected_song['title']}")
        except Exception as e:
            print(f"Error playing music: {e}")
        
        # Explicitly set the state to GAME
        print("SETTING GAME STATE TO GAME")
        self.state = "GAME"
        
        # Verify state change
        print(f"Game state after setting: {self.state}")
        
        # Optional: Print out any additional debug info
        print("Additional game initialization details:")
        print(f"Squat Interval: {self.squat_interval}")
        print(f"Initial Squat Graphics: {len(self.squat_graphics)}")
        print("===== GAME START COMPLETE =====")
        
        return True  # Indicate successful game start

    def update_squat_graphics(self, dt):
        # Generate new squat graphics
        current_time = pygame.time.get_ticks()
        if current_time - self.last_squat_time > self.squat_interval:
            self.generate_squat_graphic()
            self.last_squat_time = current_time
        
        # Update existing graphics
        for graphic in self.squat_graphics[:]:
            # Move from right to left
            graphic["x"] -= graphic["speed"] * dt
            
            # Calculate distance to target
            distance = ((graphic["x"] - self.target_position[0])**2 + 
                      (graphic["y"] - self.target_position[1])**2)**0.5
            
            # Check if reached target
            if distance < self.target_zone_radius and not graphic["reached_target"]:
                graphic["reached_target"] = True
                graphic["shine"] = 10
                self.score += 100
                print(f"Hit target! Score: {self.score}")
                # Simulate a "hit" - you can add a sound effect here
                try:
                    hit_sound = pygame.mixer.Sound("sounds/hit.wav")
                    hit_sound.play()
                except:
                    print("No hit sound available")
            
            # Update shine effect
            if graphic["shine"] > 0:
                graphic["shine"] -= 0.5 * dt * 60
            
            # Fade out after reaching target
            if graphic["reached_target"]:
                graphic["opacity"] -= 300 * dt
                
                if graphic["opacity"] <= 0:
                    graphic["active"] = False
            
            # Remove if off-screen or inactive
            if graphic["x"] + graphic["width"] < 0 or not graphic["active"]:
                self.squat_graphics.remove(graphic)

    def start_countdown(self):
        print("Starting countdown")
        self.countdown = 3
        self.countdown_start_time = pygame.time.get_ticks()
        self.countdown_started = True
        self.state = "COUNTDOWN"
        
    def draw_unified_selection(self):
        # Draw background
        if self.scaled_background:
            self.screen.blit(self.scaled_background, (0, 0))
        else:
            self.screen.fill((30, 30, 50))
        
        # Draw title
        title_text = self.fonts["large"].render("SELECT SONG AND DIFFICULTY", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//8))
        self.screen.blit(title_text, title_rect)
        
        # Draw song selection section
        song_section_y = self.HEIGHT//4
        song_title = self.fonts["medium"].render("SONG", True, self.WHITE)
        song_title_rect = song_title.get_rect(center=(self.WIDTH//4, song_section_y))
        self.screen.blit(song_title, song_title_rect)
        
        # Draw song options
        song_option_height = 60
        song_spacing = 20
        song_start_y = song_section_y + 60
        
        for i, song in enumerate(self.music_library):
            button_color = self.PURPLE if i == self.selected_song_index else self.BLUE
            button_width = 300
            button_x = (self.WIDTH//4) - (button_width//2)
            button_y = song_start_y + i * (song_option_height + song_spacing)
            
            pygame.draw.rect(self.screen, button_color, 
                            (button_x, button_y, button_width, song_option_height), 
                            border_radius=15)
            pygame.draw.rect(self.screen, self.WHITE, 
                            (button_x, button_y, button_width, song_option_height), 
                            3, border_radius=15)
            
            song_text = self.fonts["medium"].render(song["title"], True, self.WHITE)
            song_rect = song_text.get_rect(center=(self.WIDTH//4, button_y + song_option_height//2))
            self.screen.blit(song_text, song_rect)
            
            # Check for song selection
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            if (button_x <= mouse_pos[0] <= button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + song_option_height and mouse_clicked):
                self.selected_song_index = i
                self.selected_difficulty_index = 0  # Reset difficulty selection when song changes
        
        # Draw difficulty selection section
        difficulty_section_y = self.HEIGHT//4
        difficulty_title = self.fonts["medium"].render("DIFFICULTY", True, self.WHITE)
        difficulty_title_rect = difficulty_title.get_rect(center=(self.WIDTH*3//4, difficulty_section_y))
        self.screen.blit(difficulty_title, difficulty_title_rect)
        
        # Draw difficulty options
        difficulty_option_height = 60
        difficulty_spacing = 20
        difficulty_start_y = difficulty_section_y + 60
        
        selected_song = self.music_library[self.selected_song_index]
        for i, difficulty in enumerate(selected_song["difficulties"]):
            if difficulty["name"] == "Easy":
                button_color = self.RED
            elif difficulty["name"] == "Medium":
                button_color = self.RED
            else:  # Hard
                button_color = self.RED
            
            if i == self.selected_difficulty_index:
                # Add indicator for selected difficulty
                button_color = (min(button_color[0] + 50, 255), 
                                min(button_color[1] + 50, 255), 
                                min(button_color[2] + 50, 255))
            
            button_width = 300
            button_x = (self.WIDTH*3//4) - (button_width//2)
            button_y = difficulty_start_y + i * (difficulty_option_height + difficulty_spacing)
            
            pygame.draw.rect(self.screen, button_color, 
                            (button_x, button_y, button_width, difficulty_option_height), 
                            border_radius=15)
            pygame.draw.rect(self.screen, self.WHITE, 
                            (button_x, button_y, button_width, difficulty_option_height), 
                            3, border_radius=15)
            
            diff_text = self.fonts["medium"].render(difficulty["name"], True, self.WHITE)
            diff_rect = diff_text.get_rect(center=(self.WIDTH*3//4, button_y + difficulty_option_height//2))
            self.screen.blit(diff_text, diff_rect)
            
            # Check for difficulty selection
            if (button_x <= mouse_pos[0] <= button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + difficulty_option_height and mouse_clicked):
                self.selected_difficulty_index = i
        
        # Draw play button
        play_button_width, play_button_height = 300, 80
        play_button_x = (self.WIDTH - play_button_width) // 2
        play_button_y = self.HEIGHT * 3//4
        
        pygame.draw.rect(self.screen, self.GREEN, 
                        (play_button_x, play_button_y, play_button_width, play_button_height), 
                        border_radius=15)
        pygame.draw.rect(self.screen, self.WHITE, 
                        (play_button_x, play_button_y, play_button_width, play_button_height), 
                        3, border_radius=15)
        
        play_text = self.fonts["medium"].render("PLAY", True, self.WHITE)
        play_rect = play_text.get_rect(center=(self.WIDTH//2, play_button_y + play_button_height//2))
        self.screen.blit(play_text, play_rect)
        
        # Check for play button click
        if (play_button_x <= mouse_pos[0] <= play_button_x + play_button_width and
            play_button_y <= mouse_pos[1] <= play_button_y + play_button_height and mouse_clicked):
            self.selected_song = selected_song
            self.selected_difficulty = selected_song["difficulties"][self.selected_difficulty_index]
            self.start_countdown()
        
        # Back button
        back_width, back_height = 200, 60
        back_x = 50
        back_y = self.HEIGHT - back_height - 50
        
        pygame.draw.rect(self.screen, self.RED, (back_x, back_y, back_width, back_height), border_radius=15)
        pygame.draw.rect(self.screen, self.WHITE, (back_x, back_y, back_width, back_height), 3, border_radius=15)
        
        back_text = self.fonts["small"].render("Back", True, self.WHITE)
        back_rect = back_text.get_rect(center=(back_x + back_width//2, back_y + back_height//2))
        self.screen.blit(back_text, back_rect)
        
        # Check for back button click
        if (back_x <= mouse_pos[0] <= back_x + back_width and
            back_y <= mouse_pos[1] <= back_y + back_height and mouse_clicked):
            self.state = "MENU"
            
    def run(self):
        running = True
        last_time = pygame.time.get_ticks()
        
        # Debugging print to track initial state
        print(f"Initial game state: {self.state}")
        
        while running:
            # Calculate delta time
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0  # Convert to seconds
            last_time = current_time
            
            # Debugging: print current state periodically
            if current_time % 5000 < 50:  # Every 5 seconds
                print(f"Current game state: {self.state}")
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if self.state in ["GAME", "COUNTDOWN", "RESULTS", "SELECTION"]:
                            self.state = "MENU"
                        else:
                            running = False
                    elif event.key == K_SPACE and self.state == "GAME":
                        # Debugging: manual squat trigger
                        for graphic in self.squat_graphics:
                            distance = ((graphic["x"] - self.target_position[0])**2 + 
                                    (graphic["y"] - self.target_position[1])**2)**0.5
                            if distance < self.target_zone_radius * 1.5 and not graphic["reached_target"]:
                                graphic["reached_target"] = True
                                graphic["shine"] = 10
                                self.score += 100
                                print(f"Manual squat! Score: {self.score}")
                                break
                    # Debug key to force game state
                    elif event.key == K_g:
                        print("Debug: Forcing game state")
                        if self.selected_song is None:
                            self.selected_song = self.music_library[0]
                        if self.selected_difficulty is None:
                            self.selected_difficulty = self.selected_song["difficulties"][0]
                        self.start_game()
            
            # # Clear the screen
            # self.screen.fill((40, 40, 60))  # Dark blue-gray background
            
            # Update game logic based on current state
            try:
                if self.state == "MENU":
                    self.menu_screen.draw()
                elif self.state == "SELECTION":
                    self.draw_unified_selection()
                elif self.state == "COUNTDOWN":
                    self.countdown_screen.draw()
                elif self.state == "GAME":
                    # Update the squat graphics
                    self.update_squat_graphics(dt)
                    if not self.game_screen.game_started:  # Ensure GameScreen starts
                        self.game_screen.start()
                    self.game_screen.draw()  # Draw the GameScreen
                elif self.state == "RESULTS":
                    self.results_screen.draw()
                else:
                    print(f"Unknown state: {self.state}")
                    self.state = "MENU"
            except Exception as e:
                print(f"Error in game state {self.state}: {e}")
                import traceback
                traceback.print_exc()
                self.state = "MENU"
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(self.FPS)
        
        # Clean up
        if hasattr(self, 'game_screen'):
            self.game_screen.cleanup()
        pygame.quit()
        sys.exit()

# Create and run the game
if __name__ == "__main__":
    game = Squativa()
    game.run()