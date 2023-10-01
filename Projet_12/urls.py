
from django.contrib import admin
from django.urls import path
from authentication.views import inscription

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inscription/', inscription, name='inscription'),
]
