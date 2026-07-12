import os
from PIL import Image, ImageDraw, ImageFont

class KineticUI:
    """
    Generates basic Kinetic UI frames (images) using Pillow.
    For the MVP, this generates a 1920x1080 image with a dark background, 
    the keyword centered, and the emoji symbol.
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.width = 1920
        self.height = 1080
        self.bg_color = (20, 20, 25) # Dark gray/blue
        self.text_color = (255, 255, 255)
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_frame(self, text: str, symbol: str, frame_id: str) -> str:
        """Generates an image frame and returns the file path."""
        # Create base image
        img = Image.new('RGB', (self.width, self.height), color=self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # We will use default PIL font since we don't have custom TTFs in the project yet
        # In a real app we would load a custom font like Inter or Roboto
        try:
            # Try to use a standard Windows font if available
            font_large = ImageFont.truetype("arial.ttf", 120)
            font_emoji = ImageFont.truetype("seguiemj.ttf", 200) # Windows Emoji font
        except IOError:
            # Fallback to default
            font_large = ImageFont.load_default()
            font_emoji = ImageFont.load_default()
            
        # Draw Symbol
        # We estimate text size for centering since getsize is deprecated in newer PIL
        # Using bounding box
        bbox_symbol = draw.textbbox((0, 0), symbol, font=font_emoji)
        w_sym = bbox_symbol[2] - bbox_symbol[0]
        h_sym = bbox_symbol[3] - bbox_symbol[1]
        draw.text(((self.width-w_sym)/2, (self.height/2) - 200), symbol, font=font_emoji, fill=(255, 200, 0))
        
        # Draw Keyword
        bbox_text = draw.textbbox((0, 0), text, font=font_large)
        w_txt = bbox_text[2] - bbox_text[0]
        # h_txt = bbox_text[3] - bbox_text[1]
        draw.text(((self.width-w_txt)/2, (self.height/2) + 50), text, font=font_large, fill=self.text_color)
        
        # Save frame
        file_path = os.path.join(self.output_dir, f"frame_{frame_id}.png")
        img.save(file_path)
        return file_path
