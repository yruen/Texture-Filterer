# Replace mipmaps with their high res counterparts by deleting lowres images and creating copies that are named the same
# Expected that duplicate_sorter from imageDuplicateDetector has been run at least once
# Idea from Issue #8

# DESTRUCTIVE !!!! MAKE SURE TO HAVE A BACKUP IN THE EVENT THAT duplicate_sorter MESSED UP,
import os
from PIL import Image
import shutil

directory = "./Textures/"
def main():
    files = [[root, files] for root, dir, files in os.walk(directory, topdown=True)] # Uses os.walk to get all files and their subdirectories

    for parent_dir, files_in_parent in files[1:]: # Cuts off the first entry in files because that is the main directory, not sub folders

        image_sizes = [Image.open(os.path.join(parent_dir,image)).size for image in files_in_parent]
        image_in_folders = [image for image in files_in_parent if image.endswith(".png")]

        for image in image_in_folders:
            if Image.open(os.path.join(parent_dir, image)).size == max(image_sizes):
                print(os.path.join(parent_dir, image))
                for image2 in image_in_folders:
                    if image != image2:
                        shutil.copyfile(os.path.join(parent_dir, image), os.path.join(parent_dir, image2))

main()