import os
from PIL import Image
import imagehash

count = 0 # keeps track of how many duplicate/similar images there are
singleImages = [] # maybe implement in future?
imageList = []


class CacheHash:
    def __init__(self, directory, cacheFile, hashSize: int):
        self.hashSize = hashSize
        self.directory = directory
        self.cache = {}

        cacheFile = f"{directory}/{cacheFile}"
        os.close(os.open(cacheFile, os.O_CREAT))  # create the file if it doesn't exist

        self.cacheFile = open(cacheFile, "r+t", encoding="utf-8")
        self.parse()

    def parse(self):
        self.cacheFile.seek(0)  # go to start of the file
        for line in self.cacheFile:
            try:
                (img, imghash) = line.split("\0")
                self.cache[img] = int(imghash, 16)
            except ValueError:
                continue  # if this line corrupt/broken, go to the next line

    def get_hash(self, img) -> int:
        """
        gets the hash of an image
        if the hash is on the cache, get it from there
        if not, calculate and put it on there
        """
        if img in self.cache:
            return self.cache[img]
        else:
            imghash = imagehash.phash(Image.open(self.directory + img), self.hashSize)
            self.cache[img] = imghash
            self.cacheFile.write(f"{img}\0{imghash}\n")
            return imghash


"""
difference value determines how similar images must look; lower value means images have to look more similar
hashSize value determines the complexity of the hashing; higher values means higher intensity = more CPU usage = takes longer
adjust difference and hashSize values in relation with each other
"""

# The default values chosen here are what worked best for grouping together higher resolution (32x32 and higher) mm3D textures
def duplicateSorter(
    directory,
    difference=18,
    hashSize=12,
    reverseVar=True,
    sort=True,
    printOutput=False,
    groupSingleImages=False,
):
    cache = CacheHash(directory, f".hash{hashSize}", hashSize)
    count = 0
    # For loop that gets files from directory and checks if they're PNGs
    imageList = [imagePath for imagePath in os.listdir(directory) if imagePath.endswith(".png")]
    if reverseVar: imageList.reverse() # starting from higher res files might be better?

    for image in imageList:
        imageDupList = []
        # Image is removed to reduce amount of images hashed
        imageList.remove(image)
        # Imagehash has multiple methods, refer to the documentation and experiment with the one that works best for you
        # In testing against mm3D textures, phash with a difference of 18 and hash size of 12 worked the best with a few misses
        hash1 = cache.get_hash(image)

        for image2 in imageList:
            hash2 = cache.get_hash(image2)
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

# This is a mess, needs severe optimization
def secondPassDS(directory):
    groupedImages = []
    # accumulates folders
    folders = [entry for entry in os.scandir(directory) if entry.is_dir()]

    for folder in folders:
        #imagesAtLowestRes = [Image.open(image.path).size for image in os.scandir(folder.path)]
        for image in os.scandir(folder.path):
            groupedImages.append(Image.open(image.path).size)
            lowestRes = min(groupedImages)
            #print(lowestRes)
            for image1 in groupedImages:
                if lowestRes == image1:
                    lowResImageHash = imagehash.phash(Image.open(image.path))

                    for imageRoot in os.scandir(directory):
                        if not imageRoot.is_dir():
                            rootImageHash = imagehash.phash(Image.open(imageRoot.path))
                            if lowResImageHash - rootImageHash <10:
                                if not os.path.isfile(image.path[:len(image.name)]+"/"+imageRoot.name):
                                    if os.path.isfile("./Textures/"+imageRoot.name):
                                        # Needs optimization, checks files multiple times
                                        print(image.path[:len(image.name)], imageRoot.path)
                                        print(image.path[:len(image.name)]+"/"+imageRoot.name)
                                        try:
                                            os.replace(imageRoot.path, image.path[:len(image.name)]+"/"+imageRoot.name)
                                        except:
                                            None

    #1. Access one folder in list
    #2. Get smallest image (size wise) in folder with min(list)
    #3. Compare smallest image ONLY hash with other images in root of ./Textures/
    #4. Move hashes that match under a certain value to the other directory