import os
from PIL import Image
import imagehash

count = 0 # keeps track of how many duplicate/similar images there are
singleImages = [] # maybe implement in future?
imageList = []

# TODO: #7 EXPORT HASHES TO TXT OR OTHER FORMAT TO NOT NEED TO KEEP CREATING HASHES

"""
difference value determines how similar images must look; lower value means images have to look more similar
hashSize value determines the complexity of the hashing; higher values means higher intensity = more CPU usage = takes longer
adjust difference and hashSize values in relation with each other
"""

# The default values choosen here are what worked best for grouping together higher resolution (32x32 and higher) mm3D textures
def duplicate_sorter(directory, difference=18, hashSize=12, reverseVar=True, sort=True, printOutput=False, groupSingleImages=False):
    count = 0
    # For loop that gets files from directory and checks if they're PNGs
    imageList = [imagePath for imagePath in os.listdir(directory) if imagePath.endswith(".png")]
    if reverseVar: imageList.reverse() # starting from higher res files might be better?

    for image in imageList:
        imageDupList = []

        imageList.remove(image) # Image is removed to reduce amount of images hashed
        # Imagehash has multiple methods, refer to the documentation and experiment with the one that works best for you
        # In testing against mm3D textures, phash with a difference of 18 and hash size of 12 worked the best with a few misses
        hash1 = imagehash.phash(Image.open(directory + image), hashSize)
        for image2 in imageList:
            hash2 = imagehash.phash(Image.open(directory + image2), hashSize)
            # The lower the difference value, the closer the images have to look to each other
            if hash1 - hash2 <difference:
                #numDuplicates += 1
                if image not in imageDupList:
                    imageDupList.append(image)
                if image2 not in imageDupList:
                    imageDupList.append(image2)

                imageList.remove(image2)

        #if groupSingleImages:
        #    singleImages.append(image)

        if sort:
            if imageDupList != [] and type(imageDupList) is list:
                count += 1
                if printOutput: print(imageDupList)
                for i in range(len(imageDupList)):
                    duplicateDirectory = directory + imageDupList[0][0:-4] + "/"
                    if not os.path.isdir(duplicateDirectory):
                        os.mkdir(duplicateDirectory)
                    if os.path.exists(directory + imageDupList[0]):
                        os.replace(directory + imageDupList[0], duplicateDirectory + imageDupList[0])
                    if image[i] != image[0]:
                        if os.path.exists(directory + imageDupList[i]):
                            os.replace(directory + imageDupList[i], duplicateDirectory + imageDupList[i])
    return count


def secondary_passes(directory, difference=10, hash_size=8):
    files = [[root, files] for root, dir, files in os.walk(directory, topdown=True)] # Uses os.walk to get all files and their subdirectories
    mainDirectory = [entry for entry in os.scandir(directory) if entry.name.endswith(".png")] # Gets only .pngs of mainDirectory
    for parent_dir, files_in_parent in files[1:]: # Cuts off the first entry in files because that is the main directory, not sub folders
        lowres_images = []

        image_sizes = [Image.open(os.path.join(parent_dir,image)).size for image in files_in_parent]
        image_paths = [image for image in files_in_parent]

        for image in image_paths:
            if Image.open(os.path.join(parent_dir, image)).size == min(image_sizes):
                lowres_images.append(image)

        for image_in_mainDirectory in mainDirectory:
            try:
                if imagehash.phash(Image.open(os.path.join(parent_dir, lowres_images[0])), hash_size) - imagehash.phash(Image.open(image_in_mainDirectory.path), hash_size) < difference:
                    print(os.path.join(parent_dir, lowres_images[0]), image_in_mainDirectory.path)
                    os.replace(image_in_mainDirectory.path, os.path.join(parent_dir, image_in_mainDirectory.name))
            except:
                None