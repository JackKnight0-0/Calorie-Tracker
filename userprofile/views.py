from allauth.account.models import EmailAddress
from django.shortcuts import redirect, reverse
from django.views.generic import DetailView, FormView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import UserProfileChangeForm, UserProfileChangeAvatar
from .models import UserProfile


class UserProfileView(LoginRequiredMixin, UserPassesTestMixin, FormView, DetailView):
    model = UserProfile
    template_name = 'userprofile/profile.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = dict()
        context['avatar_form'] = UserProfileChangeAvatar(instance=self.request.user)
        return context

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        return redirect(reverse('profile', kwargs={'slug': slug}))

    def post(self, request, *args, **kwargs):
        form = UserProfileChangeAvatar(self.request.POST, self.request.FILES, instance=self.request.user.user_profile)
        if form.is_valid():
            form.save()
            return self.get_success_url()
        return self.render_to_response(context={'avatar_form': form})

    def test_func(self):
        slug = self.kwargs.get('slug', None)
        if slug:
            userprofile = UserProfile.objects.filter(slug=slug).first()
            if self.request.user.user_profile == userprofile:
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return redirect(reverse('profile', kwargs={'slug': self.request.user.user_profile.slug}))
        return super().dispatch(request, *args, **kwargs)


class ChangeUserProfile(LoginRequiredMixin, FormView):
    template_name = 'userprofile/change_profile.html'

    def get_context_data(self, **kwargs):
        context = dict()
        context['form'] = UserProfileChangeForm(instance=self.request.user)
        return context

    def _rewrite_old_email(self, email):
        """
        deleting the old email and rewrite to a new one
        """
        old_email = EmailAddress.objects.filter(user=self.request.user)
        if not old_email.exists():
            EmailAddress.objects.create(user=self.request.user, email=email, primary=True)
        elif old_email and not email:  # in case if email field is empty
            old_email.delete()
        elif old_email:
            old_email.delete()
            EmailAddress.objects.create(user=self.request.user, email=email, primary=True)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        form = UserProfileChangeForm(self.request.POST, instance=user)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if 'email' in form.cleaned_data:
                self._rewrite_old_email(email=email)
            form.save()
            return redirect(reverse('profile', kwargs={'slug': user.user_profile.slug}))
        return self.render_to_response(context={'form': form})
