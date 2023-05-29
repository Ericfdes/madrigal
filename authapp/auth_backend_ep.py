from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import ValidationError


class EmailOrUsernameModelBackend(object):

    def authenticate(self, request, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            messages.error(request, "Invalid Credentials!")

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None