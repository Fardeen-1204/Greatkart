from django.urls import path, include
from .views import *

urlpatterns = [
    path('signin/', login_view, name='signin'),  # Login page
    path('logout/', logout_view, name='logout'),  # Logout page

    # Register
    path('register/', register_view, name='register'),  # Register page
]