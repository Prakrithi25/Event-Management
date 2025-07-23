from PIL import Image, ImageDraw, ImageFont
import csv

def generate_images(csv_file):
    template = Image.new('RGB', (800, 300), 'white')
    
    try:
        font = ImageFont.truetype("times.ttf", 40)
    except OSError:
        # Fallback to default font if arial.ttf is not found
        font = ImageFont.load_default()
    
    text_position = (50, 50)
    image_position = (550, 50)
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        # Debug: Print column headers
        print("Available columns:", reader.fieldnames)
        
        for row_num, row in enumerate(reader, 1):
            try:
                img = template.copy()
                draw = ImageDraw.Draw(img)
                
                # Use flexible column access
                name = get_column_value(row, 'name')
                image_path = get_column_value(row, 'image_path')
                
                # Add text
                draw.text(text_position, f"Name    : {name}", fill='black', font=font)
                draw.text((50,100),"Date      : 29/06/2025", fill='black',font=font)
                draw.text((50,150),"Time     : 5.30pm onwards", fill='black',font=font)
                draw.text((50,200),"Venue   : Hotel Hablis", fill='black',font=font)
                draw.text((50,250),"", fill='black',font=font)

                # Add image if path exists
                try:
                    custom_image = Image.open(image_path).resize((200, 200))
                    img.paste(custom_image, image_position)
                except FileNotFoundError:
                    print(f"Warning: Image file '{image_path}' not found for {name}")
                    # Create a colored rectangle as placeholder
                    placeholder = Image.new('RGB', (200, 200), color='gray')
                    img.paste(placeholder, image_position)
                
                # Save the result
                img.save(f"output_{name}.png")
                print(f"Generated image for {name}")
                
            except KeyError as e:
                print(f"Error in row {row_num}: {e}")
                print(f"Row data: {row}")
                continue

def get_column_value(row, column_name):
    # Try exact match first
    if column_name in row:
        return row[column_name]
    
    # Try case-insensitive match
    for key in row.keys():
        if key.lower().strip() == column_name.lower():
            return row[key]
    
    raise KeyError(f"Column '{column_name}' not found. Available columns: {list(row.keys())}")

# Run the function
generate_images("data.csv")
