# USE PILLOW TO SEPARATE TRANSPARENT IMAGES
from PIL import Image
import os

mainDirectory = os.listdir("./Textures/")
alphaDirectory = "./Textures/alpha/"
rgbDirectory = "./Textures/RGB/"
deleteDirectory = "./Textures/delete"

left = 400
right = 512
top = 0
bottom = 256

for image in mainDirectory:
    if (image.endswith(".png")):
        img = Image.open(f"./Textures/{image}")
        data = img.getdata()
        a = [(0, 0, 0, d[3]) for d in data] #GETS ALPHA CHANNEL DATA, MIGHT REPLACE WITH getchannel("A") ONCE FIGURED OUT
        img.putdata(a)
        if img.getextrema()[3][0] == 0:
            os.replace("./Textures/" + image, alphaDirectory + image)
        elif (img.size[0] + img.size[1]) >512:
            if (img.crop((left, top, right, bottom))).getcolors[0][0] == 28672:
                os.replace("./Textures/" + image, deleteDirectory + image)
        else:
            os.replace("./Textures/" + image, rgbDirectory + image)

# https://coderslegacy.com/python/pillow-crop-images/

 
# new_img = img.crop((left, top, right, bottom))
# new_img.show()
testImage = Image.open("/home/acer/Downloads/tex1_512x256_EB116B54EEDA84E0_3.png")
# testImage.show()
cropped = testImage.crop((left, top, right, bottom))
#cropped.show()
# l = (cropped.getchannel("A")).getdata()
print(cropped.getcolors()[0][0])
print(cropped.size)
# cropped.save("test.png")

          #  cropped = img.crop((left, top, right, bottom))
          #  if cropped.getcolors()[0][0] == 28672:
          #      None