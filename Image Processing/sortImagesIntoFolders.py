# This python script will automatically sort a directory of images into folders based on the filename prefix
# Usage Example: cam001_0001.jpg, cam001_002.jpg would create a folder labeled cam001 and place both images in that directory
# By Jeffrey Ian Wilson for the 3D Scanning Masterclass (www.jeffreyianwilson.com)

import os
import shutil
import re

def sort_images_by_prefix(source_directory):
    # Ensure the source directory exists
    if not os.path.exists(source_directory):
        print(f"Source directory {source_directory} does not exist.")
        return

    # Regex pattern to match the prefix cam###
    prefix_pattern = re.compile(r"^(cam\d{3})")

    # Loop through files in the source directory
    for filename in os.listdir(source_directory):
        file_path = os.path.join(source_directory, filename)

        # Skip if not a file
        if not os.path.isfile(file_path):
            continue

        # Match the prefix
        match = prefix_pattern.match(filename)
        if match:
            prefix = match.group(1)  # Extract the prefix (e.g., cam001)

            # Create a folder with the prefix if it doesn't exist
            folder_path = os.path.join(source_directory, prefix)
            os.makedirs(folder_path, exist_ok=True)

            # Move the file into the folder
            shutil.move(file_path, os.path.join(folder_path, filename))

    print("Sorting completed.")

# Example usage
if __name__ == "__main__":
    source_directory = input("Enter the path to the source directory: ").strip()
    sort_images_by_prefix(source_directory)