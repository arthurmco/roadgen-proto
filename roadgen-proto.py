import sys
from PIL import Image


def get_distance_from_center(x, y):
    """
    Check the distance from the closest "center" for a given coordinate

    A center occurs on 200-pixel intervals.
    """
    closestx = round(x / 200) * 200
    closesty = round(y / 200) * 200

    return closestx-x, closesty-y

def generate(x, y, old_value):
    """
    Generate the pixel color from an position and the old value.

    Return the new color.
    """
    dx, dy = get_distance_from_center(x, y)
    if abs(dx) < 30 and abs(dy) < 30:
        if abs(dx) < 15 and abs(dy) < 15:
            return (250, 125, 0)

        return (230, 108, 0)

    return old_value


def transform_terrain(img):
    w, h = img.size
    for y in range(h):
        for x in range(w):
            img.putpixel((x, y), generate(x, y, img.getpixel((x, y))))

    return img

terrain_image = Image.new("RGB", (1600, 1200), (0, 0, 0))
transform_terrain(terrain_image).save("test.png")