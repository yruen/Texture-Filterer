# Group images by their resolution
import os
from PIL import Image

def groupResolution(directory, res):
    count = 0
    if type(res) is not list: res = [res] # Makes this integrate with groupAllSameResolution()
    # For loop that gets files from directory and checks if they're PNGs
    images = [entry for entry in os.scandir(directory) if entry.name.endswith(".png")]

    for image in images:
        imagePIL = Image.open(image.path)
        for resolution in res:

            # Will group all images with the tuple resolution (recommended)
            if type(resolution) is tuple and imagePIL.size ==resolution:
                resDir = f"{directory}{resolution[0]}x{resolution[1]}/"
                # Checks if directory was created and if not will create one
                if not os.path.isdir(resDir): os.mkdir(resDir)
                os.replace(image.path, resDir+image.name)
                count += 1

            # If only an int was given, will combine all that have that resolution in either their width or length (not recommended)
            elif type(resolution) is int and (imagePIL.size[0]==resolution or imagePIL.size[1]==resolution):
                resDir = f"{directory}{resolution}/"
                # Checks if directory was created and if not will create one
                if not os.path.isdir(resDir): os.mkdir(resDir)
                os.replace(image.path, resDir+image.name)
                count += 1
    return count

def groupAllSameResolution(directory):
    imagesPILsizes = [Image.open(entry.path).size for entry in os.scandir(directory) if entry.name.endswith(".png")]
    # dictionary creations removes duplicate entries in list
    imagesPILsizes = list(dict.fromkeys(imagesPILsizes))
    return groupResolution(directory, imagesPILsizes)