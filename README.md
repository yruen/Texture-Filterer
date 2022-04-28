# Texture Filter
This is a Python script designed to sort textures dumped from **Majoras Mask 3D** to aid upscaling and texture pack creation
It primarily uses Pillow and ImageHash
## The sorting modes do NOT work with each other all the same time
Due to the way images are organized into folders as of this moment you may only choose one sorting method
You can also use one sorting method and specific the directory to one folder

## The script can currently group images by:
1. Alpha and RGB
2. Resolution
3. Similarity with Imagehash (useful for mipmaps)

## Will do in the future:
1. Replace lowres mipmaps with their high res counterparts
2. Computer Vision sorting (Tensorflow powered)
