from PIL import Image, ImageDraw, ImageFont
import os

def create_default_profile_image():
    # Create a 200x200 image with a light blue background
    size = (200, 200)
    bg_color = (100, 149, 237)  # Cornflower blue
    text_color = (255, 255, 255)  # White
    
    # Create new image with background color
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw a circle for the avatar background
    circle_diameter = 180
    circle_xy = ((size[0] - circle_diameter) // 2,
                (size[1] - circle_diameter) // 2,
                (size[0] + circle_diameter) // 2,
                (size[1] + circle_diameter) // 2)
    draw.ellipse(circle_xy, fill=(80, 119, 189))
    
    # Add text
    text = "?"
    try:
        # Try to load a font
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Get text size and center it
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_xy = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    
    # Draw the text
    draw.text(text_xy, text, fill=text_color, font=font)
    
    # Save the image
    img.save("default_profile.png")

if __name__ == "__main__":
    create_default_profile_image() 