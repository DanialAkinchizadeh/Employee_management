from django.urls import path
from .views import LoginViewEMP,LoginViewCEO,logout_user,RegisterView,ProfileView
app_name='accounts'

urlpatterns = [
    path('login-emp/',LoginViewEMP.as_view(),name='login_emp'),
    path('login-ceo/',LoginViewCEO.as_view(),name='login_ceo'),
    path('logout/',logout_user,name='logout'),
    path('register/',RegisterView.as_view(),name='register'),
    path('profile-info/',ProfileView.as_view(),name='profile-info'),
]
