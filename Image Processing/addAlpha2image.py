from PIL import Image
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_image(base_dir, alpha_dir, output_dir, base_filename, invert_mask):
    base_path = os.path.join(base_dir, base_filename)
    
    # Find corresponding alpha image with the same name but possibly different extension
    alpha_filename = None
    for ext in ['.png', '.jpg', '.jpeg']:
        potential_alpha_path = os.path.join(alpha_dir, os.path.splitext(base_filename)[0] + ext)
        if os.path.isfile(potential_alpha_path):
            alpha_filename = os.path.splitext(base_filename)[0] + ext
            break

    if alpha_filename:
        alpha_path = os.path.join(alpha_dir, alpha_filename)
        try:
            base_image = Image.open(base_path).convert("RGBA")
            alpha_image = Image.open(alpha_path).convert("L")  # Convert alpha image to grayscale

            if invert_mask:
                alpha_image = Image.eval(alpha_image, lambda x: 255 - x)

            if base_image.size != alpha_image.size:
                alpha_image = alpha_image.resize(base_image.size, Image.ANTIALIAS)

            r, g, b, _ = base_image.split()
            combined_image = Image.merge("RGBA", (r, g, b, alpha_image))

            output_filename = os.path.splitext(base_filename)[0] + '.png'  # Save output as PNG
            output_path = os.path.join(output_dir, output_filename)
            combined_image.save(output_path)

            return output_filename
        except Exception as e:
            return f"Error processing {base_filename}: {e}"
    return f"Skipping {base_filename}: corresponding alpha image not found."

def add_alpha_channel(base_dir, alpha_dir, output_dir, invert_mask=False):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = [f for f in os.listdir(base_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total_files = len(files)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_image, base_dir, alpha_dir, output_dir, filename, invert_mask) for filename in files]

        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            print(f"Processed {index}/{total_files}: {result}")

if __name__ == "__main__":
    base_dir = input("Enter the path to the base images directory: ")
    alpha_dir = input("Enter the path to the alpha images directory: ")
    output_dir = input("Enter the path to the output directory: ")
    invert_input = input("Do you want to invert the mask? (y/n): ").strip().lower()
    invert_mask = invert_input == 'y'

    add_alpha_channel(base_dir, alpha_dir, output_dir, invert_mask)
