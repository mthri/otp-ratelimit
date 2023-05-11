from django.urls import path, include

from register.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('register/', include('register.urls')),
]
