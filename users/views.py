import secrets

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from service.send_utils import send_auth_code
from users.forms import CustomUserCreationForm, CustomAuthenticationForm, ActivationCodeForm

User = get_user_model()


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/signin-form.html'
    success_url = reverse_lazy('mailers:testmail')

    def form_valid(self, form):
        messages.success(self.request, 'Login successful.')
        return super().form_valid(form)


class CustomSignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup-form.html'
    success_url = reverse_lazy('users:sign-in')

    def form_valid(self, form):
        form.instance.auth_code = secrets.token_hex(3).upper()
        messages.success(self.request, 'Registration successful. You can now log in.')
        response = super().form_valid(form)
        send_auth_code(form.instance.email, form.instance.auth_code)
        return response


class ActivateAccountView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'users/activate_account.html'
    form_class = ActivationCodeForm
    success_url = reverse_lazy('mailers:subscribers')

    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.is_email_verified

    def form_valid(self, form):
        auth_code = form.cleaned_data['auth_code']
        user = self.request.user
        if user.auth_code == auth_code:
            user.is_email_verified = True
            user.save()
            messages.success(self.request, 'Account successfully activated.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid activation code.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Account is already active.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:sign-in')
    success_url = reverse_lazy('users:sign-in')
