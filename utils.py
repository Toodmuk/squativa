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
            fonts["sn"] = pygame.font.Font(font_path, 24)
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
    
    # Get the image from the graphic
    squat_image = graphic.get("image")
    
    if squat_image is None:
        # print("Warning: No image in graphic, skipping draw")
        return
    
    # Scale image to fit graphic dimensions
    scaled_image = pygame.transform.scale(squat_image, (graphic["width"], graphic["height"]))
    
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
    
    # # For debugging, draw the position coordinates
    # debug_font = pygame.font.SysFont("Arial", 12)
    # pos_text = debug_font.render(f"({int(graphic['x'])},{int(graphic['y'])})", True, (255, 255, 255))
    # surface.blit(pos_text, (graphic["x"] - 20, graphic["y"] - graphic["height"]//2 - 20))

# In utils.py, add this function to load the background image
def load_background_image():
    """Load background image for the game"""
    try:
        # Try to load the background image
        # Update this path to where you've placed your background image
        image_path = "graphics/bg.png"
        
        # Check if file exists first
        if os.path.exists(image_path):
            print(f"Loading background image from: {image_path}")
            background = pygame.image.load(image_path).convert()
            print("Background image loaded successfully!")
            return background
        else:
            # Try alternative file extensions
            alt_path = "graphics/bg.png"
            if os.path.exists(alt_path):
                print(f"Loading background image from: {alt_path}")
                background = pygame.image.load(alt_path).convert()
                print("Background image loaded successfully!")
                return background
            else:
                print("No background image found at the specified path.")
                return None
    except Exception as e:
        print(f"Error loading background image: {e}")
        return None

# Add this function to scale the background to fit the screen
def scale_background(background, screen_width, screen_height):
    """Scale background image to fit the screen"""
    if background is None:
        return None
    
    try:
        # Scale the image to fill the screen while maintaining aspect ratio
        bg_width, bg_height = background.get_size()
        scale_factor = max(screen_width / bg_width, screen_height / bg_height)
        
        new_width = int(bg_width * scale_factor)
        new_height = int(bg_height * scale_factor)
        
        scaled_bg = pygame.transform.scale(background, (new_width, new_height))
        
        # Create a cropping rect to center the image if it's larger than the screen
        crop_x = max(0, (new_width - screen_width) // 2)
        crop_y = max(0, (new_height - screen_height) // 2)
        
        cropped_bg = scaled_bg.subsurface((crop_x, crop_y, screen_width, screen_height))
        return cropped_bg
    except Exception as e:
        print(f"Error scaling background: {e}")
        return None