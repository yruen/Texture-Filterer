# Group images by their resolution
import os
from PIL import Image

def groupResolution(mainDirectory, res):
    count = 0
    tracker = -1
    if type(res) is not list: res = [res] # Makes this integrate with groupAllSameResolution()
    # For loop that gets files from directory, checks if they're PNGs and makes them PIL instances
    imagesPIL = [Image.open(mainDirectory + imagePath) for imagePath in os.listdir(mainDirectory) if imagePath.endswith(".png")]

    for imagePIL in imagesPIL:
        if len(res) > 1:
            tracker += 1 # maybe kinda lazy fix for integration with groupAllSameResolution()
            # doing a "for res in res" was not working well

        # Will group all images with the tuple resolution (recommended)
        if type(res[tracker]) is tuple and imagePIL.size ==res[tracker]:
            resDir = f"{mainDirectory}{res[tracker][0]}x{res[tracker][1]}/"
            # Checks if directory was created and if not will create one
            if not os.path.isdir(resDir): os.mkdir(resDir)
            os.replace(imagePIL.filename, resDir+imagePIL.filename[len(mainDirectory):])
            count += 1

        # If only an int was given, will combine all that have that resolution in either their width or length (not recommended)
        elif type(res[tracker]) is int and (imagePIL.size[0]==res[tracker] or imagePIL.size[1]==res[tracker]):
            resDir = f"{mainDirectory}{res[tracker]}/"
            # Checks if directory was created and if not will create one
            if not os.path.isdir(resDir): os.mkdir(resDir)
            os.replace(imagePIL.filename, resDir+imagePIL.filename[len(mainDirectory):])
            count += 1
    return count

def groupAllSameResolution(mainDirectory):
    imagesPILsizes = [Image.open(mainDirectory + imagePath).size for imagePath in os.listdir(mainDirectory) if imagePath.endswith(".png")]
    return groupResolution(mainDirectory, imagesPILsizes)