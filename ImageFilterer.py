# USE PILLOW TO SEPARATE TRANSPARENT IMAGES
from PIL import Image
import os
from imageDuplicateDetector import duplicateSorter

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

duplicateSorter(mainDirectory, printOutput=True)