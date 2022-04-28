import os
from PIL import Image
import imagehash

singleImages = [] # maybe implement in future?
imageList = []

# TODO: #7 EXPORT HASHES TO TXT OR OTHER FORMAT TO NOT NEED TO KEEP CREATING HASHES

"""
difference value determines how similar images must look; lower value means images have to look more similar
hashSize value determines the complexity of the hashing; higher values means higher intensity = more CPU usage = takes longer
adjust difference and hashSize values in relation with each other
"""

# The default values choosen here are what worked best for grouping together higher resolution (32x32 and higher) mm3D textures
def duplicateSorter(directory, difference=18, hashSize=12, reverseVar=True, sort=True, printOutput=False, groupSingleImages=False):
    # filelist creation for loop
    filelist = [image for image in os.listdir(directory)]
    for file in filelist:
        if file.endswith(".png"): imageList.append(file)
    if reverseVar: filelist.reverse() # starting from higher res files might be better?

    for image in imageList:
        imageDupList = []
        imageList.remove(image)
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