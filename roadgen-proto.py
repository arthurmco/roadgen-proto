import sys
from PIL import Image
import random


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

def create_seed():
    seed = round(random.random() * 2**24)
    if random.random() > 0.5:
        return -seed

    return seed

seed = create_seed()
print(f"your seed is {seed}")

terrain_image = Image.new("RGB", (1600, 1200), (0, 0, 0))
transform_terrain(terrain_image, seed).save(f"test{seed}.png")