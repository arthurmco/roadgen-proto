import sys
from PIL import Image
import random


terrain_types = {
    "water": (96, 128, 255),
    "deep_water": (6, 38, 165),
    "grass": (32, 164, 32),
}


def is_terrain_buildable(old_value):
    return old_value != terrain_types['deep_water'] and old_value != terrain_types['water']

def get_center_offset_from_seed(seed):
    """
    Get the center X, Y offset from the seed.

    The offset will be different for each seed.
    """
    dx = seed % 64
    dy = seed % 64

    return dx, dy

def get_distance_from_center(x, y, old_value, seed):
    """
    Check the distance from the closest "center" for a given coordinate

    A center occurs on 200-pixel intervals.
    """
    if not is_terrain_buildable(old_value):
        # TODO: if possible, return the distance to the closest non-water center?
        return 200, 200 

    dx, dy = get_center_offset_from_seed(seed)
    
    closestx = (round(x / 200) * 200) + dx
    closesty = (round(y / 200) * 200) + dy

    return closestx-x, closesty-y

def is_path(x, y, old_value, seed):
    """
    Check if the position is on a "path"
    """
    dx, dy = get_center_offset_from_seed(seed)
   
    if not is_terrain_buildable(old_value):
        return False

    def on_bias(vx, vcenter, vdx, vbias):
        return vx % vcenter >= vdx-vbias and vx % vcenter <= vdx+vbias

    if (on_bias(x, 200, dx, 1) or on_bias(y, 200, dy, 1)) and x > 0 and y > 0:
        return True

    return False


def generate(x, y, old_value, seed):
    """
    Generate the pixel color from an position and the old value.

    Return the new color.
    """
    dx, dy = get_distance_from_center(x, y, old_value, seed)
    if abs(dx) < 30 and abs(dy) < 30:
        if abs(dx) < 15 and abs(dy) < 15:
            return (250, 125, 0)

        return (230, 108, 0)

    if is_path(x, y, old_value, seed):
        return (255, 255, 255)

    return old_value


def transform_terrain(img, seed):
    w, h = img.size
    for y in range(h):
        for x in range(w):
            img.putpixel((x, y), generate(x, y, img.getpixel((x, y)), seed))

    return img



def generate_terrain(img, seed):
    """
    Generate a simple terrain for us.

    Might be badly coded, but will be there only to generate a basic terrain.
    It is not the core of the script.
    """
    i = 0
    rndarr = range(0, abs(seed)+1, round(abs(seed)/65536))

    def get_next():
        nonlocal i

        i = (i+1) % max(1, len(rndarr)-1)
        return rndarr[i]


    def is_water(x, y, a, b, c, is_negative):
        """
        Calculate if a certain pixel is a water pixel

        Usually they lie in the corners of deep water pixels
        """
        deep_waterinterval = 128 + (c % 1024)
        deep_waterx = a % 512
        deep_watery = b % 512
        deep_watersize = a % 128 + b % 128

        rx = x % deep_waterinterval
        ry = y % deep_waterinterval

        if is_negative:
            deep_watersize = deep_watersize * 2

        water_limit = 25

        wx1 = deep_waterx-deep_watersize
        wx2 = deep_waterx+deep_watersize 
        wy1 = deep_watery-deep_watersize
        wy2 = deep_watery+deep_watersize

        if rx > wx1 and rx < wx2 and ry > wy1 and ry < wy2:
            if abs(wx1-rx) <= water_limit or abs(rx-wx2) <= water_limit or \
                abs(wy1-ry) <= water_limit or abs(ry-wy2) <= water_limit:
                return True

        return False

    def is_deep_water(x, y, a, b, c, is_negative):
        """
        Calculate if a certain pixel is a deep water pixel
        """
        deep_waterinterval = 128 + (c % 1024)
        deep_waterx = a % 512
        deep_watery = b % 512
        deep_watersize = a % 128 + b % 128

        rx = x % deep_waterinterval
        ry = y % deep_waterinterval

        if is_negative:
            deep_watersize = deep_watersize * 2

        if rx > deep_waterx-deep_watersize and rx < deep_waterx+deep_watersize and \
            ry > deep_watery-deep_watersize and ry < deep_watery+deep_watersize:
                return True

        return False

    a = get_next() * get_next()
    b = get_next() * get_next()
    c = get_next() * get_next() * get_next()

    w, h = img.size
    for y in range(h):
        for x in range(w):

            pixel = terrain_types['deep_water'] if is_deep_water(x, y, a, b, c,
                seed < 0) is True else terrain_types['grass']

            if is_water(x, y, a, b, c, seed < 0):
                pixel = terrain_types['water']

            img.putpixel((x, y), generate(x, y, pixel, seed))

    return img

def create_seed():
    seed = round(random.random() * 2**24)
    if random.random() > 0.5:
        return -seed

    return seed


if len(sys.argv) > 1:
    seed = int(sys.argv[1])
else:
    seed = create_seed()

print(f"your seed is {seed}")

terrain_image = Image.new("RGB", (1600, 1200), (0, 0, 0))
transform_terrain(
    generate_terrain(
        terrain_image, seed), seed).save(f"test{seed}.png")