# USE PILLOW TO SEPARATE TRANSPARENT IMAGES
from PIL import Image
import imagehash
import os

hashCheck = True # Enables the hash checking / Disables main filtering code (they conflict for now)
numImagePairs = 0 #keeps track of how many duplicate pairs there are
tracker = -1 #keeps track of how many times the outer loop has been executed

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
            
            # checks how many colors there are in the cropped region to separate mm3d save file texture
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
if hashCheck:
    # Compare file hashes using Imageahsh to find out duplicates and mipmaps
    filelist = [image for image in os.listdir(mainDirectory)]
    for file in filelist:
        if file.endswith(".png"):
            imageList.append(file)

    for image in imageList:
        imageDupList = []
        imageList.remove(image)
        # phash stands for perceptual hashing, there are other modes you can experiment with
        hash1 = imagehash.phash(Image.open(mainDirectory + image))
        for image2 in imageList:
            hash2 = imagehash.phash(Image.open(mainDirectory + image2))
            # The lower the number, the closer the images have to look to each other
            if hash1 - hash2 <15:
                if image not in imageDupList:
                    imageDupList.append(image)
                    #print(f"{mainDirectory + image} is very similar to {mainDirectory+image2}")
                if image2 not in imageDupList:
                    imageDupList.append(image2)
                #imageList.remove(image2) # Removes mainDirectory image hashed from directory, preventing duplicate checking
            else:
                singleImages.append(image)
                    
        #print(imageDupList)
        if imageDupList != []:
            imageDupListTotal.append(imageDupList)

    print("Hash checking done")
    for image in imageDupListTotal:
        #print(image)
        if isinstance(image, list):
            for image in image:
                print(image)
            #duplicateDirectory = mainDirectory + image[0][0:-4] + "/"
            #if not os.path.isdir(duplicateDirectory):
            #    os.mkdir(duplicateDirectory)
            #os.replace(mainDirectory + image, duplicateDirectory + image)
        else:
            duplicateDirectory = mainDirectory + image[0][0:-4] + "/"
            if not os.path.isdir(duplicateDirectory):
                os.mkdir(duplicateDirectory)
            os.replace(mainDirectory + image[0], duplicateDirectory + image[0])
            for dupImage in image:
                if dupImage != image[0]:
                    os.replace(mainDirectory + dupImage, duplicateDirectory + dupImage)