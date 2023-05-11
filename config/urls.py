from django.urls import path, include

from register.admin import admin_site
from register import views

urlpatterns = [
    path('admin/', admin_site.urls),
    path('register/', include('register.urls')),
]

# http error page
urlpatterns += [
    path('429/', views.error_429, name='error-429'),
]
