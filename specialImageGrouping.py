# Special image separation
import os
from PIL import Image

# checks if the image is a Majoras mask 3D save file preview (doesn't need to be upscaled)
# Cropping dimensions for MM3D Savefile preview textures
                                                #left, top, right, bottom
def mm3dSaveFileGrouping(directory, dimensions=(400, 0, 410, 10)):
    count = 0 # keeps track of how many images there are
    saveFilePreviewDir = directory + "saveFilePreview/"
    if not os.path.isdir(saveFilePreviewDir):
        os.mkdir(saveFilePreviewDir)
    for image in os.listdir(directory):
        if (image.endswith(".png")):
            if Image.open(directory+image).size == (512, 256):
                # Image is cropped to check if it's one color as is the case in mm3D's save file preview texture
                img_cropped = (Image.open(directory+image).crop(dimensions))
                if len(img_cropped.getcolors()) == 1:
                    os.replace(directory + image, saveFilePreviewDir + image)
                    count+= 1
    return count