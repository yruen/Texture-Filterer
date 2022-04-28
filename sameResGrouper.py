# Group images by their resolution
import os
from PIL import Image

textureSizes = []

def sameTextureGrouping(mainDirectory):
    for image in os.listdir(mainDirectory):
        if (image.endswith(".png")):
            image = Image.open(mainDirectory+image)
            if image.size not in textureSizes:
                textureSizes.append(image.size)
            # Adds all the resolutions images are at to a list to compare them

    # creates directories named with the resolutions of images in directory (textureSizes list)
    for resolution in textureSizes:
        if not os.path.isdir(f"{mainDirectory}{str(resolution[0])}x{str(resolution[1])}/"):
            os.mkdir(f"{mainDirectory}{str(resolution[0])}x{str(resolution[1])}/")

    for image in os.listdir(mainDirectory):
        if (image.endswith(".png")):
            imagePil = Image.open(mainDirectory+image)
            for resolution in textureSizes:
                if imagePil.size == resolution:
                    os.replace(mainDirectory + image, f"{mainDirectory}{str(resolution[0])}x{str(resolution[1])}/{image}")
    return textureSizes