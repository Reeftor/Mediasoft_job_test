from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_ref, name='redirectref'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/admin/', views.AdminProfileView.as_view(), name='adminprofile'),
    path('profile/admin/userpage/<int:pk>/', views.UserpageAdminView.as_view(), name='userpage'),
    path('profile/admin/edituserpost/<int:image_id>', views.AdminPostEditView.as_view(), name='editpost'),
    path('profile/admin/deleteuser/<int:user_id>/', views.delete_user, name='deleteuser'),
    path('profile/admin/blockuser/<int:user_id>/', views.block_user, name='blockuser'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.RegistrationView.as_view(), name='signup'),
    path('delete/<int:image_id>/', views.delete_image, name='delete'),
    path('counter/<int:pk>/', views.ImageClickCounterRedirectView.as_view(), name='viewcount')

]
