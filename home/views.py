from django.shortcuts import render
from django.views.generic import TemplateView,View
from accounts.models import EmployeeProfile
from django.contrib import messages

class HomeView(View):
    def get(self,request):
        messages.info(request,'کاربر گرامی لطفا با زدن بر روی دکمه مشاهده پروفایل ،پروفایل خود را تکمیل کنید ')
        return render(request,'home/index.html')