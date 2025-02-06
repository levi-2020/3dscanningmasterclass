# This python script will automatically sort Navvis imagery into a directory structure compatible with Agisoft Metashape camera rig functions
# By Jeffrey Ian Wilson for the 3D Scanning Masterclass (www.jeffreyianwilson.com)

import os
import re
import shutil

def sort_navvis_images(source_dir):
    # Ensure the source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    # Regular expression to match "cam#" in filenames
    cam_pattern = re.compile(r'cam(\d+)')

    # Iterate through all files in the source directory
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Search for "cam#" in the filename
            match = cam_pattern.search(filename)
            
            if match:
                cam_number = match.group(1)
                target_dir = os.path.join(source_dir, f"cam{cam_number}")
                
                # Create the target directory if it doesn't exist
                os.makedirs(target_dir, exist_ok=True)
                
                # Move the file to the target directory
                target_path = os.path.join(target_dir, filename)
                shutil.move(file_path, target_path)
                print(f"Moved '{filename}' to '{target_dir}'")

if __name__ == "__main__":
    # Ask for user input for the source directory
    source_directory = input("Enter the path to your image directory: ").strip()
    sort_navvis_images(source_directory)
