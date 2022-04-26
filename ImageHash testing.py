# ImageHash testing
from PIL import Image
import imagehash

#image1 = "/home/acer/Documents/Github/Texture-Filterer/Textures/tex1_128x128_01F06373B35754D9_12/tex1_128x128_01F06373B35754D9_12.png"
image2 = "/home/acer/Documents/Github/Texture-Filterer/Textures/tex1_16x16_7CC65FBDF0E7CA51_13.png"
image3 = "/home/acer/Documents/Github/Texture-Filterer/Textures/tex1_8x8_C27F2DD33C3BC899_13.png"

#result1 =imagehash.phash(Image.open(image1), 12) - imagehash.phash(Image.open(image2), 12)
#print(result1)
result2 =imagehash.phash(Image.open(image2), 8) - imagehash.phash(Image.open(image3), 8)
print(result2)