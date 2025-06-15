from PIL import Image
import numpy as np
import math
import cv2


def color_img(image: Image.Image, color: list, background: list) -> Image.Image:
    image = image.convert("RGB")
    image_output = np.array(image)

    for i in range(len(image_output)):
        for j in range(len(image_output[i])):
            if (
                image_output[i][j][0] > 150
                and image_output[i][j][1] > 150
                and image_output[i][j][2] > 150
            ):
                image_output[i][j][0] = background[0]
                image_output[i][j][1] = background[1]
                image_output[i][j][2] = background[2]
            else:
                image_output[i][j][0] = color[0]
                image_output[i][j][1] = color[1]
                image_output[i][j][2] = color[2]

    return Image.fromarray(image_output)


def rotate_img_90(image: Image.Image):
    image = image.convert("RGB")
    image_output = np.array(image)
    HEIGHT = image_output.shape[0]
    WIDTH = image_output.shape[1]
    COLORS = image_output.shape[2]

    rotated = np.zeros((WIDTH, HEIGHT, COLORS), dtype=np.uint8)

    for y in range((HEIGHT)):
        for x in range((WIDTH)):
            rotated[x, HEIGHT - y - 1] = image_output[y, x]

    return Image.fromarray(rotated)


def rotate_img_270(image: Image.Image):
    image = image.convert("RGB")
    image_output = np.array(image)
    HEIGHT = image_output.shape[0]
    WIDTH = image_output.shape[1]
    COLORS = image_output.shape[2]

    rotated = np.zeros((WIDTH, HEIGHT, COLORS), dtype=np.uint8)

    for y in range((HEIGHT)):
        for x in range((WIDTH)):
            rotated[x, HEIGHT - y - 1] = image_output[y, x]

    return Image.fromarray(rotated[::-1])


def rotate_img_180(image: Image.Image):
    image = image.convert("RGB")
    image_output = np.array(image)
    return Image.fromarray(image_output[::-1])


def grayscale(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    image_output = np.array(image)
    for i in range(len(image_output)):
        for j in range(len(image_output[i])):
            avg = (
                image_output[i][j][0] * (0.299)
                + image_output[i][j][1] * (0.587)
                + image_output[i][j][2] * (0.114)
            )
            image_output[i][j][0] = avg
            image_output[i][j][1] = avg
            image_output[i][j][2] = avg
    return Image.fromarray(image_output)


def box_blur(image: Image.Image, intensity: int) -> Image.Image:
    image = image.convert("RGB")
    image_np = np.array(image)
    height, width, channels = image_np.shape

    blurred_np = np.zeros_like(image_np)
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            for c in range(channels):
                row_start = y - 1
                row_end = y + intensity
                col_start = x - 1
                col_end = x + intensity
                region = image_np[row_start:row_end, col_start:col_end, c]
                blurred_np[y, x, c] = np.mean(region)

    blurred_image = Image.fromarray(blurred_np)

    return blurred_image


def glaussian_blur():
    pass


img_source = Image.open(r"./images/astroboy.jpg")

img_colored = color_img(img_source, [255, 175, 255], [255, 255, 255])
# img_colored = color_img(img_source, [255, 255, 255], [0, 0, 0])
# img_source.show()
img_colored.show()
# Grayscale
# img_blur = box_blur(img_source, 10)
# img_blur.show()

# img_gray = grayscale(img_source)
# img_gray.show()
# img_rotate = rotate_img_90(img_source)
# img_rotate_upside = rotate_img_180(img_source)
# img_rotate_upside.show()
