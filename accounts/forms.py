from django import forms
from django.forms import ValidationError
from django.contrib.auth import get_user_model, authenticate
from .models import CEOProfile,EmployeeProfile
User = get_user_model()


class LoginFormEMP(forms.Form):
    use_required_attribute = False
    national_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={'class': 'input-login', 'placeholder': 'National Code'}),
        required=True,
        label='',
        error_messages={
            'required': 'لطفا کد ملی خود را وارد کنید'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'input-login', 'placeholder': 'Password'}),
        required=True,
        label='',
        error_messages={
            'required': 'لطفا رمز خود را وارد کنید'
        }
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        if not User.objects.filter(national_code=national_code).exists():
            raise ValidationError('این کد ملی در سامانه وجود ندارد ')
        return national_code

    


class LoginFormCEO(forms.Form):
    national_code = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'class': 'input-login', 'placeholder': 'National Code'}),
        required=True,
        label='',
        error_messages={
            'required': 'لطفا کد ملی خود را وارد کنید'
    })
    phone_number=forms.CharField(max_length=11,widget=forms.TextInput(
        attrs={'class': 'input-login', 'placeholder': 'Phone_Number'}),
        required=True,
        label='',
        error_messages={
            'required': 'لطفا شماره تلفن خود را وارد کنید'
        })
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input-login', 'placeholder': 'Password'}),
        required=True,
        label='',
        error_messages={
            'required': 'لطفا رمز خود را وارد کنید'
    })
    def __init__(self,*args,**kwargs):
        self.request=kwargs.pop('request',None)
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data=super().clean()
        national_code = cleaned_data.get('national_code')
        phone_number = cleaned_data.get('phone_number')
        password = cleaned_data.get('password')
        if national_code and password and phone_number:
            user=authenticate(request=self.request,phone_number=phone_number,national_code=national_code,password=password)
            if user is None:
                raise ValidationError('اطلاعات وارد شده صحیح نمی باشد')
            self.user=user
        return cleaned_data


class RegisterForm(forms.ModelForm):
    use_required_attribute = False
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-group','placeholder':'password','required':True}),
            error_messages={
                'required':'لطفا رمز عبور خود را وارد کنید',
            })
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-group','placeholder':'confirm-password','required':True}),
             error_messages={
                'required':'لطفا رمز عبور خود را وارد یا تکرار کنید',
            })
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in ['phone_number','email','national_code']:
            self.fields[field].required = True
    
    class Meta:
        model=User
        fields=['phone_number','email','national_code','role']
        widgets={
            'phone_number':forms.TextInput(attrs={'class':'form-group','placeholder':'phone_number'}),
            'email':forms.EmailInput(attrs={'class':'form-group','placeholder':'email'}),
            'national_code':forms.TextInput(attrs={'class':'form-group','placeholder':'national_code'}),
            'role':forms.Select(attrs={'class':'form-group',})
        }
        error_messages={
            'phone_number':{
                'required':'لطفا شماره تلفن خود را وارد کنید'
            },
            'email':{
                'required':'لطفا ایمیل خود را وارد کنید',
                'invalid':'ایمیل معتبر وارد کنید',
            },
            'national_code':{
                'required':'لطفا کدملی خود را وارد کنید'
            }, 
        }
    
        
    def clean(self):
        cleaned_data=super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        phone_number=cleaned_data.get('phone_number')
        national_code=cleaned_data.get('national_code')
        email=cleaned_data.get('email')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'رمز عبورها یکسان نیستند')

        if email and not email.endswith('@gmail.com'):
            self.add_error('email', 'آدرس ایمیل باید Gmail باشد')

        if phone_number and not phone_number.startswith('0'):
            self.add_error('phone_number', 'شماره تلفن باید با صفر شروع شود')
        if national_code and  len(national_code) != 10:
            self.add_error ('national_code',f'رقم وارد کرده اید{len(national_code)}کدملی باید دقیقا 10 رقم باشد ولی شما ')
        return cleaned_data
    
    

class EmpProfileForm(forms.ModelForm):

    class Meta:
        model=EmployeeProfile
        fields=['first_name','last_name','department_of','profile_image','short_description','age']

    
class CeoProfileForm(forms.ModelForm):

    class Meta:
        model=CEOProfile
        fields=['first_name','last_name','department_of','profile_image','age']