# Group images by their transparency value
import os
from PIL import Image

def alphaGrouping(directory):

    alpha_directory = os.path.join(directory, "alpha")
    rgb_directory = os.path.join(directory, "RGB")

    sub_directories_list = [
        alpha_directory,
        rgb_directory,
    ]

    # Check if folders exist to sort images into
    for dir in sub_directories_list:
        if not os.path.isdir(dir):
            os.mkdir(dir)

    # checks if file in directory is a .png
    image_list = [entry for entry in os.scandir(directory) if entry.name.endswith(".png")]

    for image in image_list: # gets the Alpha channel of an Image and checks how many differences there are, if 1 it has no transparency
        if len(Image.open(image.path).getchannel("A").getcolors()) > 1:
            os.replace(image.path, os.path.join(alpha_directory, image.name))
        else:
            os.replace(image.path, os.path.join(rgb_directory, image.name))
