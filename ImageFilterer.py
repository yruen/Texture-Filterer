#!/usr/bin/env python
import argparse

from imageDuplicateDetector import duplicate_sorter
from sameResGrouper import group_resolution, group_all_same_resolution
from alphaValueGrouper import alphaGrouping
from specialImageGrouping import mm3dSaveFileGrouping

hashCheck = True # Enables the hash checking, disabled by default because it is CPU intensive

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

# Sorters
# All return the count of images sorted

# mm3D save file preview separation
#print(mm3dSaveFileGrouping(mainDirectory))

"""
Group images by similarity using ImageHash
difference value determines how similar images must look; lower value means images have to look more similar
hashSize value determines the complexity of the hashing; higher values means higher intensity = more CPU usage = takes longer
adjust difference and hashSize values in relation with each other
Set printOutput to True to see images being combined 
REPLACE WITH A PROGRESS BAR ?
"""

if hashCheck:
    duplicate_sorter(mainDirectory)
    #secondPassDS(mainDirectory)
    #duplicateSorter(mainDirectory, difference=8, hashSize=12, printOutput=False)
    #print("Done")

# Group all images in a directory by their resolution
#groupAllSameResolution(mainDirectory)

# Group images by a given resolution, tuples are prefered
#group_resolution(mainDirectory, (16,16))

# Group images by their alpha channel
#alphaGrouping(mainDirectory)