#!/usr/bin/env python
import argparse
import os, sys
from imageDuplicateDetector import duplicateSorter, secondPassDS
from sameResGrouper import groupAllSameResolution
from alphaValueGrouper import alphaGrouping
from specialImageGrouping import mm3dSaveFileGrouping

clear = "\x1b[m"
blue = "\x1b[34m"
red = "\x1b[31m"
sort_text = f"""Choose sorting mode:
        {blue}[1]{clear} Alpha (default)
        {blue}[2]{clear} Resolution
        {blue}[3]{clear} image similarity (CPU intensive)
        {blue}[4]{clear} Save file preview"""

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--texture-folder", metavar="FOLDER", dest="folder")
parser.add_argument("-s", "--sort-mode", metavar="INT", dest="sort", type=int, help=sort_text)
args = parser.parse_args()
del parser

if args.folder:
    mainDirectory = f"{args.folder}/"
else:
    mainDirectory = "./Textures/"
    print(
        f"{red}no folder specified! using default {mainDirectory}{clear}",
        file=sys.stderr,
    )


sort_range = range(1, 5)  # number of sorting modes (4 currently) in a range
if args.sort:
    if args.sort in sort_range:
        sort = args.sort
    else:
        print(f"{red}not a valid sorting method!{clear}", file=sys.stderr)
        exit(1)

elif os.isatty(1):  # if it's a interactive session, ask for it
    print(sort_text, file=sys.stderr)
    while True:
        try:
            sort = int(input(">>> "))
            if sort in sort_range:
                break
            else:
                print(
                    f"{red}not a valid sorting method! try again{clear}",
                    file=sys.stderr,
                )
                continue
        except ValueError as e:
            print(f"{red}{str(e)[40:]} not a number!{clear}", file=sys.stderr)
            continue
        except (EOFError, KeyboardInterrupt):
            print()  # print newline so it doesn't mess up bash
            exit(1)
        break

else: # if neither, use default
    print(f"{red}no sorting mode! sorting using defalt alpha mode{clear}", file=sys.stderr)
    sort = 1

# Sorters
# All return the count of images sorted
if sort == 1:  # alpha
    # Group images by their alpha channel
    alphaGrouping(mainDirectory)

elif sort == 2:  # resolution
    # Group all images in a directory by their resolution
    groupAllSameResolution(mainDirectory)

elif sort == 3:  # image similarity
    """
    Group images by similarity using ImageHash
    difference value determines how similar images must look; lower value means images have to look more similar
    hashSize value determines the complexity of the hashing; higher values means higher intensity = more CPU usage = takes longer
    adjust difference and hashSize values in relation with each other
    Set printOutput to True to see images being combined
    REPLACE WITH A PROGRESS BAR ?
    """
    duplicateSorter(mainDirectory)
    # secondPassDS(mainDirectory)

elif sort == 4:  # save file preview
    # mm3D save file preview separation
    mm3dSaveFileGrouping(mainDirectory)
