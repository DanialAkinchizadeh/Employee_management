from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, TemplateView
from .forms import LoginFormEMP, LoginFormCEO, RegisterForm, EmpProfileForm, CeoProfileForm
from .models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class LoginViewEMP(View):
    def get(self, request):
        form = LoginFormEMP()
        return render(request, 'accounts/login_emp.html', {'form_emp': form})

    def post(self, request):
        form = LoginFormEMP(request.POST)
        if form.is_valid():
            national_code = form.cleaned_data['national_code']
            password = form.cleaned_data['password']

            user = authenticate(
                request=request, national_code=national_code, password=password)

            if user is not None:
                if user.role != 'employee':
                    form.add_error(None, 'این بخش مخصوص کارمندان است')
                else:
                    login(request, user)
                    return redirect('home')

            else:
                form.add_error(None, 'نام کاربر یا رمز عبور اشتباه است')

        return render(request, 'accounts/login_emp.html', {'form_emp': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


class LoginViewCEO(View):
    def get(self, request):
        form = LoginFormCEO()
        return render(request, 'accounts/login_ceo.html', {'form_ceo': form})

    def post(self, request):
        form = LoginFormCEO(request.POST)
        if form.is_valid():
            user = form.user
            if user is None:
                form.add_error(None, 'نام کاربری یا رمز عبور اشتباه است')
                return render(request, 'accounts/login_ceo.html', {'form_ceo': form})

            if user.role != 'ceo':
                form.add_error(None, 'این بخش مخصوص مدیرعامل است')
                return render(request, 'accounts/login_ceo.html', {'form_ceo': form})

            login(request, user)
            return redirect('home')
        return render(request, 'accounts/login_ceo.html', {'form_ceo': form})


class RegisterView(View):
    def get(self, request):
        forms = RegisterForm()
        return render(request, 'accounts/register.html', {'forms': forms})

    def post(self, request):
        forms = RegisterForm(request.POST)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.set_password(forms.cleaned_data['password'])
            user.save()
            user = authenticate(
                request=request, national_code=forms.cleaned_data['national_code'], password=forms.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            
        return render(request, 'accounts/register.html', {'forms': forms})


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile_info.html'

    def get(self, request):
        user = request.user
        profile = user.get_profile()

        # edit_mode از query parameter یا default False
        edit_mode = request.GET.get("edit") == "true"

        if user.role == 'employee':
            form = EmpProfileForm(instance=profile)
        else:
            form = CeoProfileForm(instance=profile)

        context = {
            'user': user,
            'profile': profile,
            'category': profile.department_of.all(),
            'edit_mode': edit_mode,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        profile = user.get_profile()

        if user.role == 'employee':
            form = EmpProfileForm(
                request.POST, request.FILES, instance=profile)
        else:
            form = CeoProfileForm(
                request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            # بعد از ذخیره → حالت نمایش
            return redirect('accounts:profile-info')

        context = {
            'user': user,
            'profile': profile,
            'category': profile.department_of.all(),
            'edit_mode': True,
            'form': form,
        }
        return render(request, self.template_name, context)
