from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from users.tokens import account_activation_token
from django.core.mail import EmailMessage


User = get_user_model()


class CreationForm(UserCreationForm):

    class Meta:

        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.is_active = False
            user.save()
            current_site = get_current_site(self.request)
            domain = current_site.domain
            mail_subject = 'Активация аккаунта Foodgram'
            message = render_to_string('auth/confirmation_email.html', {
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = self.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

        return user
