import sys
from PIL import Image


def generate(x, y, old_value):
    """
    Generate the pixel color from an position and the old value.

    Return the new color.
    """
    if x % 100 == 0:
        return (255, 0, 0)

    return old_value


def transform_terrain(img):
    w, h = img.size
    for y in range(h):
        for x in range(w):
            img.putpixel((x, y), generate(x, y, img.getpixel((x, y))))

    return img

terrain_image = Image.new("RGB", (1600, 1200), (0, 0, 0))
transform_terrain(terrain_image).save("test.png")