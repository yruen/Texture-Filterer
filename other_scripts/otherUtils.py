import os
from PIL import Image
import shutil

image_file_extensions = (".png", ".jpg")

"""
Replace mipmaps with their high res counterparts by copying the high res image in a folder and overwriting lower-res images
Expected that duplicate_sorter from imageDuplicateDetector has been run at least once
Idea from Issue #8

DESTRUCTIVE !!!! MAKE SURE TO HAVE A BACKUP IN THE EVENT THAT duplicate_sorter MESSED UP
MAKE SURE YOU ONLY SEPARATED BY IMAGE SIMILARITY BEFORE RUNNING
"""
def mipmap_replacement(directory):
    texture_dir = [[root, files] for root, dir, files in os.walk(directory, topdown=True)] # Uses os.walk to get all files and their subdirectories

    for dir, files_in_parent in texture_dir[1:]: # Cuts off the first entry in files because that is the main directory, not sub folders
        image_sizes = [Image.open(os.path.join(dir,image)).size for image in files_in_parent if image[-4:] in image_file_extensions] # gets all images and stores their resolution in a list

        for image in files_in_parent:
            if image[-4:] in image_file_extensions:
                if Image.open(os.path.join(dir, image)).size == max(image_sizes): # Gets the largest image size
                    #print(os.path.join(dir, image)) # maybe incorporate later
                    for image2 in files_in_parent:
                        if image != image2:
                            shutil.copyfile(os.path.join(dir, image), os.path.join(dir, image2))

# Revert *sorting*, does not revert destructive utils
def revert_sorting(directory):
    texture_dir = [[root, files] for root, dir, files in os.walk(directory, topdown=True)] # Uses os.walk to get all files and their subdirectories
    for dir, files_in_parent in texture_dir[1:]: # Cuts off the first entry in files because that is the main directory, not sub folders
        for image in files_in_parent:
            if image[-4:] in image_file_extensions:
                    #print(os.path.join(dir, image)) # maybe incorporate later
                    shutil.move(os.path.join(dir, image), os.path.join(directory, image)) # Moves all images outside into parent folder

        # Tries code so one folder with non-images doesn't stop the whole thing
        try:
            os.rmdir(dir) # For deleting empty folders
        except OSError as e:
            if "39" in str(e):
                print(f"{e}, skipping")
            else:
                print(e)