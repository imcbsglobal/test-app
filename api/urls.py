from django.urls import path
from .views import HomeView, LoginView, LogoutView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),        # Base URL → http://127.0.0.1:8000/
    path('home/', HomeView.as_view(), name='home'),                 
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]