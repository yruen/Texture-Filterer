#!/usr/bin/env python
import argparse

from imageDuplicateDetector import duplicateSorter
from sameResGrouper import sameSizeGrouping
from alphaValueGrouper import alphaGrouping
from specialImageGrouping import mm3dSaveFileGrouping

hashCheck = False # Enables the hash checking, disabled by default because it is CPU intensive

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

# mm3D save file preview separation
# returns number of images
#print(mm3dSaveFileGrouping(mainDirectory))

"""
Group images by similarity using ImageHash
Returns number of duplicate images
difference value determines how similar images must look; lower value means images have to look more similar
hashSize value determines the complexity of the hashing; higher values means higher intensity = more CPU usage = takes longer
adjust difference and hashSize values in relation with each other
Set printOutput to True to see images being combined 
REPLACE WITH A PROGRESS BAR ?
"""
if hashCheck:
    duplicateSorter(mainDirectory, difference=18, hashSize=12, printOutput=False)
    print("Done")

# Group images by their resolution
# Returns the list of resolutions + texture directories in 2D array
#sameSizeGrouping(mainDirectory)

# Group images by their alpha channel
alphaGrouping(mainDirectory)