import argparse
from PIL import Image
import os

from imageDuplicateDetector import duplicateSorter
from sameResGrouper import sameTextureGrouping
from alphaValueGrouper import alphaGrouping

hashCheck = True # Enables the hash checking / Disables main filtering code (they conflict for now)

def get_texture_dir():
    """
    Tries to get main textures folder from argument
    Could be converted into a "parse_args" function if more arguments ever needed
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--texture-folder",
        metavar="FOLDER",
    )
    args = parser.parse_args()

    if args.texture_folder:
        return f"{args.texture_folder}/"
    else:
        return "./Textures/"

mainDirectory = get_texture_dir()
alphaDirectory = f"{mainDirectory}alpha/"
rgbDirectory = f"{mainDirectory}RGB/"

directoriesList = [
    mainDirectory,
    alphaDirectory,
    rgbDirectory,
]

# Cropping dimensions for MM3D Savefile preview textures
            #left, top, right, bottom
dimensions = (400, 0, 410, 10)

# TODO: Implement this code with the new module system
# checks if the image resolution is 256 x 512
#if (img.size[0] * img.size[1]) == 256*512:
#    img_cropped = (img.crop(dimensions))
#
#    # checks how many colors there are in the cropped region to separate mm3d save file preview texture
#    if len(img_cropped.getcolors()) == 1:
#        os.replace(mainDirectory + image, deleteDirectory + image)
#    else:
#       os.replace(mainDirectory + image, rgbDirectory + image)

# Sorters

"""
Group images by similarity using ImageHash
difference value determines how similar images must look; lower value means images have to look more similar
hashSize value determines the complexity of the hashing; higher values means higher intensity = more CPU usage = takes longer
adjust difference and hashSize values in relation with each other
Set printOutput to True to see images being combined REPLACE WITH A PROGRESS BAR ?
"""
if hashCheck:
    duplicateSorter(mainDirectory, difference=18, hashSize=12, printOutput=False)
    print("Done")

# Group images by their resolution
sameTextureGrouping(mainDirectory)

# Group images by their alpha channel
alphaGrouping(mainDirectory)