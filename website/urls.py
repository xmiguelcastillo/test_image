from django.contrib import admin
from django.urls import path
from image_editor.views import get_array
from image_editor.views import upload_image

urlpatterns = [
    path("admin/", admin.site.urls),
    path("get-array/", get_array),
    path("upload-image/", upload_image),
]
