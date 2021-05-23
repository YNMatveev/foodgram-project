from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{timestamp}{user.is_active}{user.email}'


account_activation_token = TokenGenerator()
