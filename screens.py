import pygame
from utils import draw_squat_graphic

class MenuScreen:
    def __init__(self, game):
        self.game = game
    
    def draw(self):
        # Draw background
        self.game.screen.fill(self.game.BLACK)
        
        # Draw title
        title_text = self.game.fonts["large"].render("SQUATIVA", True, self.game.WHITE)
        title_rect = title_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT//4))
        self.game.screen.blit(title_text, title_rect)
        
        # Draw start button
        button_width, button_height = 300, 80
        button_x = (self.game.WIDTH - button_width) // 2
        button_y = self.game.HEIGHT // 2
        
        pygame.draw.rect(self.game.screen, self.game.BLUE, (button_x, button_y, button_width, button_height), border_radius=15)
        pygame.draw.rect(self.game.screen, self.game.WHITE, (button_x, button_y, button_width, button_height), 3, border_radius=15)
        
        start_text = self.game.fonts["medium"].render("START", True, self.game.WHITE)
        start_rect = start_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT//2 + button_height//2))
        self.game.screen.blit(start_text, start_rect)
        
        # Draw instructions
        instructions_text = self.game.fonts["small"].render("Click START to select a song", True, self.game.WHITE)
        instructions_rect = instructions_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT*3//4))
        self.game.screen.blit(instructions_text, instructions_rect)
        
        # Check for button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if (button_x <= mouse_pos[0] <= button_x + button_width and
            button_y <= mouse_pos[1] <= button_y + button_height and mouse_clicked):
            self.game.state = "SONG_SELECT"


class SongSelectScreen:
    def __init__(self, game):
        self.game = game
    
    def draw(self):
        # Draw background
        self.game.screen.fill((30, 30, 50))
        
        # Draw title
        title_text = self.game.fonts["large"].render("Select a Song", True, self.game.WHITE)
        title_rect = title_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT//8))
        self.game.screen.blit(title_text, title_rect)
        
        # Draw song buttons
        button_width, button_height = 500, 80
        button_spacing = 30
        start_y = self.game.HEIGHT//4
        
        for i, song in enumerate(self.game.music_library):
            button_x = (self.game.WIDTH - button_width) // 2
            button_y = start_y + i * (button_height + button_spacing)
            
            # Button color
            button_color = self.game.BLUE
            
            pygame.draw.rect(self.game.screen, button_color, 
                            (button_x, button_y, button_width, button_height), 
                            border_radius=15)
            pygame.draw.rect(self.game.screen, self.game.WHITE, 
                            (button_x, button_y, button_width, button_height), 
                            3, border_radius=15)
            
            song_text = self.game.fonts["medium"].render(song["title"], True, self.game.WHITE)
            song_rect = song_text.get_rect(center=(self.game.WIDTH//2, button_y + button_height//2))
            self.game.screen.blit(song_text, song_rect)
            
            # Check for button click
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            if (button_x <= mouse_pos[0] <= button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + button_height and mouse_clicked):
                self.game.selected_song = song
                self.game.state = "DIFFICULTY_SELECT"
        
        # Back button
        back_width, back_height = 200, 60
        back_x = 50
        back_y = self.game.HEIGHT - back_height - 50
        
        pygame.draw.rect(self.game.screen, self.game.RED, (back_x, back_y, back_width, back_height), border_radius=15)
        pygame.draw.rect(self.game.screen, self.game.WHITE, (back_x, back_y, back_width, back_height), 3, border_radius=15)
        
        back_text = self.game.fonts["small"].render("Back", True, self.game.WHITE)
        back_rect = back_text.get_rect(center=(back_x + back_width//2, back_y + back_height//2))
        self.game.screen.blit(back_text, back_rect)
        
        # Check for back button click
        if (back_x <= mouse_pos[0] <= back_x + back_width and
            back_y <= mouse_pos[1] <= back_y + back_height and mouse_clicked):
            self.game.state = "MENU"


class DifficultySelectScreen:
    def __init__(self, game):
        self.game = game
    
    def draw(self):
        # Draw background
        self.game.screen.fill((30, 30, 50))
        
        # Draw title
        title_text = self.game.fonts["large"].render(f"Select Difficulty: {self.game.selected_song['title']}", True, self.game.WHITE)
        title_rect = title_text.get_rect(center=(self.game.WIDTH//2, self.game.HEIGHT//8))
        self.game.screen.blit(title_text, title_rect)
        
        # Draw difficulty buttons
        button_width, button_height = 400, 80
        button_spacing = 30
        start_y = self.game.HEIGHT//3
        
        for i, difficulty in enumerate(self.game.selected_song["difficulties"]):
            button_x = (self.game.WIDTH - button_width) // 2
            button_y = start_y + i * (button_height + button_spacing)
            
            # Button color based on difficulty
            if difficulty["name"] == "Easy":
                button_color = self.game.GREEN
            elif difficulty["name"] == "Medium":
                button_color = self.game.YELLOW
            else:  # Hard
                button_color = self.game.RED
            
            pygame.draw.rect(self.game.screen, button_color, 
                            (button_x, button_y, button_width, button_height), 
                            border_radius=15)
            pygame.draw.rect(self.game.screen, self.game.WHITE, 
                            (button_x, button_y, button_width, button_height), 
                            3, border_radius=15)
            
            diff_text = self.game.fonts["medium"].render(difficulty["name"], True, self.game.WHITE)
            diff_rect = diff_text.get_rect(center=(self.game.WIDTH//2, button_y + button_height//2))
            self.game.screen.blit(diff_text, diff_rect)
            
            # Check for button click
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            if (button_x <= mouse_pos[0] <= button_x + button_width and
                button_y <= mouse_pos[1] <= button_y + button_height and mouse_clicked):
                self.game.selected_difficulty = difficulty
                self.game.start_game()
        
        # Back button
        back_width, back_height = 200, 60
        back_x = 50
        back_y = self.game.HEIGHT - back_height - 50
        
        pygame.draw.rect(self.game.screen, self.game.RED, (back_x, back_y, back_width, back_height), border_radius=15)
        pygame.draw.rect(self.game.screen, self.game.WHITE, (back_x, back_y, back_width, back_height), 3, border_radius=15)
        
        back_text = self.game.fonts["small"].render("Back", True, self.game.WHITE)
        back_rect = back_text.get_rect(center=(back_x + back_width//2, back_y + back_height//2))
        self.game.screen.blit(back_text, back_rect)
        
        # Check for back button click
        if (back_x <= mouse_pos[0] <= back_x + back_width and
            back_y <= mouse_pos[1] <= back_y + back_height and mouse_clicked):
            self.game.state = "SONG_SELECT"


class GameScreen:
    def __init__(self, game):
        self.game = game
    
    def draw_target_zone(self):
        # Draw the target zone where squat graphics should align
        pygame.draw.circle(self.game.screen, (50, 50, 50), self.game.target_position, self.game.target_zone_radius, 2)
        pygame.draw.circle(self.game.screen, (80, 80, 80), self.game.target_position, self.game.target_zone_radius - 5, 1)
    
    def draw_camera_feed(self):
        # Draw a placeholder for camera
        pygame.draw.rect(self.game.screen, (40, 40, 40), (self.game.WIDTH//2, 0, self.game.WIDTH//2, self.game.HEIGHT//2))
        text = self.game.fonts["small"].render("Camera placeholder (OpenCV integration)", True, self.game.WHITE)
        text_rect = text.get_rect(center=(self.game.WIDTH*3//4, self.game.HEIGHT//4))
        self.game.screen.blit(text, text_rect)
    
    def draw_game_ui(self):
        # Draw score
        score_text = self.game.fonts["medium"].render(f"Score: {self.game.score}", True, self.game.WHITE)
        self.game.screen.blit(score_text, (20, 20))
        
        # Draw song and difficulty info
        song_text = self.game.fonts["small"].render(f"Song: {self.game.selected_song['title']}", True, self.game.WHITE)
        self.game.screen.blit(song_text, (20, 80))
        
        diff_text = self.game.fonts["small"].render(f"Difficulty: {self.game.selected_difficulty['name']}", True, self.game.WHITE)
        self.game.screen.blit(diff_text, (20, 120))
        
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
            self.game.state = "MENU"
            pygame.mixer.music.stop()
    
    def draw(self):
        # Clear screen with dark background
        self.game.screen.fill((20, 20, 30))
        
        # Draw camera feed
        self.draw_camera_feed()
        
        # Draw target zone
        self.draw_target_zone()
        
        # Draw all active squat graphics
        for graphic in self.game.squat_graphics:
            draw_squat_graphic(self.game.screen, graphic)
        
        # Draw game UI elements
        self.draw_game_ui()