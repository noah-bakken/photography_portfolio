from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(width=800, height=450, text="No Image Available"):
    # Create a new image with a light gray background
    image = Image.new('RGB', (width, height), color='#f0f0f0')
    draw = ImageDraw.Draw(image)
    
    # Add a border
    draw.rectangle([(0, 0), (width-1, height-1)], outline='#cccccc', width=2)
    
    # Add text
    try:
        font = ImageFont.truetype("Arial", 40)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw the text
    draw.text((x, y), text, fill='#666666', font=font)
    
    # Save the image
    os.makedirs('static/photos/placeholder', exist_ok=True)
    image.save('static/photos/placeholder/placeholder.jpg', 'JPEG')

if __name__ == '__main__':
    create_placeholder() 