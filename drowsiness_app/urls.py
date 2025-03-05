from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("driver_dashboard/", views.driver_view, name="driver_dashboard"),
    path('update-settings/', views.update_settings, name='update_settings'),
    path('toggle-monitoring/', views.toggle_monitoring, name='toggle_monitoring'),
    path('update-profile/', views.update_profile, name='update_profile'),
    
]
