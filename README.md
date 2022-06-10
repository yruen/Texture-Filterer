# Texture Filter
This is a Python script designed to sort textures dumped from **Majoras Mask 3D** (but can be modified to different types of texture) to aid upscaling and texture pack creation. It primarily uses Pillow, [ImageHash](https://pypi.org/project/ImageHash/) (for image similarity checking) and [tqdm](https://pypi.org/project/tqdm/) (for the progress bars)

### The sorting modes do NOT work with each other all the same time
Due to the way images are organized into folders as of this moment you may only choose one sorting method<br/>
You can use one sorting method and specify a directory created from using another sorting method

## The script can currently group images by:
1. Alpha and RGB
2. Resolution
3. Similarity with Imagehash (useful for mipmaps)
4. mm3D save file preview

## Can also:
1. Replace lowres mipmaps with their high res counterparts (destructive)

## Planned:
1. Computer Vision sorting (Tensorflow powered)

## USAGE:
```
python ImageFilterer.py -t FOLDER -s SORTING_MODE
  -t / --texture-folder      Specify the folder in which your textures are located, if none set to "./Textures/"
  -s / --sort-mode           Choose how to sort/group images with an INT corresponding to the previously listed methods (Ex: 2 = Resolution sorting)
```
Also has a kinda interactive UI by running ImageFilterer.py only (texture-folder defaults to "./Textures/" if not specified
### IF ON WINDOWS
Please use Powershell for proper GUI on terminal; CMD does not support Unicode escapes (?)
