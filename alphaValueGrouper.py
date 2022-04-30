# Group images by their transparency value
import os
from PIL import Image

def alphaGrouping(directory):

    alphaDirectory = f"{directory}alpha/"
    rgbDirectory = f"{directory}RGB/"

    subDirectoriesList = [
        alphaDirectory,
        rgbDirectory,
    ]

    # Check if folders exist to sort images into
    for dir in subDirectoriesList:
        if not os.path.isdir(dir):
            os.mkdir(dir)

    # checks if file in directory is a .png
    images = [entry for entry in os.scandir(directory) if entry.name.endswith(".png")]

    for image in images: # gets the Alpha channel of an Image and checks how many differences there are, if 1 it has no transparency
        if len(Image.open(image.path).getchannel("A").getcolors()) > 1:
            os.replace(image.path, alphaDirectory + image.name)
        else:
            os.replace(image.path, rgbDirectory + image.name)
