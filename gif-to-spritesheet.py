from PIL import Image
import os

def gif_to_frames(gif_path):
    # Use the temp folder for storing extracted frames
    temp_folder = "temp"
    
    # Create the temp folder if it doesn't exist
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    
    # Open the GIF file
    gif = Image.open(gif_path)
    
    # Get the width and height of the GIF frames
    frame_width, frame_height = gif.size
    print(f"Frame size: {frame_width}x{frame_height} for {os.path.basename(gif_path)}")
    
    # List to hold all frames
    frames = []
    
    # Loop through each frame in the GIF
    frame_number = 0
    try:
        while True:
            # Append each frame to the list of frames
            frame = gif.copy().convert("RGBA")  # Convert to RGBA to handle transparency
            frames.append(frame)
            frame_number += 1
            gif.seek(gif.tell() + 1)
    except EOFError:
        # End of the GIF
        pass

    print(f"Extracted {frame_number} frames.")
    return frames, frame_width, frame_height

def frames_to_sprite_sheet(frames, sprite_sheet_path, frame_width, frame_height, columns):
    # Calculate the required number of rows based on columns and number of frames
    rows = (len(frames) + columns - 1) // columns  # Ceiling division
    
    # Create a blank image for the sprite sheet
    sprite_sheet = Image.new("RGBA", (frame_width * columns, frame_height * rows))
    
    # Paste each frame into the sprite sheet
    for i, frame in enumerate(frames):
        x = (i % columns) * frame_width
        y = (i // columns) * frame_height
        sprite_sheet.paste(frame, (x, y))

    # Save the sprite sheet
    sprite_sheet.save(sprite_sheet_path)
    print(f"Sprite sheet saved at: {sprite_sheet_path}")

# Function to process all GIFs in a given folder
def process_all_gifs(input_folder, output_folder, columns):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop through all files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".gif"):
            gif_path = os.path.join(input_folder, file_name)
            sprite_sheet_name = os.path.splitext(file_name)[0] + ".png"  # Keep the same name, change the extension to .png
            sprite_sheet_path = os.path.join(output_folder, sprite_sheet_name)
            
            # Extract frames and dimensions from the GIF
            frames, frame_width, frame_height = gif_to_frames(gif_path)
            
            # Create the sprite sheet from frames
            frames_to_sprite_sheet(frames, sprite_sheet_path, frame_width, frame_height, columns)

# Example usage to process all GIFs in the input folder
input_folder = "input"  # Folder containing GIFs
output_folder = "output"  # Folder where sprite sheets will be saved
columns = 4  # Number of columns in the sprite sheet

# Process all GIFs in the input folder
process_all_gifs(input_folder, output_folder, columns)