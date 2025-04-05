from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from Petstagram.accounts.forms import PetstagramUserCreateForm, LoginForm, PetstagramUserEditForm
from Petstagram.accounts.models import PetstagramUser
from django.contrib.auth import views as auth_views


class UserRegisterView(CreateView):
    model = PetstagramUser
    form_class = PetstagramUserCreateForm
    template_name = '../templates/profile/register-page.html'
    success_url = reverse_lazy('login')


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = '../templates/profile/login-page.html'
    next_page = reverse_lazy('index')


class UserLogoutView(auth_views.LogoutView):
    # next_page = reverse_lazy('login')
    pass


class UserDetailsView(LoginRequiredMixin, DetailView):
    model = PetstagramUser
    template_name = '../templates/profile/profile-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_likes_count = sum(p.like_set.count() for p in self.object.photo_set.all())
        total_photo_count = self.object.photo_set.all().count()
        total_pets_count = self.object.pet_set.all().count()
        total_pets = self.object.pet_set.all()
        total_photos = self.object.photo_set.all()

        context.update({
            'total_likes_count': total_likes_count,
            'total_photo_count': total_photo_count,
            'total_pets_count': total_pets_count,
            'total_pets': total_pets,
            'total_photos': total_photos,
        })

        return context


class UserEditView(UpdateView):
    model = PetstagramUser
    form_class = PetstagramUserEditForm
    template_name = '../templates/profile/profile-edit-page.html'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})


class UserDeleteView(DeleteView):
    model = PetstagramUser
    template_name = '../templates/profile/profile-delete-page.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return redirect(self.success_url)
