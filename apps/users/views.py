from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, TemplateView

from users.forms import CreationForm

from .tokens import account_activation_token

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('confirmation')
    template_name = 'signup.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ConfirmationView(TemplateView):
    template_name = 'confirmation.html'


class ConfirmationCompleteView(TemplateView):

    template_name = 'confirmation_complete.html'

    def dispatch(self, *args, **kwargs):

        assert 'uidb64' in kwargs and 'token' in kwargs
        self.validlink = False

        try:
            uid = urlsafe_base64_decode(kwargs['uidb64']).decode()
            self.user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.user = None

        if self.user is not None:
            token = kwargs['token']
            if account_activation_token.check_token(self.user, token):
                self.validlink = True
                self.user.is_active = True
                self.user.save()

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        return context
