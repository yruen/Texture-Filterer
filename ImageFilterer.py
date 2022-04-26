# USE PILLOW TO SEPARATE TRANSPARENT IMAGES
from PIL import Image
import os
import imagehash

hashCheck = True # Enables the hash checking / Disables main filtering code (they conflict for now)

mainDirectory = "./Textures/"
alphaDirectory = "./Textures/alpha/"
rgbDirectory = "./Textures/RGB/"
deleteDirectory = "./Textures/delete/"
lowresDirectory = "./Textures/lowres/"

directoriesList = [mainDirectory, alphaDirectory, rgbDirectory, lowresDirectory, deleteDirectory]
resolutions = [16, 32, 64, 128, 256, 512, 1024] # resolutions of textures
# Cropping dimensions for MM3D Savefile preview textures
            #left, top, right, bottom
dimensions = (400, 0, 410, 10)

# Check if folders exist
for dir in directoriesList:
    if not os.path.isdir(dir) and not hashCheck:
        os.mkdir(alphaDirectory)

for image in os.listdir(mainDirectory):
    if (image.endswith(".png")) and not hashCheck:
        img = Image.open(mainDirectory + image)

        # gets the Alpha channel of an Image and checks how many differences there are, if 1 it has no transparency
        if len(img.getchannel("A").getcolors()) > 1:
            os.replace(mainDirectory + image, alphaDirectory + image)

        # checks if the image resolution is 256 x 512
        elif (img.size[0] * img.size[1]) == 256*512:
            img_cropped = (img.crop(dimensions))
            
            # checks how many colors there are in the cropped region to separate mm3d save file preview texture
            if len(img_cropped.getcolors()) == 1:
                os.replace(mainDirectory + image, deleteDirectory + image)
            else:
                os.replace(mainDirectory + image, rgbDirectory + image)

        # checks if image resolution is less than 16x16
        elif img.size[0] * img.size[1] <= 16^2:
            os.replace(mainDirectory + image, lowresDirectory + image)
        
        elif img.size[0] * img.size[1] > 16^2:
            os.replace(mainDirectory + image, rgbDirectory + image)

# TODO: #7 EXPORT HASHES TO TXT OR OTHER FORMAT TO NOT NEED TO KEEP CREATING HASHES

# Loop that adds to a 2D list
# imageDupList[0] is the first group of images
# imageDupList[0][0] should be the first image of which hashes are compared to
# imageDupList[0][1], [2], [3] etc should be the duplicates of the first image

singleImages = []
imageDupList = []
imageDupListTotal = []
imageList = []
difference = 18 # Higher value, groups less similar
                # lower value, groups more similar
hashSize = 12 # determines the "complexity"
printOutput = False

# Compare file hashes using Imagehash to find out duplicates and mipmaps
if hashCheck:
    filelist = [image for image in os.listdir(mainDirectory)]
    for file in filelist:
        if file.endswith(".png"):
            imageList.append(file)
    #filelist.reverse() # starting from higher res files might be better?
    
    for image in imageList:
        imageDupList = []
        imageList.remove(image)
        # Imagehash has multiple methods, refer to the documentary and try the one that works best for you
        # In testing against mm3D textures, phash with a difference of 18 and hash size of 12 worked the best with a few misses
        # crop_resistant_hash DOES NOT WORK AT ALL
        hash1 = imagehash.phash(Image.open(mainDirectory + image), hashSize)
        for image2 in imageList:
            hash2 = imagehash.phash(Image.open(mainDirectory + image2), hashSize)
            # The lower the number, the closer the images have to look to each other
            if hash1 - hash2 <difference:
                #numDuplicates += 1
                if image not in imageDupList:
                    imageDupList.append(image)
                if image2 not in imageDupList:
                    imageDupList.append(image2)
                imageList.remove(image2)
            #else:
            #    singleImages.append(image)
                    
        if imageDupList != []:
            if printOutput:
                print(imageDupList)
            for i in range(len(imageDupList)):
                duplicateDirectory = mainDirectory + imageDupList[0][0:-4] + "/"
                if not os.path.isdir(duplicateDirectory):
                    os.mkdir(duplicateDirectory)
                if os.path.exists(mainDirectory + imageDupList[0]):
                    os.replace(mainDirectory + imageDupList[0], duplicateDirectory + imageDupList[0])
                if image[i] != image[0]:
                    if os.path.exists(mainDirectory + imageDupList[i]):
                        os.replace(mainDirectory + imageDupList[i], duplicateDirectory + imageDupList[i])
    print("sorting done")