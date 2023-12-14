from PIL import Image
import os

def overlay_images(base_image_path, output_directory, *overlay_directories):
    # Ensure the BASE image exists
    if not os.path.exists(base_image_path):
        print(f"Error: BASE image {base_image_path} not found.")
        return

    # Open the base image
    base_image = Image.open(base_image_path)

    # Ensure the base image is in RGBA mode
    base_image = base_image.convert("RGBA")

    # Loop through each overlay directory in the specified order
    for i, overlay_directory in enumerate(overlay_directories):
        # Ensure the overlay directory exists
        if not os.path.exists(overlay_directory):
            print(f"Error: Directory {overlay_directory} not found.")
            continue

        # Loop through each file in the overlay directory
        for j, overlay_file in enumerate(os.listdir(overlay_directory)):
            if overlay_file.endswith(".png"):
                overlay_path = os.path.join(overlay_directory, overlay_file)

                # Open the overlay image
                overlay_image = Image.open(overlay_path)

                # Ensure the overlay image is in RGBA mode
                overlay_image = overlay_image.convert("RGBA")

                # Resize the overlay image to fit the base image if needed
                overlay_image = overlay_image.resize(base_image.size, Image.BICUBIC)

                # Create a new image with an "RGBA" mode for the composite
                composite_image = Image.new("RGBA", base_image.size, (0, 0, 0, 0))

                # Paste the overlay image onto the composite image with transparency
                composite_image.paste(overlay_image, (0, 0), overlay_image)

                # Paste the base image onto the composite image using the alpha channel as a mask
                composite_image.paste(base_image, (0, 0), base_image)

                # Convert to "RGB" before saving (JPEG does not support alpha channel)
                composite_image = composite_image.convert("RGB")

                # Save the result to the output directory with a sequential name
                output_path = os.path.join(output_directory, f"result_{i:02d}_{j:02d}.jpg")
                composite_image.save(output_path, "JPEG")

                print(f"Overlay created: {output_path}")

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.realpath(__file__))
    base_image_path = os.path.join(script_directory, "BASE.png")
    output_directory = os.path.join(script_directory, "out")
    overlay_directories = [
        os.path.join(script_directory, "BACKGROUNDZ"),
        os.path.join(script_directory, "EYEZ"),
        os.path.join(script_directory, "MOUTHZ"),
        os.path.join(script_directory, "WEAPONZ"),
    ]

    # Ensure the output directory exists, create if it doesn't
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    overlay_images(base_image_path, output_directory, *overlay_directories)
