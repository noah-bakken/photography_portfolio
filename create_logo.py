from PIL import Image, ImageDraw, ImageFont
import os

def create_logo(width=200, height=50):
    # Create a new image with a transparent background
    image = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Add text
    try:
        font = ImageFont.truetype("Arial", 30)
    except:
        font = ImageFont.load_default()
    
    # Draw the text
    text = "Travel Lens"
    draw.text((10, 10), text, fill='#333333', font=font)
    
    # Save the image
    os.makedirs('static', exist_ok=True)
    image.save('static/logo.png', 'PNG')

if __name__ == '__main__':
    create_logo() 