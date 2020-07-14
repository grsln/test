from django.urls import path
from .views import image_upload

app_name = 'upload'
urlpatterns = [
    path("", image_upload, name="upload"),
]
