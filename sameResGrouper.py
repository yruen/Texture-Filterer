# Group images by their resolution
import os
from PIL import Image

totalTextureSizeDirs = []
textureSizes = []

def sameSizeGrouping(mainDirectory):
    for image in os.listdir(mainDirectory):
        if (image.endswith(".png")):
            image = Image.open(mainDirectory+image)
            if image.size not in textureSizes:
                textureSizes.append(image.size)
            # Adds all the resolutions images are at to a list to compare them

    # creates directories named with the resolutions of images in directory (textureSizes list)
    for resolution in textureSizes:
        textureSizeDir = f"{mainDirectory}{str(resolution[0])}x{str(resolution[1])}/"
        if not os.path.isdir(textureSizeDir):
            os.mkdir(textureSizeDir)
            totalTextureSizeDirs.append(textureSizeDir)

    for image in os.listdir(mainDirectory):
        if (image.endswith(".png")):
            imagePil = Image.open(mainDirectory+image)
            for resolution in textureSizes:
                if imagePil.size == resolution:
                    os.replace(mainDirectory + image, f"{mainDirectory}{str(resolution[0])}x{str(resolution[1])}/{image}")
    return textureSizes, totalTextureSizeDirs