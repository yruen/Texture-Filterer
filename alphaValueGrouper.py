# Group images by their transparency value
import os
from PIL import Image

def alphaGrouping(mainDirectory):

    alphaDirectory = f"{mainDirectory}alpha/"
    rgbDirectory = f"{mainDirectory}RGB/"

    subDirectoriesList = [alphaDirectory, rgbDirectory,]

    # Check if folders exist to sort images into
    for dir in subDirectoriesList:
        if not os.path.isdir(dir):
            os.mkdir(alphaDirectory)
        else: print("why")

    for image in os.listdir(mainDirectory):
        if (image.endswith(".png")): # checks if file in directory is a .png
            img = Image.open(mainDirectory + image)

            # gets the Alpha channel of an Image and checks how many differences there are, if 1 it has no transparency
            if len(img.getchannel("A").getcolors()) > 1:
                os.replace(mainDirectory + image, alphaDirectory + image)
            else:
                os.replace(mainDirectory + image, rgbDirectory + image)

alphaGrouping("./Textures/")