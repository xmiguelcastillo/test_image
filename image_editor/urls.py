from django.urls import path
from . import views

urlpatterns = [
    path("get-array/", views.get_array),
    path("upload-image/", views.upload_image),
]
