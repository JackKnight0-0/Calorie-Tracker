from allauth.account.views import SignupView, LoginView, PasswordChangeView, PasswordResetView, PasswordResetFromKeyView

from .forms import CustomSignUpForm, CustomLoginForm, CustomPasswordChangeForm, CustomResetPasswordForm, \
    CustomResetPasswordKeyForm


class CustomSingUpView(SignupView):
    form_class = CustomSignUpForm
    template_name = 'account/signup.html'


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'account/login.html'


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'account/password_change.html'


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomResetPasswordForm
    template_name = 'account/password_reset.html'


class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    form_class = CustomResetPasswordKeyForm
    template_name = 'account/password_reset_from_key.html'
