#!/usr/bin/env python
import argparse
import os, sys

from sorting_scripts.imageDuplicateDetector import duplicate_sorter, secondary_passes
from sorting_scripts.basicSorters import alpha_grouping, group_all_same_resolution
from sorting_scripts.specialImageGrouping import mm3d_savefile_grouping
from other_scripts.otherUtils import mipmap_replacement, revert_sorting

command_options = ("Alpha (default)", "Resolution", "Image similarity (CPU intensive)", "Save file preview", "Extras")
extra_command_options = ("Mipmap replacement (DESTRUCTIVE!!!)", "Revert sorting (Run this in case you messed up using a sorthing algortihm;\n DOES NOT REVERT A DESTRUCTIVE UTIL)")
clear = "\x1b[m"
blue = "\x1b[34m"
red = "\x1b[31m"

sort_text = "Choose sorting mode:\n"

for count, option in enumerate(command_options):
    sort_text += f"{blue}[{count+1}]{clear} {option}\n"

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

sort_range = range(1, len(command_options)+1)  # number of sorting modes in a range
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

else:  # if neither, use default
    print(
        f"{red}no sorting mode! sorting using defalt alpha mode{clear}", file=sys.stderr
    )
    sort = 1

# Sorters
# All return the count of images sorted
if sort == 1:  # alpha
    # Group images by whether they have an alpha channel
    count = alpha_grouping(mainDirectory)
    print(f"{count[0]} images with alpha and {count[1]} images without alpha separated")

elif sort == 2:  # resolution
    # Group all images in a directory by their resolution
    print(group_all_same_resolution(mainDirectory), "images sorted according to their resolution")

elif sort == 3:  # Image similarity
    """
    Group images by similarity using ImageHash
    difference value determines how similar images must look; lower value means images have to look more similar
    hashSize value determines the complexity of the hashing; higher values means higher intensity = more CPU usage = takes longer
    adjust difference and hashSize values in relation with each other
    """
    print(f"{duplicate_sorter(mainDirectory)} similar images sorted")
    #print(secondary_passes(mainDirectory), "similar images in second pass sorted")

elif sort == 4:  # save file preview
    # mm3D save file preview separation
    print (mm3d_savefile_grouping(mainDirectory), "save file previews sorted")

elif sort == 5: # Extras menu
    extras_string = f"Extras menu\n"
    for count, option in enumerate(extra_command_options):
        extras_string += f"{blue}[{count+1}]{clear} {option}\n"

    print(extras_string)
    while True:
        try:
            extras_input = int(input(">>> "))
            if extras_input in range(1,len(extra_command_options)+1):
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

    for count, option in enumerate(extra_command_options):
        if extras_input == count+1:
            extras_input = option

    """
    Replace mipmaps with their high res counterparts by copying the high res image in a folder and overwriting lower-res images
    Expects that duplicate_sorter (image similarity) from imageDuplicateDetector has been run at least once
    Idea from Issue #8

    DESTRUCTIVE !!!! MAKE SURE TO HAVE A BACKUP IN THE EVENT THAT duplicate_sorter MESSED UP
    MAKE SURE YOU DID NOT SEPARATE BY ALPHA
    """
    if "Mipmap" in extras_input:
        import time
        print(f"Mipmap replacement is {red}destructive{clear}\nit works by copying the largest image in a subfolder\nand overwriting smaller images with no check for similarity\n\n{red}Make sure you have a backup of your images before using!!!!!{clear}", file=sys.stderr)
        time.sleep(3)
        print("To continue type 'Mipmap' or exit by doing Ctrl+C", file=sys.stderr)
        while True:
            try:
                user_input = input(f"{red}>>> {clear}")
                if user_input == "Mipmap":
                    print(f"{red}proceeding{clear}")
                    mipmap_replacement(mainDirectory)
                    break
                else:
                    print(
                        f"{red}Not 'Mipmap', to exit press Ctrl+C{clear}",
                        file=sys.stderr,
                    )
                    continue
            except (EOFError, KeyboardInterrupt):
                print()  # print newline so it doesn't mess up bash
                exit(1)
            break

    # Revert *sorting*, does not revert destructive utils
    elif "Revert" in extras_input:
        revert_sorting(mainDirectory)
        print("Placed images inside of folders outside")