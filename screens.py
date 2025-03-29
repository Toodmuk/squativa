# At the top of screens.py
import pygame
import cv2
import numpy as np
import sys
import os

# Add opcv folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'opcv'))

try:
    # Import the SquatDetector from your files
    from opcv.squat_late import SquatDetector
    print("Successfully imported SquatDetector")
except ImportError as e:
    print(f"Error importing SquatDetector: {e}")
    # Fallback to simple detector if needed

class MenuScreen:
    def __init__(self, game):
        self.game = game
        # Load and set up the background video
        self.video_frames = []
        self.current_frame = 0
        self.frame_delay = 30  # Milliseconds between frames
        self.last_frame_time = 0
    
    def draw(self):
        # Check if we have a background image
        if self.game.scaled_background is not None:
            # Draw the scaled background image
            self.game.screen.blit(self.game.scaled_background, (0, 0))
        else:
            # Use the existing solid color as fallback
            self.game.screen.fill((30, 30, 50))
        
        # Rest of the code stays the same...
        # Draw title
        title_text = self.game.fonts["large"].render("SQUATIVA", True, self.game.WHITE)
        title_rect = title_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT//4 ))
        self.game.screen.blit(title_text, title_rect)
        
        # Draw start button
        button_width, button_height = 300, 80
        button_x = (self.game.WIDTH - button_width) // 2
        button_y = (self.game.HEIGHT // 2) + 100
        
        pygame.draw.rect(self.game.screen, self.game.BLUE, (button_x, button_y, button_width, button_height), border_radius=15)
        pygame.draw.rect(self.game.screen, self.game.WHITE, (button_x, button_y, button_width, button_height), 3, border_radius=15)
        
        start_text = self.game.fonts["medium"].render("START", True, self.game.WHITE)
        start_rect = start_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT//2 + button_height//2 + 100))
        self.game.screen.blit(start_text, start_rect)
        
        # Draw instructions
        instructions_text = self.game.fonts["small"].render("Rules", True, self.game.RED)
        instructions_rect = instructions_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT*3//4 - 270))
        self.game.screen.blit(instructions_text, instructions_rect)
        
        instructions_text = self.game.fonts["small"].render("Squat in proper form", True, self.game.WHITE)
        instructions_rect = instructions_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT*3//4 - 220))
        self.game.screen.blit(instructions_text, instructions_rect)
        
        instructions_text = self.game.fonts["small"].render("Squat on target zone", True, self.game.WHITE)
        instructions_rect = instructions_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT*3//4 - 170))
        self.game.screen.blit(instructions_text, instructions_rect)
        
        # Check for button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if (button_x <= mouse_pos[0] <= button_x + button_width and
            button_y <= mouse_pos[1] <= button_y + button_height and mouse_clicked):
            self.game.state = "SELECTION"
            # Reset selected song and difficulty when going back to selection
            self.game.selected_song = None
            self.game.selected_difficulty = None

def draw_unified_selection(self):
    # Draw background
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
    
    # Draw difficulty options - UPDATED COLORS
    difficulty_option_height = 60
    difficulty_spacing = 20
    difficulty_start_y = difficulty_section_y + 60
    
    # Base color for all difficulty buttons - orangeish
    difficulty_base_color = (200, 120, 50)  # Orange base for all difficulties
    
    selected_song = self.music_library[self.selected_song_index]
    for i, difficulty in enumerate(selected_song["difficulties"]):
        # Add text label based on difficulty instead of changing button color
        # Consistent base color for all difficulty buttons
        button_color = difficulty_base_color
        
        # If selected, make it significantly brighter and add a glow effect
        if i == self.selected_difficulty_index:
            # Much brighter selected state
            button_color = (255, 170, 70)  # Brighter orange
            
            # Draw a subtle glow behind the button
            glow_surface = pygame.Surface((button_width + 20, difficulty_option_height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 200, 100, 100), 
                           (0, 0, button_width + 20, difficulty_option_height + 20), 
                           border_radius=20)
            
            button_width_with_glow = 300
            button_x_with_glow = (self.WIDTH*3//4) - (button_width_with_glow//2) - 10
            button_y_with_glow = difficulty_start_y + i * (difficulty_option_height + difficulty_spacing) - 10
            
            self.screen.blit(glow_surface, (button_x_with_glow, button_y_with_glow))
        
        button_width = 300
        button_x = (self.WIDTH*3//4) - (button_width//2)
        button_y = difficulty_start_y + i * (difficulty_option_height + difficulty_spacing)
        
        pygame.draw.rect(self.screen, button_color, 
                        (button_x, button_y, button_width, difficulty_option_height), 
                        border_radius=15)
        pygame.draw.rect(self.screen, self.WHITE, 
                        (button_x, button_y, button_width, difficulty_option_height), 
                        3, border_radius=15)
        
        # Add a small label with text indicating difficulty level
        if difficulty["name"] == "Easy":
            label_color = self.RED
            label_text = "EASY"
        elif difficulty["name"] == "Medium":
            label_color = self.RED
            label_text = "MEDIUM"
        else:  # Hard
            label_color = self.RED
            label_text = "HARD"
        
        # Draw difficulty name as main text
        diff_text = self.fonts["medium"].render(label_text, True, self.WHITE)
        diff_rect = diff_text.get_rect(center=(self.WIDTH*3//4, button_y + difficulty_option_height//2))
        self.screen.blit(diff_text, diff_rect)
        
        # Add a small colored indicator square
        indicator_size = 12
        pygame.draw.rect(self.screen, label_color, 
                        (button_x + 20, button_y + difficulty_option_height//2 - indicator_size//2, 
                         indicator_size, indicator_size))
        
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
        print(f"Selected song: {self.selected_song['title']}, difficulty: {self.selected_difficulty['name']}")
        
        # Reset countdown screen - IMPORTANT
        self.countdown_screen.reset()
        self.state = "COUNTDOWN"
    
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

class CountdownScreen:
    def __init__(self, game):
        self.game = game
        self.countdown = 3
        self.start_time = 0
        self.count_duration = 1000  # 1 second per number
        self.started = False
        self.transition_started = False
    
    def start(self):
        print("COUNTDOWN: Starting countdown sequence")
        self.started = True
        self.start_time = pygame.time.get_ticks()
        self.transition_started = False
    
    def reset(self):
        print("COUNTDOWN: Resetting countdown")
        self.started = False
        self.countdown = 3
        self.transition_started = False
 
    def draw(self):
        # Start countdown if not already started
        if not self.started:
            self.start()
        
        # Draw background
        if self.game.scaled_background:
            self.game.screen.blit(self.game.scaled_background, (0, 0))
        else:
            self.game.screen.fill((20, 20, 30))
        
        # Calculate current countdown number
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        
        # Prevent negative countdown
        self.countdown = max(0, 3 - (elapsed // self.count_duration))
        
        # Debug info
        print(f"COUNTDOWN: Current time: {current_time}, Start time: {self.start_time}, Elapsed: {elapsed}")
        print(f"COUNTDOWN: Countdown number: {self.countdown}, Duration: {self.count_duration}")
        
        # Draw the countdown number or GO
        if self.countdown > 0:
            # Draw number with animation
            scale_factor = 1.0 + 0.5 * ((elapsed % self.count_duration) / self.count_duration)
            count_text = self.game.fonts["large"].render(str(self.countdown), True, self.game.WHITE)
            
            # Scale the text
            scaled_size = (int(count_text.get_width() * scale_factor), 
                        int(count_text.get_height() * scale_factor))
            scaled_text = pygame.transform.scale(count_text, scaled_size)
            
            text_rect = scaled_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT//2))
            self.game.screen.blit(scaled_text, text_rect)
        
        # Transition to game
        elif self.countdown == 0 and not self.transition_started:
            # Show "GO!" text
            go_text = self.game.fonts["large"].render("GO!", True, self.game.GREEN)
            text_rect = go_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT//2))
            self.game.screen.blit(go_text, text_rect)
            
            # Mark transition as started to prevent multiple calls
            self.transition_started = True
            
            # Immediate transition to game
            print("COUNTDOWN: TRANSITIONING TO GAME")
            print(f"COUNTDOWN: Current game state before transition: {self.game.state}")
            
            # Explicitly set up game before transitioning
            if self.game.selected_song is None:
                print("COUNTDOWN: No song selected, using default")
                self.game.selected_song = self.game.music_library[0]
            if self.game.selected_difficulty is None:
                print("COUNTDOWN: No difficulty selected, using default")
                self.game.selected_difficulty = self.game.selected_song["difficulties"][0]
            
            # Start the game
            self.game.start_game()
            
            print(f"COUNTDOWN: Game state after transition: {self.game.state}")
  
class GameScreen:
    def __init__(self, game):
        self.game = game
        self.game_duration = 6000  # 1 minute in milliseconds
        self.start_time = 0
        self.game_started = False
        
        # Initialize squat detector and camera
        self.squat_detector = SquatDetector()
        self.camera = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not self.camera.isOpened():
            print("Error: Could not open camera. Using fallback.")

    def start(self):
        """Initialize the game screen and start the timer"""
        print("Starting game screen timer")
        self.game_started = True
        self.start_time = pygame.time.get_ticks()
        
        # Make sure camera is initialized
        if not hasattr(self, 'camera') or not self.camera.isOpened():
            print("Reinitializing camera...")
            try:
                # Release old camera if it exists
                if hasattr(self, 'camera'):
                    self.camera.release()
                
                # Initialize a new camera
                self.camera = cv2.VideoCapture(0)
                if self.camera.isOpened():
                    print("Camera successfully reinitialized")
                else:
                    print("Failed to reinitialize camera - will use fallback display")
            except Exception as e:
                print(f"Error initializing camera: {e}")
        
        # Make sure squat detector is initialized
        if not hasattr(self, 'squat_detector'):
            print("Reinitializing squat detector...")
            try:
                from opcv.squat_late import SquatDetector
                self.squat_detector = SquatDetector()
                print("Squat detector successfully reinitialized")
            except Exception as e:
                print(f"Error initializing squat detector: {e}")

    def draw_camera_feed(self):
        """Draw the camera feed with squat detection overlays"""
        # Ensure background is drawn first
        if self.game.scaled_background:
            self.game.screen.blit(self.game.scaled_background, (0, 0))
        else:
            # Fallback background
            self.game.screen.fill((30, 30, 50))
        
        # Read a frame from the camera
        try:
            # Make sure camera is initialized
            if not hasattr(self, 'camera') or not self.camera.isOpened():
                print("Camera not initialized or opened, attempting to reinitialize...")
                try:
                    if hasattr(self, 'camera'):
                        self.camera.release()
                    self.camera = cv2.VideoCapture(0)
                    print(f"Camera reinitialized: {self.camera.isOpened()}")
                except Exception as e:
                    print(f"Error reinitializing camera: {e}")
            
            # Try to read from camera
            if hasattr(self, 'camera') and self.camera.isOpened():
                ret, frame = self.camera.read()
                if ret:
                    # Flip the frame horizontally for more intuitive interaction
                    frame = cv2.flip(frame, 1)
                    
                    # Make sure squat detector is initialized
                    if not hasattr(self, 'squat_detector'):
                        print("Squat detector not initialized, attempting to reinitialize...")
                        try:
                            from opcv.squat_late import SquatDetector
                            self.squat_detector = SquatDetector()
                            print("Squat detector reinitialized")
                        except Exception as e:
                            print(f"Error reinitializing squat detector: {e}")
                    
                    # Process frame with squat detector if available
                    if hasattr(self, 'squat_detector'):
                        processed_frame = self.squat_detector.process_frame(frame)
                    else:
                        processed_frame = frame  # Fallback to unprocessed frame
                    
                    # Convert to PyGame surface
                    processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                    h, w = processed_frame.shape[:2]
                    
                    # Scale the frame to fit the screen
                    scale_factor = min(self.game.WIDTH / w, self.game.HEIGHT / h)
                    new_w, new_h = int(w * scale_factor), int(h * scale_factor)
                    processed_frame = cv2.resize(processed_frame, (new_w, new_h))
                    
                    # Convert to PyGame surface correctly without rotation
                    try:
                        temp_surface = pygame.Surface((new_w, new_h))
                        pygame.surfarray.blit_array(temp_surface, processed_frame.swapaxes(0, 1))
                        
                        # Position the camera feed in the center
                        x_offset = (self.game.WIDTH - new_w) // 2
                        y_offset = (self.game.HEIGHT - new_h) // 2
                        self.game.screen.blit(temp_surface, (x_offset, y_offset))
                        
                        # Check for squats and update game
                        self.check_for_squats()
                        return True  # Successfully displayed camera feed
                    except Exception as e:
                        print(f"Error creating pygame surface from frame: {e}")
        except Exception as e:
            print(f"Error in camera feed: {e}")
        
        # If we got here, there was a problem with the camera feed
        print("Using fallback display due to camera feed issue")
        return False

    def check_for_squats(self):
        # Check the squat detector for detected squats
        for player_key, player_data in self.squat_detector.players.items():
            if player_data["squat_state"]:
                # Find any graphics near the target zone
                for graphic in self.game.squat_graphics[:]:
                    if not graphic["reached_target"]:
                        # Calculate distance to target
                        distance = abs(graphic["x"] - self.game.target_position[0])
                        
                        # Check if graphic is in target zone
                        in_target_zone = distance < self.game.target_zone_radius
                        
                        # Pass alignment information to SquatDetector
                        self.squat_detector.update_target_alignment(player_key, in_target_zone)
                        
                        if in_target_zone:
                            graphic["reached_target"] = True
                            graphic["shine"] = 10  # Start shine effect
                            
                            # Add points based on form and alignment
                            if player_data["correct_form"]:
                                self.game.score += 100
                            else:
                                self.game.score += 50
                            
                            print(f"Hit target! Score: {self.game.score}")
                            break
    
    def draw_target_zone(self):
        # Draw the target zone where squat graphics should align - BRIGHT COLORS
        pygame.draw.circle(self.game.screen, self.game.YELLOW, self.game.target_position, self.game.target_zone_radius, 4)
        pygame.draw.circle(self.game.screen, (255, 200, 0), self.game.target_position, self.game.target_zone_radius - 10, 2)
        
        # Add text above target
        target_text = self.game.fonts["small"].render("SQUAT HERE", True, self.game.YELLOW)
        target_rect = target_text.get_rect(center=(self.game.target_position[0], self.game.target_position[1] - 70))
        self.game.screen.blit(target_text, target_rect)
    
    def draw_game_ui(self):
        # Start timer if not already started
        if not self.game_started:
            print("Game UI starting timer")
            self.start()
        
        # Calculate remaining time
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        remaining = max(0, self.game_duration - elapsed)
        minutes = remaining // 60000
        seconds = (remaining % 60000) // 1000
        
        # Check if game is over
        if remaining <= 0:
            print("Game timer finished - transitioning to results")
            self.cleanup()  # Clean up camera resources
            self.game.state = "RESULTS"
            return
        

        
        # Get scores from squat detector for both players
        player1_score = int(self.squat_detector.players["player1"]["score"])
        player2_score = int(self.squat_detector.players["player2"]["score"])
        
        # Draw Player 1 score (left side)
        score_bg_p1 = pygame.Surface((180, 40), pygame.SRCALPHA)
        score_bg_p1.fill((0, 100, 0, 180))  # Semi-transparent green
        self.game.screen.blit(score_bg_p1, (10, 200))
        
        score_text_p1 = self.game.fonts["medium"].render("player1", True, self.game.WHITE)
        self.game.screen.blit(score_text_p1, (20, 150))
        score_text_p1 = self.game.fonts["medium"].render(f"{player1_score}", True, self.game.WHITE)
        self.game.screen.blit(score_text_p1, (20, 200))
        
        # Draw Player 2 score (right side)
        score_bg_p2 = pygame.Surface((180, 40), pygame.SRCALPHA)
        score_bg_p2.fill((0, 100, 0, 180))  # Semi-transparent green
        self.game.screen.blit(score_bg_p2, (self.game.WIDTH - 190, 200))
        
        score_text_p2_ds = self.game.fonts["medium"].render("player2", True, self.game.WHITE)
        self.game.screen.blit(score_text_p2_ds, (self.game.WIDTH - 180, 150))
        score_text_p2 = self.game.fonts["medium"].render(f"{player2_score}", True, self.game.WHITE)
        self.game.screen.blit(score_text_p2, (self.game.WIDTH - 180, 200))
        
        # Draw squat state indicator if squatting (for either player)
        for player_key, player_data in self.squat_detector.players.items():
            if player_data["squat_state"]:
                squat_color = self.game.GREEN if player_data["correct_form"] else self.game.RED
                
                # Position based on player
                if player_key == "player1":
                    pos_x = 320
                else:
                    pos_x = self.game.WIDTH - 500
                    
                squat_bg = pygame.Surface((200, 40), pygame.SRCALPHA)
                squat_bg.fill((*squat_color[:3], 180))  # Semi-transparent
                self.game.screen.blit(squat_bg, (pos_x, 600))
                
                squat_text = self.game.fonts["medium"].render("SQUATTING", True, self.game.WHITE)
                self.game.screen.blit(squat_text, (pos_x + 10, 600))
        
        # Add back to menu button
        menu_btn_width, menu_btn_height = 150, 50
        menu_btn_x = 20
        menu_btn_y = self.game.HEIGHT - menu_btn_height - 20
        
        # Semi-transparent button
        menu_btn_bg = pygame.Surface((menu_btn_width, menu_btn_height), pygame.SRCALPHA)
        menu_btn_bg.fill((255, 50, 50, 180))  # Semi-transparent red
        self.game.screen.blit(menu_btn_bg, (menu_btn_x, menu_btn_y))
        
        pygame.draw.rect(self.game.screen, self.game.WHITE, 
                        (menu_btn_x, menu_btn_y, menu_btn_width, menu_btn_height), 
                        2, border_radius=10)
        
        menu_text = self.game.fonts["small"].render("Menu", True, self.game.WHITE)
        menu_rect = menu_text.get_rect(center=(menu_btn_x + menu_btn_width//2, menu_btn_y + menu_btn_height//2))
        self.game.screen.blit(menu_text, menu_rect)
        
        # Check for button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if (menu_btn_x <= mouse_pos[0] <= menu_btn_x + menu_btn_width and
            menu_btn_y <= mouse_pos[1] <= menu_btn_y + menu_btn_height and mouse_clicked):
            print("Menu button clicked - returning to menu")
            self.cleanup()  # Clean up camera resources
            self.game.state = "MENU"
            try:
                pygame.mixer.music.stop()
            except:
                pass

        # Start timer if not already started
        if not self.game_started:
            print("Game UI starting timer")
            self.start()
        
        # Calculate remaining time
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        remaining = max(0, self.game_duration - elapsed)
        minutes = remaining // 60000
        seconds = (remaining % 60000) // 1000
        
        # Check if game is over
        if remaining <= 0:
            print("Game timer finished - transitioning to results")
            self.cleanup()  # Clean up camera resources
            self.game.state = "RESULTS"
            return
        
        # Draw timer with visible background
        timer_bg = pygame.Surface((140, 90))
        timer_bg.fill((0, 0, 100))
        self.game.screen.blit(timer_bg, ((self.game.WIDTH/2)-50, 10))
        
        timer_text = self.game.fonts["large"].render(f"{seconds:02d}", True, self.game.WHITE)
        self.game.screen.blit(timer_text, ((self.game.WIDTH/2)-20, 20))
        
        
    
        
        # Add back to menu button
        menu_btn_width, menu_btn_height = 150, 50
        menu_btn_x = 20
        menu_btn_y = self.game.HEIGHT - menu_btn_height - 20
        
        pygame.draw.rect(self.game.screen, self.game.RED, 
                        (menu_btn_x, menu_btn_y, menu_btn_width, menu_btn_height), 
                        border_radius=10)
        
        menu_text = self.game.fonts["small"].render("Menu", True, self.game.WHITE)
        menu_rect = menu_text.get_rect(center=(menu_btn_x + menu_btn_width//2, menu_btn_y + menu_btn_height//2))
        self.game.screen.blit(menu_text, menu_rect)
        
        # Check for button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if (menu_btn_x <= mouse_pos[0] <= menu_btn_x + menu_btn_width and
            menu_btn_y <= mouse_pos[1] <= menu_btn_y + menu_btn_height and mouse_clicked):
            print("Menu button clicked - returning to menu")
            self.cleanup()  # Clean up camera resources
            self.game.state = "MENU"
            try:
                pygame.mixer.music.stop()
            except:
                pass

    def draw(self):
        """Main draw method for the game screen"""
        print("DRAWING GAME SCREEN")
        
        # Ensure game is started
        if not self.game_started:
            self.start()
        
        # Draw camera feed - if it fails, the method handles the fallback
        camera_success = self.draw_camera_feed()
        
        # If camera feed failed, ensure we at least have the background
        if not camera_success and self.game.scaled_background:
            self.game.screen.blit(self.game.scaled_background, (0, 0))
        elif not camera_success:
            self.game.screen.fill((30, 30, 50))  # Dark background as fallback
        
        # Draw target zone on top of camera feed
        self.draw_target_zone()
        
        # Draw all active squat graphics
        for graphic in self.game.squat_graphics:
            from utils import draw_squat_graphic  # Import here to avoid circular imports
            draw_squat_graphic(self.game.screen, graphic)
        
        # Draw game UI elements on top
        self.draw_game_ui()
   
    def cleanup(self):
        """Release camera resources when leaving the game screen"""
        if hasattr(self, 'camera') and self.camera.isOpened():
            self.camera.release()

class ResultsScreen:
    def __init__(self, game):
        self.game = game
        self.qr_code = None
        self.qr_generated = False
    
    def generate_qr_code(self):
        # Skip QR code generation for testing
        print("Skipping QR code generation for testing")
        self.qr_generated = True

    def reset_game(self):
        """Reset the game state when returning to menu"""
        print("Resetting game state...")
        
        # Stop music if playing
        try:
            pygame.mixer.music.stop()
            print("Music stopped successfully")
        except Exception as e:
            print(f"Error stopping music: {e}")
        
        # Reset scores
        self.game.score = 0
        
        # Reset squat graphics
        self.game.squat_graphics = []
        
        # Reset player data in squat detector if exists
        if hasattr(self.game, 'game_screen') and hasattr(self.game.game_screen, 'squat_detector'):
            for player_key in self.game.game_screen.squat_detector.players:
                player = self.game.game_screen.squat_detector.players[player_key]
                player["squat_count"] = 0
                player["score"] = 0
                player["squat_state"] = False
                player["rhythm_score"] = 0
                player["total_rhythm_squats"] = 0
                print(f"Reset {player_key} data")
        
        # Clean up any resources
        if hasattr(self.game, 'game_screen'):
            self.game.game_screen.cleanup()
            
        # Reset selection state
        self.game.selected_song = None
        self.game.selected_difficulty = None
        
        # Make sure countdown screen is reset
        if hasattr(self.game, 'countdown_screen'):
            self.game.countdown_screen.reset()
            print("Countdown screen reset")
        
        # Reinitialize game_screen with a fresh SquatDetector
        if hasattr(self.game, 'game_screen'):
            try:
                from opcv.squat_late import SquatDetector
                self.game.game_screen.squat_detector = SquatDetector()
                self.game.game_screen.game_started = False
                self.game.game_screen.start_time = 0
                print("Game screen reinitialized")
            except ImportError as e:
                print(f"Error reinitializing SquatDetector: {e}")
        
        print("Game state reset complete")

    def draw(self):
        # Generate QR code if not already done
        if not self.qr_generated:
            self.generate_qr_code()
        
        # Draw background
        if self.game.scaled_background:
            self.game.screen.blit(self.game.scaled_background, (0, 0))
        else:
            self.game.screen.fill((30, 30, 50))
        
        # Get scores from squat detector for both players
        try:
            player1_score = int(self.game.game_screen.squat_detector.players["player1"]["score"])
            player2_score = int(self.game.game_screen.squat_detector.players["player2"]["score"])
        except (AttributeError, KeyError):
            # Fallback if we can't get scores from squat detector
            player1_score = 1000  # Example value
            player2_score = 200   # Example value
        
        # Determine winner
        if player1_score >= player2_score:
            winner = "PLAYER 1"
            winner_score = player1_score
            loser = "PLAYER 2"
            loser_score = player2_score
        else:
            winner = "PLAYER 2"
            winner_score = player2_score
            loser = "PLAYER 1"
            loser_score = player1_score
        
        # Draw WINNER section - top third of screen
        winner_y_start = self.game.HEIGHT // 8
        
        # Draw "WINNER" title
        winner_title = self.game.fonts["large"].render("WINNER", True, self.game.YELLOW)
        winner_title_rect = winner_title.get_rect(center=(self.game.WIDTH//2, winner_y_start))
        self.game.screen.blit(winner_title, winner_title_rect)
        
        # Draw winner name
        winner_name = self.game.fonts["medium"].render(winner, True, self.game.WHITE)
        winner_name_rect = winner_name.get_rect(center=(self.game.WIDTH//2, winner_y_start + 100))
        self.game.screen.blit(winner_name, winner_name_rect)
        
        # Draw winner score with glow effect
        score_bg = pygame.Surface((300, 100), pygame.SRCALPHA)
        score_bg.fill((0, 200, 0, 80))  # Green glow
        score_rect = score_bg.get_rect(center=(self.game.WIDTH//2, winner_y_start + 180))
        self.game.screen.blit(score_bg, score_rect)
        
        winner_score_text = self.game.fonts["large"].render(str(winner_score), True, self.game.GREEN)
        winner_score_rect = winner_score_text.get_rect(center=(self.game.WIDTH//2, winner_y_start + 180))
        self.game.screen.blit(winner_score_text, winner_score_rect)
        
        # Draw LOSER section - bottom third of screen
        loser_y_start = self.game.HEIGHT // 2 + 50
        
        # Draw "LOSER" title
        loser_title = self.game.fonts["medium"].render("LOSER", True, self.game.RED)
        loser_title_rect = loser_title.get_rect(center=(self.game.WIDTH//2, loser_y_start))
        self.game.screen.blit(loser_title, loser_title_rect)
        
        # Draw loser name
        loser_name = self.game.fonts["small"].render(loser, True, self.game.WHITE)
        loser_name_rect = loser_name.get_rect(center=(self.game.WIDTH//2, loser_y_start + 50))
        self.game.screen.blit(loser_name, loser_name_rect)
        
        # Draw loser score
        loser_score_text = self.game.fonts["medium"].render(str(loser_score), True, self.game.WHITE)
        loser_score_rect = loser_score_text.get_rect(center=(self.game.WIDTH//2, loser_y_start + 100))
        self.game.screen.blit(loser_score_text, loser_score_rect)
        
        # Draw menu button
        menu_btn_width, menu_btn_height = 300, 80
        menu_btn_x = (self.game.WIDTH - menu_btn_width) // 2
        menu_btn_y = self.game.HEIGHT * 3//4 + 50
        
        pygame.draw.rect(self.game.screen, self.game.BLUE, 
                        (menu_btn_x, menu_btn_y, menu_btn_width, menu_btn_height), 
                        border_radius=15)
        pygame.draw.rect(self.game.screen, self.game.WHITE, 
                        (menu_btn_x, menu_btn_y, menu_btn_width, menu_btn_height), 
                        3, border_radius=15)
        
        menu_text = self.game.fonts["medium"].render("Back to Menu", True, self.game.WHITE)
        menu_rect = menu_text.get_rect(center=(self.game.WIDTH//2, menu_btn_y + menu_btn_height//2))
        self.game.screen.blit(menu_text, menu_rect)
        
        # Check for button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if (menu_btn_x <= mouse_pos[0] <= menu_btn_x + menu_btn_width and
            menu_btn_y <= mouse_pos[1] <= menu_btn_y + menu_btn_height and mouse_clicked):
            # Stop the music
            try:
                pygame.mixer.music.stop()
                print("Music stopped successfully")
            except Exception as e:
                print(f"Error stopping music: {e}")
            
            # Reset game state
            self.reset_game()
            
            # Return to menu
            self.game.state = "MENU"