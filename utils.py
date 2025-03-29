import pygame
import os

def load_fonts():
    """Load custom TTF fonts for the game"""
    fonts = {}
    try:
        # Font file paths - update these to your actual font paths
        font_path = "fonts/ARCADECLASSIC.ttf"  
        
        # Check if the font file exists
        if not os.path.exists(font_path):
            print(f"Warning: Font file not found at {font_path}")
            print("Using system fonts as fallback")
            # Fallback to system fonts if custom font not found
            fonts["large"] = pygame.font.SysFont("Arial", 72, bold=True)
            fonts["medium"] = pygame.font.SysFont("Arial", 48)
            fonts["small"] = pygame.font.SysFont("Arial", 32)
        else:
            # Create font objects with custom font in different sizes
            fonts["large"] = pygame.font.Font(font_path, 72)
            fonts["medium"] = pygame.font.Font(font_path, 48)
            fonts["small"] = pygame.font.Font(font_path, 32)
            print("Custom font loaded successfully!")
    except Exception as e:
        print(f"Error loading fonts: {e}")
        # Fallback to system fonts if there's an error
        fonts["large"] = pygame.font.SysFont("Arial", 72, bold=True)
        fonts["medium"] = pygame.font.SysFont("Arial", 48)
        fonts["small"] = pygame.font.SysFont("Arial", 32)
    
    return fonts

def load_music_library():
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

def draw_squat_graphic(surface, graphic):
    # Draw the squat graphic (currently just a square, you'll replace with your own graphic)
    temp_surface = pygame.Surface((graphic["width"], graphic["height"]), pygame.SRCALPHA)
    
    # If the graphic is at the target zone, make it shine
    if graphic["shine"] > 0:
        # Create a glow/shine effect - Fix the integer conversion error
        glow_radius = int(graphic["width"] // 2 + graphic["shine"] * 5)  # Convert to integer
        pygame.draw.rect(
            temp_surface, 
            (255, 255, 100, int(100 - graphic["shine"] * 10)),  # Convert to integer
            (graphic["width"]//2 - glow_radius, graphic["height"]//2 - glow_radius, 
             glow_radius * 2, glow_radius * 2),
            border_radius=glow_radius
        )
    
    # Draw the actual graphic with current opacity
    pygame.draw.rect(
        temp_surface, 
        (255, 255, 255, int(graphic["opacity"])),  # Convert to integer
        (0, 0, graphic["width"], graphic["height"]),
        border_radius=15
    )
    
    pygame.draw.rect(
        temp_surface, 
        (0, 150, 255, int(graphic["opacity"])),  # Convert to integer 
        (0, 0, graphic["width"], graphic["height"]), 
        3, 
        border_radius=15
    )
    
    # Draw a simple squat icon inside the square (placeholder)
    if graphic["opacity"] > 50:
        # Stick figure for squat
        pygame.draw.circle(
            temp_surface, 
            (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
            (graphic["width"]//2, graphic["height"]//4), 
            10
        )
        pygame.draw.line(
            temp_surface, 
            (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
            (graphic["width"]//2, graphic["height"]//4), 
            (graphic["width"]//2, graphic["height"]//2), 
            5
        )
        pygame.draw.line(
            temp_surface, 
            (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
            (graphic["width"]//2, graphic["height"]//2), 
            (graphic["width"]//3, graphic["height"]*3//4), 
            5
        )
        pygame.draw.line(
            temp_surface, 
            (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
            (graphic["width"]//2, graphic["height"]//2), 
            (graphic["width"]*2//3, graphic["height"]*3//4), 
            5
        )
        pygame.draw.line(
            temp_surface, 
            (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
            (graphic["width"]//2, graphic["height"]//2), 
            (graphic["width"]//3, graphic["height"]*2//5), 
            5
        )
        pygame.draw.line(
            temp_surface, 
            (0, 0, 0, int(graphic["opacity"])),  # Convert to integer
            (graphic["width"]//2, graphic["height"]//2), 
            (graphic["width"]*2//3, graphic["height"]*2//5), 
            5
        )
    
    # Position and draw the graphic
    surface.blit(temp_surface, (graphic["x"] - graphic["width"]//2, graphic["y"] - graphic["height"]//2))