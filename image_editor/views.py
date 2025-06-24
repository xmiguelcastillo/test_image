from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
from io import BytesIO
import base64


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

    return Image.fromarray(blurred_np)


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


def change_color(image: Image.Image, rgb: list) -> Image.Image:
    image = image.convert("RGB")
    image_output = np.array(image)
    for i in range(len(image_output)):
        for j in range(len(image_output[i])):
            # print(image_output[i][j])
            if (
                image_output[i][j][0] > 150
                and image_output[i][j][1] > 150
                and image_output[i][j][2] > 150
            ):
                image_output[i][j][0] = 255
                image_output[i][j][1] = 255
                image_output[i][j][2] = 255
            else:
                image_output[i][j][0] = rgb[0]
                image_output[i][j][1] = rgb[1]
                image_output[i][j][2] = rgb[2]
    return Image.fromarray(image_output)


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        image_file = request.FILES.get("image")
        rColor = request.POST.get("rColor")
        gColor = request.POST.get("gColor")
        bColor = request.POST.get("bColor")
        # intensity = request.POST.get("intensity")
        rgb = [int(rColor), int(gColor), int(bColor)]
        if not image_file:
            return JsonResponse({"error": "No image uploaded"}, status=400)

        try:
            image = Image.open(image_file)
            og_image = Image.open(image_file)
            image = image.convert("RGB")

            # image_output = np.array(image)
            # HEIGHT, WIDTH, COLORS = image_output.shape
            #
            # rotated = np.zeros((WIDTH, HEIGHT, COLORS), dtype=np.uint8)
            # for y in range(HEIGHT):
            #     for x in range(WIDTH):
            #         rotated[x, HEIGHT - y - 1] = image_output[y, x]

            # rotated_img = Image.fromarray(rotated)
            colored_img = change_color(og_image, rgb)
            # greyscaled_img = grayscale(og_image)
            # blurred_img = box_blur(og_image, int(intensity))

            # buffered_rotated = BytesIO()
            # rotated_img.save(buffered_rotated, format="PNG")
            # img_str = base64.b64encode(buffered_rotated.getvalue()).decode()

            buffered_colored = BytesIO()
            colored_img.save(buffered_colored, format="PNG")
            img_colored_str = base64.b64encode(
                buffered_colored.getvalue()).decode()

            # buffered_blurred = BytesIO()
            # blurred_img.save(buffered_blurred, format="PNG")
            # img_blurred_str = base64.b64encode(
            #     buffered_blurred.getvalue()).decode()

            # buffered_grey = BytesIO()
            # greyscaled_img.save(buffered_grey, format="PNG")
            # img_grey_str = base64.b64encode(buffered_grey.getvalue()).decode()
            return JsonResponse(
                {
                    "message": "Image received successfully",
                    # "shape": [WIDTH, HEIGHT, COLORS],
                    # "rotated_base64": img_str,
                    "colored_base64": img_colored_str,
                    # "blurred_base64": img_blurred_str,
                    # "grey_base64": img_grey_str,
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_array(request):
    arr = np.array([[1, 4444, 32], [4, 5, 132313290]])
    return JsonResponse({"array": arr.tolist()})
