import os
import shutil

def duplicate_file(file_path, num_copies, padding):
    # Replace backslashes if present
    file_path = file_path.replace('\\', '/')
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Get the file's directory, name, and extension
    file_dir, file_name = os.path.split(file_path)
    file_base, file_ext = os.path.splitext(file_name)

    # Create the specified number of copies with padded copy number
    for i in range(1, num_copies + 1):
        padded_number = str(i).zfill(padding)  # Pad the copy number with leading zeros
        new_file_name = f"{file_base}_{padded_number}_{suffix}{file_ext}"
        new_file_path = os.path.join(file_dir, new_file_name)
        shutil.copy(file_path, new_file_path)
        print(f"Created: {new_file_path}")

if __name__ == "__main__":
    # Get user input for the file path, number of copies, and padding
    file_path = input("Enter the path of the file to duplicate: ").replace('"', '').replace('\\', '/')
    num_copies = int(input("Enter the number of copies to create: "))
    padding = int(input("Enter the padding for the copy number (e.g., 3 for 001): "))
    suffix = input("Enter suffix label: ")
    # Call the function to duplicate the file with padding
    duplicate_file(file_path, num_copies, padding)
