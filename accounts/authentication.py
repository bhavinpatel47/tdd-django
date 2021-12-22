from accounts.models import User, Token

class PasswordlessAuthenticationBackend(object):
    def authenticate(self, request, token_uid):
        try:
            token = Token.objects.get(uid=token_uid)
            user = User.objects.get(email=token.email)
            return user
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, user_email):
        try:
            return User.objects.get(email=user_email)
        except User.DoesNotExist:
            return None
