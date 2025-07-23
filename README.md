# Event-Management
Generation, Distribution &amp; Management of Customised tickets for an event. 
The biggest challenge was carrying out the entire process using only open source tools and trial limits. 


Step 1 :
-	Qr code generation
-	Put numbers 2001… and generate qr codes using limitqr (extension in gsheets) and download the files on computer.
  
Step 2:
-	Put all the images of qr codes in a file and note the path. 
-	Change the data.csv file with the last path name according to the numbers associated with the the excel sheet.
-	Use the generate.py code to generate tickets. 

CODE FOR THE PURPOSE:
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
                draw.text((50,100),"Date      : 29/05/2025", fill='black',font=font)
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

Modify the required details 

Step 3 :
-	Upload the tickets generated in a google drive as a folder. Enable the share feature.
-	Change the view access as “anyone on the internet with the link can view”
Step 4:
-	Get a direct link for all the drive link images. 
-	To do so, open a google excel sheet. Go to extensions and open apps script. 
-	Copy this code.

function generateImageLinksFromFolder() {
  const folderId = '1XW_KrZpKXHd_e2ATerJr9im_gy58f4ic'; // Replace this with your real folder ID
  const folder = DriveApp.getFolderById(folderId);
  const files = folder.getFiles();

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.clear(); // Clears old data
  sheet.appendRow(["Filename", "Direct Image Link"]);

  while (files.hasNext()) {
    const file = files.next();
    const name = file.getName();
    const id = file.getId();
    const directLink = "https://drive.google.com/uc?export=view&id=" + id;
    sheet.appendRow([name, directLink]);
  }
}

-	Change the folder name or id if required. 

Step 5:
-	Use the direct link to create a html tag <img src=” direct link “ width=’500’>
Step 6:
-	Use gmass to share the images customised to each other. 

