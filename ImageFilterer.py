# USE PILLOW TO SEPARATE TRANSPARENT IMAGES
from PIL import Image
import imagehash
import os

hashCheck = True

mainDirectory = "./Textures/"
alphaDirectory = "./Textures/alpha/"
rgbDirectory = "./Textures/RGB/"
deleteDirectory = "./Textures/delete/"
lowresDirectory = "./Textures/lowres/"

directoriesList = [mainDirectory, alphaDirectory, rgbDirectory, lowresDirectory, deleteDirectory]
# Cropping dimensions for MM3D Savefile preview textures
dimensions = (400, 0, 410, 10)
            #left, top, right, bottom
# Check if folders exist
for dir in directoriesList:
    if not os.path.isdir(dir):
        os.mkdir(alphaDirectory)

for image in os.listdir(mainDirectory):
    if (image.endswith(".png")):
        img = Image.open(mainDirectory + image)

        # gets the Alpha channel of an Image and checks how many differences there are, if 1 it has no transparency
        if len(img.getchannel("A").getcolors()) > 1:
            os.replace("./Textures/" + image, alphaDirectory + image)

        # checks if the image resolution is 256 x 512
        elif (img.size[0] * img.size[1]) == 256*512:
            img_cropped = (img.crop(dimensions))
            
            # checks how many colors there are in the cropped region to separate mm3d save file texture
            if len(img_cropped.getcolors()) == 1:
                os.replace("./Textures/" + image, deleteDirectory + image)
            else:
                os.replace("./Textures/" + image, rgbDirectory + image)

        # checks if image resolution is less than 16x16
        elif img.size[0] * img.size[1] <= 16^2:
            os.replace("./Textures/" + image, lowresDirectory + image)
        
        elif img.size[0] * img.size[1] > 16^2:
            os.replace("./Textures/" + image, rgbDirectory + image)

# Find a way to link filenames with hashes
# Possibly 2D list? 
# Ex: hashGroup[0] = [2020ffffff202020, filename.png]
if hashCheck:
    hashGroup = [[str(imagehash.average_hash(Image.open(lowresDirectory + image))), lowresDirectory + image] for image in os.listdir(lowresDirectory)]
        # print([str(imagehash.average_hash(Image.open(lowresDirectory + image)))])
    print(hashGroup[0])