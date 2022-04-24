# USE PILLOW TO SEPARATE TRANSPARENT IMAGES
from PIL import Image
import imagehash
import os

hashCheck = True # Enables the hash checking / Disables main filtering code (they conflict for now)
addCount = 0 #keeps track of how many duplicates there are

mainDirectory = "./Textures/"
alphaDirectory = "./Textures/alpha/"
rgbDirectory = "./Textures/RGB/"
deleteDirectory = "./Textures/delete/"
lowresDirectory = "./Textures/lowres/"

directoriesList = [mainDirectory, alphaDirectory, rgbDirectory, lowresDirectory, deleteDirectory]
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

# TODO: #7 EXPORT HASHES TO TXT OR OTHER FORMAT TO NOT NEED TO KEEP CREATING HASHES
imageList = []
if hashCheck:
    # Compare file hashes using Imageahsh to find out duplicates and mipmaps
    imageList = [image for image in os.listdir(mainDirectory)]
    for image in os.listdir(mainDirectory):
        # phash stands for perceptual hashing, there are other modes you can experiment with
        hash1 = imagehash.phash(Image.open(mainDirectory + image))
        imageList.remove(image) # Removes image hashed from directory, preventing duplicate checking
        for image2 in imageList:
            hash2 = imagehash.phash(Image.open(mainDirectory + image2))
            # The lower the number, the closer the images have to look to each other
            if hash1 - hash2 <10:
                print(f"{mainDirectory + image} is very similar to {mainDirectory+image2}")
                addCount += 1
    print(addCount)