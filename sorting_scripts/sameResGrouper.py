# Group images by their resolution
import os
from PIL import Image

def group_resolution(directory, res):
    count = 0
    if type(res) is not list: res = [res] # Makes this integrate with groupAllSameResolution()
    # For loop that gets files from directory and checks if they're PNGs
    image_list = [entry for entry in os.scandir(directory) if entry.name.endswith(".png")]

    for image in image_list:
        image_PIL = Image.open(image.path)
        for resolution in res:

            # Will group all images with the tuple resolution (recommended)
            if type(resolution) is tuple and image_PIL.size == resolution:
                resDir = os.path.join(directory, f"{resolution[0]}x{resolution[1]}")
                # Checks if directory exists and if not will create one
                if not os.path.isdir(resDir): os.mkdir(resDir)
                os.replace(image.path, os.path.join(resDir, image.name))
                count += 1

            # If only an int was given, will combine all that have that resolution in either their width or length (not recommended)
            elif type(resolution) is int and (image_PIL.size[0]==resolution or image_PIL.size[1]==resolution):
                resDir = os.path.join(directory, resolution)
                # Checks if directory exists and if not will create one
                if not os.path.isdir(resDir): os.mkdir(resDir)
                os.replace(image.path, os.path.join(resDir, image.name))
                count += 1
    return count

def group_all_same_resolution(directory):
    image_sizes = [Image.open(entry.path).size for entry in os.scandir(directory) if entry.name.endswith(".png")]
    # dictionary creation removes duplicate entries in list
    image_sizes = list(dict.fromkeys(image_sizes))
    return group_resolution(directory, image_sizes)