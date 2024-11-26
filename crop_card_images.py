import glob
import os
from utils import create_folder_if_not_exists

from PIL import Image

def main():
    directory_path = "./database/card_images/en"
    destination_directory = "./database/cropped-images"

    create_folder_if_not_exists(destination_directory)

    Images = glob.glob(os.path.join(directory_path,"*.jpg"))

    for image_file_and_path in Images:
        image_filename = os.path.basename(image_file_and_path)
        output_filename = os.path.join(destination_directory, image_filename)
        uncropped_image = Image.open(image_file_and_path)

        # The argument to crop is a box : a 4-tuple defining the left, upper, right, and lower pixel positions.
        left = 35
        top = 220
        width = 674
        height = 197

        CroppedImg = uncropped_image.crop((left, top, width + left, height + top))

        CroppedImg.save(output_filename)

if __name__ == "__main__":
    main()