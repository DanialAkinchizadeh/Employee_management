from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


# ------------------- User Manager -------------------
class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password, national_code, role='employee', **extra_fields):
        if not email:
            raise ValueError(_('The email must be set'))
        if not phone_number:
            raise ValueError(_('The phone number must be set'))
        if not national_code:
            raise ValueError(_('The national code must be set'))

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            national_code=national_code,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number, password, national_code, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, phone_number, password, national_code, role='ceo', **extra_fields)


# ------------------- User Model -------------------
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ceo', 'CEO'),
        ('employee', 'Employee'),
    )

    phone_number = models.CharField(max_length=250, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    national_code = models.CharField(max_length=10, unique=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'national_code'
    REQUIRED_FIELDS = ['phone_number', 'email']

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

    def get_profile(self):
        if self.role == 'ceo':
            return getattr(self, 'ceoprofile', None)
        elif self.role == 'employee':
            return getattr(self, 'employeeprofile', None)
    @property
    def first_name(self):
        profile = self.get_profile()
        return profile.first_name if profile else None

    @property
    def last_name(self):
        profile = self.get_profile()
        return profile.last_name if profile else None


# ------------------- Department -------------------
class CategoryDepartment(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


# ------------------- CEO Profile -------------------
class CEOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    department_of = models.ManyToManyField(CategoryDepartment, blank=True)
    profile_image = models.ImageField(upload_to="CEOprofile_pics/", blank=True, null=True)
    is_present = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CEO: {self.first_name} {self.last_name} ({self.user.email})"


# ------------------- Employee Profile -------------------
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    department_of = models.ManyToManyField(CategoryDepartment, blank=True)
    profile_image = models.ImageField(upload_to="EMPprofile_pics/", blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    is_present = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Employee: {self.first_name} {self.last_name} ({self.user.email})"
    
    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()



# ------------------- Signals -------------------
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    
    if created:
        if instance.role == 'ceo':
            CEOProfile.objects.get_or_create(user=instance)
        elif instance.role == 'employee':
            EmployeeProfile.objects.get_or_create(user=instance)
