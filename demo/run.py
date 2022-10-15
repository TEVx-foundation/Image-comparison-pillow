from PIL import Image
from PIL import ImageChops

class ImageCompareException(Exception):
    pass


def pixel_diff(image_a, image_b):

    if image_a.size != image_b.size:
        raise ImageCompareException(
            "different image sizes, can only compare same size images: A = " + str(image_a.size) + " B = " + str(
                image_b.size))

    if image_a.mode != image_b.mode:
        raise ImageCompareException(
            "different image mode, can only compare same mode images: A = " + str(image_a.mode) + " B = " + str(
                image_b.mode))

    diff = ImageChops.difference(image_a, image_b)
    diff = diff.convert('L')
    return diff


def total_histogram_diff(pixel_diff):
    return sum(i * n for i, n in enumerate(pixel_diff.histogram()))


def image_diff(image_a, image_b):
    histogram_diff = total_histogram_diff(pixel_diff(image_a, image_b))
    return histogram_diff


def is_equal(image_a, image_b, tolerance=0.0):
    return image_diff_percent(image_a, image_b) <= tolerance


def image_diff_percent(image_a, image_b):

    close_a = False
    close_b = False
    if isinstance(image_a, str):
        image_a = Image.open(image_a)
        close_a = True

    if isinstance(image_b, str):
        image_b = Image.open(image_b)
        close_b = True

    try:
        input_images_histogram_diff = image_diff(image_a, image_b)

        black_reference_image = Image.new('RGB', image_a.size, (0, 0, 0))
        white_reference_image = Image.new('RGB', image_a.size, (255, 255, 255))

        worst_bw_diff = image_diff(black_reference_image, white_reference_image)

        percentage_histogram_diff = (input_images_histogram_diff / float(worst_bw_diff)) * 100
    finally:
        if close_a:
            image_a.close()
        if close_b:
            image_b.close()

    return percentage_histogram_diff

percentage = image_diff_percent("a.jpg", "b.jpg")
print("Similarity is:", 100 - percentage)
x = input("\nPress any key to exit.")
