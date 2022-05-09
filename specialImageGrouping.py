# Special image separation
import os
from PIL import Image

# checks if the image is a Majoras mask 3D save file preview (doesn't need to be upscaled)
# Cropping dimensions for MM3D Savefile preview textures
                                                #left, top, right, bottom
def mm3d_savefile_grouping(directory, dimensions=(400, 0, 410, 10)):

    count = 0 # keeps track of how many images there are
    savefile_preview_dir = os.path.join(directory, "saveFilePreview")
    if not os.path.isdir(savefile_preview_dir):
        os.mkdir(savefile_preview_dir)

    image_list = [entry for entry in os.scandir(directory) if entry.name.endswith(".png")]
    for image in image_list:
        if Image.open(image.path).size == (512, 256):
                # Image is cropped to check if it's one color as is the case in mm3D's save file preview texture
                img_cropped = (Image.open(image.path).crop(dimensions))
                if len(img_cropped.getcolors()) == 1:
                    os.replace(image.path, os.path.join(savefile_preview_dir, image.name))
                    count+= 1
    return count