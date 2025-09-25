# backends.py
from django.contrib.auth.backends import BaseBackend
from .models import User



class NationalCodeBackend(BaseBackend):
    def authenticate(self, request, national_code=None, password=None):
        if not national_code or not password:
            return None
        try:
            user = User.objects.get(national_code=national_code)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None