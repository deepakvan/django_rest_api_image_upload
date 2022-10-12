from django.urls import path
from .views import login,sample_api,upload_image,all,register


urlpatterns = [
    path('api/sampleapi', sample_api,name="test"),
    path('api/login', login,name="login"),
    path('api/upload',upload_image,name="upload"),
    path('api/register', register,name="register"),
    path('api/view',all,name="all")
]


