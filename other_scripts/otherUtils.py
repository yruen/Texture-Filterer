# Replace mipmaps with their high res counterparts by deleting lowres images and creating copies that are named the same
# Expected that duplicate_sorter from imageDuplicateDetector has been run at least once
# Idea from Issue #8

# DESTRUCTIVE !!!! MAKE SURE TO HAVE A BACKUP IN THE EVENT THAT duplicate_sorter MESSED UP
# MAKE SURE YOU DID NOT SEPARATE BY ALPHA
import os
from PIL import Image
import shutil # <----- USES SHUTIL FOR COPY FUNCTION

image_file_extensions = (".png", ".jpg")

def mipmapReplacement(directory):
    texture_dir = [[root, files] for root, dir, files in os.walk(directory, topdown=True)] # Uses os.walk to get all files and their subdirectories

    for dir, files_in_parent in texture_dir[1:]: # Cuts off the first entry in files because that is the main directory, not sub folders
        image_sizes = [Image.open(os.path.join(dir,image)).size for image in files_in_parent if image[-4:] in image_file_extensions] # gets all images and stores their resolution in a list

        for image in files_in_parent:
            if image[-4:] in image_file_extensions:
                if Image.open(os.path.join(dir, image)).size == max(image_sizes):
                    print(os.path.join(dir, image)) # Possibly remove this in the future or make it a toggle
                    for image2 in files_in_parent:
                        if image != image2:
                            shutil.copyfile(os.path.join(dir, image), os.path.join(dir, image2))

def revertSorting(directory):
    texture_dir = [[root, files] for root, dir, files in os.walk(directory, topdown=True)] # Uses os.walk to get all files and their subdirectories
    for dir, files_in_parent in texture_dir[1:]: # Cuts off the first entry in files because that is the main directory, not sub folders
        for image in files_in_parent:
            if image[-4:] in image_file_extensions:
                    print(os.path.join(dir, image)) # Status printing, maybe make optional
                    shutil.move(os.path.join(dir, image), os.path.join(directory, image)) # Moves all images outside into parent folder
        os.rmdir(dir) # Deletes empty folders