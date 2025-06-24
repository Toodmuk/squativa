import pygame
import sys
from game import Squativa
import cv2

def main():
    try:
        print("Starting Fitness Dance Game with forced background...")

        # Initialize pygame first
        pygame.init()
        pygame.mixer.init()

        # Pre-load the background image directly
        print("Pre-loading background image...")
        try:
            bg = pygame.image.load("graphics/bg.png").convert()
            print(f"Successfully pre-loaded background! Size: {bg.get_size()}")
        except Exception as e:
            print(f"Error pre-loading background: {e}")
            bg = None
        
        # Now initialize the game
        game = Squativa()
        
        # Force the background into the game object
        if bg:
            print("Forcing background into game object...")
            game.background_image = bg
            
            # Calculate the right scale
            scale_w = game.WIDTH / bg.get_width()
            scale_h = game.HEIGHT / bg.get_height()
            scale = max(scale_w, scale_h)
            
            new_width = int(bg.get_width() * scale)
            new_height = int(bg.get_height() * scale)
            
            scaled_bg = pygame.transform.scale(bg, (new_width, new_height))
            
            # Crop to fit if needed
            crop_x = max(0, (new_width - game.WIDTH) // 2)
            crop_y = max(0, (new_height - game.HEIGHT) // 2)
            
            game.scaled_background = scaled_bg.subsurface((crop_x, crop_y, game.WIDTH, game.HEIGHT))
            print("Background forced and scaled!")
        
        game.run()
    except Exception as e:
        print(f"Game crashed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cv2.destroyAllWindows()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()