import sys
from PIL import Image
import random


terrain_types = {
    "water": (96, 128, 255),
    "grass": (32, 164, 32),
}


def get_center_offset_from_seed(seed):
    """
    Get the center X, Y offset from the seed.

    The offset will be different for each seed.
    """
    dx = seed % 64
    dy = seed % 64

    return dx, dy

def get_distance_from_center(x, y, seed):
    """
    Check the distance from the closest "center" for a given coordinate

    A center occurs on 200-pixel intervals.
    """
    dx, dy = get_center_offset_from_seed(seed)
    
    closestx = (round(x / 200) * 200) + dx
    closesty = (round(y / 200) * 200) + dy

    return closestx-x, closesty-y

def is_path(x, y, seed):
    """
    Check if the position is on a "path"
    """
    dx, dy = get_center_offset_from_seed(seed)
    
    if (x % 200 == dx or y % 200 == dy) and x > 0 and y > 0:
        return True

    return False


def generate(x, y, old_value, seed):
    """
    Generate the pixel color from an position and the old value.

    Return the new color.
    """
    dx, dy = get_distance_from_center(x, y, seed)
    if abs(dx) < 30 and abs(dy) < 30:
        if abs(dx) < 15 and abs(dy) < 15:
            return (250, 125, 0)

        return (230, 108, 0)

    if is_path(x, y, seed):
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
    rndarr = range(0, abs(seed)+1, round(seed/65536))

    def get_next():
        nonlocal i

        i = (i+1) % max(1, len(rndarr)-1)
        return rndarr[i]


    def is_water(x, y, a, b, c, is_negative):
        waterinterval = 128 + (c % 1024)
        waterx = a % 512
        watery = b % 512
        watersize = a % 128 + b % 128

        print(f"\rwi: {waterinterval}, wx: {waterx}, wy: {watery}, wsize: {watersize}", end="")

        rx = x % waterinterval
        ry = y % waterinterval

        if is_negative:
            watersize = watersize * 2

        if rx > waterx-watersize and rx < waterx+watersize and \
            ry > watery-watersize and ry < watery+watersize:
                return True

        return False

    a = get_next() * get_next()
    b = get_next() * get_next()
    c = get_next() * get_next() * get_next()

    w, h = img.size
    for y in range(h):
        for x in range(w):
            pixel = terrain_types['water'] if is_water(x, y, a, b, c,
                seed < 0) is True else terrain_types['grass']
            img.putpixel((x, y), generate(x, y, pixel, seed))

    return img

def create_seed():
    seed = round(random.random() * 2**24)
    if random.random() > 0.5:
        return -seed

    return seed

seed = create_seed()
print(f"your seed is {seed}")

terrain_image = Image.new("RGB", (1600, 1200), (0, 0, 0))
transform_terrain(
    generate_terrain(
        terrain_image, seed), seed).save(f"test{seed}.png")