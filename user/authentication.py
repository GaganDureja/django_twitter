from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        if username:
            # Check if username is provided and try to authenticate using it
            if username:
                try:
                    user = user_model.objects.get(username=username)
                    if user.check_password(password):
                        return user
                except user_model.DoesNotExist:
                    pass

            # Check if email is provided and try to authenticate using it
            if '@' in username:  # Assuming if '@' is present, it's an email
                print("checking in email")
                try:
                    user = user_model.objects.get(email=username)
                    if user.check_password(password):
                        return user
                except user_model.DoesNotExist:
                    pass

            # Check if phone number is provided and try to authenticate using it
            if username.isdigit():  # Assuming if it's all digits, it's a phone number
                try:
                    user = user_model.objects.get(phone_number=username)
                    if user.check_password(password):
                        return user
                except user_model.DoesNotExist:
                    pass

            # Return None if no user was authenticated
            return None
        else:
            return None