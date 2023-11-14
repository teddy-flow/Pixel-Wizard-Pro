import os
from PIL import Image

def process_images():
    # User inputs
    folder_path = input("Enter the path to the folder containing the images: ")
    output_folder_name = "new"
    
    print("Enter final resolution (width x height):")
    final_width = int(input("  Final width: "))
    final_height = int(input("  Final height: "))

    # Ask for rotation
    rotate_choice = input("Do you want to rotate the image? (yes/no): ").lower()
    rotation_direction = ""
    if rotate_choice == 'yes':
        rotation_direction = input("Rotate to the left or right? (left/right): ").lower()
        if rotation_direction not in ['left', 'right']:
            print("Invalid rotation direction. Please choose 'left' or 'right'.")
            return  # Exit the function if an invalid choice is made

    # Calculate crop resolution as 50% of the final resolution
    crop_width = final_width // 2
    crop_height = final_height // 2

    # Create the output folder if it doesn't exist
    output_folder_path = os.path.join(folder_path, output_folder_name)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".jpg"):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)

            # Rotate the image if requested
            rotated_image = image
            if rotate_choice == 'yes':
                angle = 90 if rotation_direction == 'left' else -90
                rotated_image = image.rotate(angle, expand=True)

            # Calculate the number of crops based on the original image size
            num_crops_horizontal = (rotated_image.width + crop_width - 1) // crop_width  # Round up division
            num_crops_vertical = (rotated_image.height + crop_height - 1) // crop_height  # Round up division

            # Crop, resize, and save each section
            for i in range(num_crops_vertical):
                for j in range(num_crops_horizontal):
                    start_x = min(j * crop_width, rotated_image.width - crop_width)
                    start_y = min(i * crop_height, rotated_image.height - crop_height)
                    end_x = start_x + crop_width
                    end_y = start_y + crop_height

                    cropped_image = rotated_image.crop((start_x, start_y, end_x, end_y))
                    resized_image = cropped_image.resize((final_width, final_height))
                    resized_image.save(os.path.join(output_folder_path, f"{filename}_crop_{i}_{j}.jpg"))

# Run the function
process_images()
