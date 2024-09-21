from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('client-registration', views.create_client, name='create_client'),
    path('login/', views.login_client, name='login_client'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_client, name=('logout_client')),
    path('upload/', views.upload, name='upload'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile', views.edit_profile, name='edit_profile')
]

