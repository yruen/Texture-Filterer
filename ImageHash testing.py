# ImageHash testing
from PIL import Image
import imagehash

window8 = "./Textures/tex1_8x8_C27F2DD33C3BC899_13.png"
window16 = "./Textures/tex1_16x16_7CC65FBDF0E7CA51_13.png"

result =imagehash.phash(Image.open(window8)) - imagehash.phash(Image.open(window16))
print(result)