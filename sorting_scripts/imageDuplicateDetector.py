import os
from PIL import Image
import imagehash


class CacheHash:
    def __init__(self, directory, cacheFile, hash_size: int):
        self.hash_size = hash_size
        self.directory = directory
        self.cache = {}
        # Usage of os.path.join prevents errors from input having an extra slash ex: input is /directory/ rather than /directory
        cacheFile = os.path.join(directory, cacheFile)

        self.cacheFile = open(cacheFile, "a+t", encoding="utf-8")
        self.parse()

    def __del__(self):
        self.cacheFile.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.__del__()

    def parse(self):
        self.cacheFile.seek(0)  # go to start of the file
        for line in self.cacheFile:
            try:
                (img, imghash) = line.split("\0")
                self.cache[img] = imagehash.hex_to_hash(imghash)
            except ValueError:
                continue  # if this line corrupt/broken, go to the next line

    def get_hash(self, img) -> imagehash.ImageHash:
        """
        gets the hash of an image
        if the hash is on the cache, get it from there
        if not, calculate and put it on there
        """
        if img in self.cache:
            return self.cache[img]
        else:
            imghash = imagehash.phash(Image.open(img), self.hash_size)
            self.cache[img] = imghash
            self.cacheFile.write(f"{img}\0{imghash}\n")
            return imghash


"""
difference value determines how similar images must look; lower value means images have to look more similar
hash_size value determines the complexity of the hashing; higher values means higher intensity = more CPU usage = takes longer
adjust difference and hash_size values in relation with each other
"""
# The default values chosen here are what worked best for grouping together higher resolution (32x32 and higher) mm3D textures
def duplicate_sorter(
    directory,
    difference=18,
    hash_size=12,
    reverse_var=True,
    sort=True,
    print_output=False,
):
    count = 0 # keeps track of how many duplicates there are

    # For loop that gets files from directory and checks if they're PNGs
    image_list = [image_files for image_files in os.scandir(directory) if image_files.name.endswith(".png")]
    if reverse_var: image_list.reverse() # starting from higher res files might be better?

    with CacheHash(directory, f".hash{hash_size}", hash_size) as cache:
        for image in image_list:
            duplicate_images = []
            image_list.remove(image)    # Image is removed to reduce amount of images hashed
            # Imagehash has multiple methods, refer to the documentation and experiment with the one that works best for you
            # In testing against mm3D textures, phash with a difference of 18 and hash size of 12 worked the best with a few misses
            hash1 = cache.get_hash(image.path)

            for image2 in image_list:
                hash2 = cache.get_hash(image2.path)
                # The lower the difference value, the closer the images have to look to each other
                if hash1 - hash2 < difference:
                    count += 1
                    if image not in duplicate_images:
                        duplicate_images.append(image)
                    if image2 not in duplicate_images:
                        duplicate_images.append(image2)
                    image_list.remove(image2)
            # move the "if image not in duplicate_images:" check outside before hashing to prevent unnecesary hashing?
            if sort:
                # Checks that there are images, type check might be a bit redudant
                if duplicate_images != [] and type(duplicate_images) is list:
                    if print_output: print(duplicate_images)
                    for image in duplicate_images[1:]:
                        duplicate_directory = duplicate_images[0].path[0:-4]
                        if not os.path.isdir(duplicate_directory):
                            os.mkdir(duplicate_directory)
                        if os.path.exists(duplicate_images[0].path):
                            os.replace(duplicate_images[0].path, os.path.join(duplicate_directory, duplicate_images[0].name))

                        if os.path.exists(image.path):
                            os.replace(image.path, os.path.join(duplicate_directory, image.name))

    return count

def secondary_passes(directory, difference=10, hash_size=8):
    files = [[root, files] for root, dir, files in os.walk(directory, topdown=True)] # Uses os.walk to get all files and their subdirectories
    mainDirectory = [entry for entry in os.scandir(directory) if entry.name.endswith(".png")] # Gets only .pngs of mainDirectory
    for parent_dir, files_in_parent in files[1:]: # Cuts off the first entry in files because that is the main directory, not sub folders
        lowres_images = []

        image_sizes = [Image.open(os.path.join(parent_dir,image)).size for image in files_in_parent]
        image_paths = [image for image in files_in_parent]

        for image in image_paths:
            if Image.open(os.path.join(parent_dir, image)).size == min(image_sizes):
                lowres_images.append(image)

        for image_in_mainDirectory in mainDirectory:
            try:
                if imagehash.phash(Image.open(os.path.join(parent_dir, lowres_images[0])), hash_size) - imagehash.phash(Image.open(image_in_mainDirectory.path), hash_size) < difference:
                    print(os.path.join(parent_dir, lowres_images[0]), image_in_mainDirectory.path)
                    os.replace(image_in_mainDirectory.path, os.path.join(parent_dir, image_in_mainDirectory.name))
            except:
                None
