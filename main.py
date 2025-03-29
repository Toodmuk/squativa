import pygame
import sys
from game import FitnessDanceGame
import cv2  # Add OpenCV import

def main():
    # Simple error handling to show any crashes
    try:
        print("Starting Fitness Dance Game...")
        game = FitnessDanceGame()
        print("Game initialized, starting main loop")
        game.run()
    except Exception as e:
        print(f"Game crashed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Make sure to release any OpenCV resources
        cv2.destroyAllWindows()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()