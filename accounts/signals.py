from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver

@receiver(user_logged_in)
def mark_user_present(sender, request, user, **kwargs):
    if user.role == 'employee':
        profile = user.get_profile()  
        if profile:
            profile.is_present = True
            profile.save()
    if user.role == 'ceo':
        profile = user.get_profile()  
        if profile:
            profile.is_present = True
            profile.save()


@receiver(user_logged_out)
def mark_user_absent(sender, request, user, **kwargs):
       if user is not None:  # حتما چک کن که کاربر وجود داشته باشه
        profile = user.get_profile()
        if profile:
            profile.is_present = False
            profile.save()