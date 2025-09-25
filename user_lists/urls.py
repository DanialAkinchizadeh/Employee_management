from django.urls import path
from .views import UserView,ProfileView,UserDeleteView

app_name='user_list'


urlpatterns = [
    path('',UserView.as_view(),name='user-list'),
    path('profile/<int:pk>/',ProfileView.as_view(),name='profile'),
    path('delete/<int:pk>/',UserDeleteView.as_view(),name='delete'),
]
