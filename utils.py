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

# Store the squat image so we only load it once
_squat_image = None

def draw_squat_graphic(surface, graphic):
    global _squat_image
    
    # Create a temporary surface for this frame
    temp_surface = pygame.Surface((graphic["width"], graphic["height"]), pygame.SRCALPHA)
    
    # If the graphic is at the target zone, make it shine
    if graphic["shine"] > 0:
        # Create a glow/shine effect
        glow_radius = int(graphic["width"] // 2 + graphic["shine"] * 5)
        pygame.draw.rect(
            temp_surface, 
            (255, 255, 100, int(100 - graphic["shine"] * 10)),
            (graphic["width"]//2 - glow_radius, graphic["height"]//2 - glow_radius, 
             glow_radius * 2, glow_radius * 2),
            border_radius=glow_radius
        )
    
    # Create a simple graphic instead of trying to load an image
    if _squat_image is None:
        print("Creating a new squat graphic")
        # Create a simple stick figure squat
        _squat_image = pygame.Surface((100, 100), pygame.SRCALPHA)
        
        # Background circle
        pygame.draw.circle(_squat_image, (150, 100, 255, 200), (50, 50), 45)
        pygame.draw.circle(_squat_image, (200, 150, 255, 200), (50, 50), 45, 3)
        
        # Draw a simple stick figure in squat position
        # Head
        pygame.draw.circle(_squat_image, (255, 255, 255), (50, 30), 12)
        
        # Body
        pygame.draw.line(_squat_image, (255, 255, 255), (50, 42), (50, 65), 4)
        
        # Arms in squat position
        pygame.draw.line(_squat_image, (255, 255, 255), (50, 50), (25, 60), 4)
        pygame.draw.line(_squat_image, (255, 255, 255), (50, 50), (75, 60), 4)
        
        # Legs in squat position
        pygame.draw.line(_squat_image, (255, 255, 255), (50, 65), (30, 85), 4)
        pygame.draw.line(_squat_image, (255, 255, 255), (50, 65), (70, 85), 4)
        
        # Add text 
        font = pygame.font.SysFont("Arial", 12, bold=True)
        text = font.render("SQUAT", True, (255, 255, 255))
        text_rect = text.get_rect(center=(50, 15))
        _squat_image.blit(text, text_rect)
    
    # Scale image to fit graphic dimensions
    scaled_image = pygame.transform.scale(_squat_image, (graphic["width"], graphic["height"]))
    
    # Apply opacity
    if graphic["opacity"] < 255:
        # Create a copy with adjusted alpha
        alpha_image = scaled_image.copy()
        alpha_value = max(0, min(255, int(graphic["opacity"])))
        alpha_image.fill((255, 255, 255, alpha_value), None, pygame.BLEND_RGBA_MULT)
        scaled_image = alpha_image
    
    # Draw the image onto the temporary surface
    temp_surface.blit(scaled_image, (0, 0))
    
    # Position and draw the graphic
    surface.blit(temp_surface, (graphic["x"] - graphic["width"]//2, graphic["y"] - graphic["height"]//2))
    
    # For debugging, draw the position coordinates
    debug_font = pygame.font.SysFont("Arial", 12)
    pos_text = debug_font.render(f"({int(graphic['x'])},{int(graphic['y'])})", True, (255, 255, 255))
    surface.blit(pos_text, (graphic["x"] - 20, graphic["y"] - graphic["height"]//2 - 20))