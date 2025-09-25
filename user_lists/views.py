from django.shortcuts import render
from django.views.generic import ListView,TemplateView,DetailView,DeleteView
from accounts.models import EmployeeProfile,User
from django.urls import reverse_lazy

class UserView(ListView):
    template_name='user_lists/user_view.html'
    model=EmployeeProfile


class ProfileView(DetailView):
    template_name='user_lists/profile_view.html'
    model=EmployeeProfile
    context_object_name='profile'

class UserDeleteView(DeleteView):
    template_name='user_lists/user_view.html'
    model=EmployeeProfile
    success_url= reverse_lazy('home')