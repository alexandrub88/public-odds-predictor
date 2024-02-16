from django.contrib import admin
from django.urls import path, include # Make sure include is imported here
from webpage import views as webpage_views  # Import the views from your app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', webpage_views.home, name='home'),
    path('webpage/', include('webpage.urls')),
]
