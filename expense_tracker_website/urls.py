from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('sign-in', include('main.urls')),
    path('user/', include('main.urls'))
]
