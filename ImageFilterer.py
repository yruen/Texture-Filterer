#!/usr/bin/env python
import argparse

from imageDuplicateDetector import duplicateSorter, secondPassDS
from sameResGrouper import groupResolution, groupAllSameResolution
from alphaValueGrouper import alphaGrouping
from specialImageGrouping import mm3dSaveFileGrouping

hashCheck = False # Enables the hash checking, disabled by default because it is CPU intensive


parser = argparse.ArgumentParser()
parser.add_argument(
    "-t",
    "--texture-folder",
    metavar="FOLDER",
)
args = parser.parse_args()
del parser

if args.texture_folder:
    mainDirectory = f"{args.texture_folder}/"
else:
    mainDirectory = "./Textures/"

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
    duplicateSorter(mainDirectory)
    #secondPassDS(mainDirectory)
    #duplicateSorter(mainDirectory, difference=8, hashSize=12, printOutput=False)
    #print("Done")

# Group all images in a directory by their resolution
#groupAllSameResolution(mainDirectory)

# Group images by a given resolution, tuples are prefered
#groupResolution(mainDirectory, (16,16))

# Group images by their alpha channel
#alphaGrouping(mainDirectory)