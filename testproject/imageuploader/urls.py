from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.RegistrationView.as_view(), name='signup'),
    path('delete/<int:image_id>/', views.delete_image, name='delete'),
    path('counter/<int:pk>/', views.ImageClickCounterRedirectView.as_view(), name='viewcount')
]
