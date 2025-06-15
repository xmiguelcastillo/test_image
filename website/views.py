import numpy as np
from django.http import JsonResponse


def get_array(request):
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    return JsonResponse({"array": arr.tolist()})


def upload_image(request):
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    return JsonResponse({"array": arr.tolist()})
