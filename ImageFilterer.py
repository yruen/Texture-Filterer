# USE PILLOW TO SEPARATE TRANSPARENT IMAGES
from PIL import Image
import os

mainDirectory = os.listdir("./Textures/")
alphaDirectory = "./Textures/alpha/"
rgbDirectory = "./Textures/RGB/"
deleteDirectory = "./Textures/delete/"

# Cropping dimensions for MM3D Savefile preview textures
# https://coderslegacy.com/python/pillow-crop-images/
left = 400
right = 512
top = 0
bottom = 256

for image in mainDirectory:
    if (image.endswith(".png")):
        img = Image.open(f"./Textures/{image}")

        # gets the Alpha channel of an Image and checks how many differences there are, if 1 it has no transparency
        if len(img.getchannel("A").getcolors()) > 1:
            os.replace("./Textures/" + image, alphaDirectory + image)

        # checks if the image resolution is 131072 (the result of 256 x 512)
        elif (img.size[0] * img.size[1]) == 131072:
            img_cropped = (img.crop((left, top, right, bottom)))

            # checks if the area color (outside the 400x240 3ds screen area) is 28672
            if img_cropped.getcolors()[0][0] == 28672:
               os.replace("./Textures/" + image, deleteDirectory + image)
            else:
                os.replace("./Textures/" + image, rgbDirectory + image)

        else:
            os.replace("./Textures/" + image, rgbDirectory + image)