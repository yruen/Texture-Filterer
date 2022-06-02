# ImageHash testing
# Use to quickly test the effectiveness of an algorithm in comparison of two images
# Does not affect functionality of main code
import argparse
from PIL import Image
import imagehash
parser = argparse.ArgumentParser()
parser.add_argument(
    "-t",
    "--texture-folder",
    metavar="FOLDER",
)
args = parser.parse_args()

if args.texture_folder:
    texture_dir = f"{args.texture_folder}/"
else:
    texture_dir = "./Textures/"

hashSize = 12
print(imagehash.average_hash(Image.open(f"{texture_dir}tex1_8x8_C27F2DD33C3BC899_13.png"), hashSize) - imagehash.average_hash(Image.open(f"{texture_dir}tex1_16x16_7CC65FBDF0E7CA51_13.png"), hashSize))
print(imagehash.average_hash(Image.open(""), hashSize) - imagehash.average_hash(Image.open(f"{texture_dir}tex1_16x32_6C09147B1C7C11F3_12/tex1_128x256_ABD856CB8AF093EE_12.png"), hashSize))
print(imagehash.average_hash(Image.open(f"{texture_dir}tex1_16x32_6C09147B1C7C11F3_12/tex1_16x32_6C09147B1C7C11F3_12.png"), hashSize) - imagehash.average_hash(Image.open(f"{texture_dir}tex1_16x16_7CC65FBDF0E7CA51_13.png"), hashSize))
