from PIL import Image
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import sys

def convert_images_to_pdf(input_dir, output_pdf, use_margins=True):
    """
    Convert multiple images into a single PDF file, cropping from bottom if needed.
    
    Args:
        input_dir (str): Directory containing the image files
        output_pdf (str): Name of the output PDF file
        use_margins (bool): Whether to add margins around images (default: True)
    """
    try:
        # Get all image files from the directory
        image_files = []
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_files.append(os.path.join(input_dir, filename))
        
        if not image_files:
            print("No image files found in the specified directory!")
            return
        
        # Sort files to maintain order
        image_files.sort()
        
        # Create PDF
        c = canvas.Canvas(output_pdf, pagesize=letter)
        page_width, page_height = letter
        
        # Set margin size
        margin = 20 if use_margins else 0
        
        # Available width and height for image
        available_width = page_width - (2 * margin)
        available_height = page_height - (2 * margin)
        
        # Process each image
        for image_path in image_files:
            try:
                # Open and process image
                img = Image.open(image_path)
                
                # Convert image to RGB if it's not
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Calculate scaling factor to fit width while maintaining aspect ratio
                scale_factor = available_width / img.width
                
                # Calculate new dimensions
                new_width = available_width
                new_height = min(img.height * scale_factor, available_height)
                
                # Position image at top of page with margins
                x = margin
                y = page_height - margin - new_height
                
                # Draw image on PDF
                c.drawImage(image_path, x, y, new_width, new_height)
                
                # Add a message if image was cropped
                if img.height * scale_factor > available_height:
                    cropped_percent = round((1 - (available_height / (img.height * scale_factor))) * 100, 1)
                    print(f"Warning: {os.path.basename(image_path)} was cropped {cropped_percent}% from bottom to fit page")
                
                c.showPage()
                print(f"Processed: {os.path.basename(image_path)}")
                
            except Exception as e:
                print(f"Error processing {image_path}: {str(e)}")
                continue
        
        # Save PDF
        c.save()
        print(f"\nPDF created successfully: {output_pdf}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_user_margin_preference():
    """Get user preference for margins"""
    while True:
        response = input("Would you like to add margins around the images? (yes/no): ").lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        print("Please enter 'yes' or 'no'")

def main():
    # Example usage
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_directory> <output_pdf>")
        print("Example: python script.py ./images output.pdf")
        return
    
    input_dir = sys.argv[1]
    output_pdf = sys.argv[2]
    
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' does not exist!")
        return
    
    # Get user preference for margins
    use_margins = get_user_margin_preference()
        
    convert_images_to_pdf(input_dir, output_pdf, use_margins)

if __name__ == "__main__":
    main()