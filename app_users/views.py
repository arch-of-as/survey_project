from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from app_users.forms import UserRegisterForm, ProfileForm, ChangeColorForm
from app_users.models import Profile
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.models import User


class LoginView(LoginView):
    template_name = 'users/login.html'


class LogoutView(LogoutView):
    template_name = 'users/logout.html'


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return HttpResponseRedirect('/')

    form = UserRegisterForm()
    return render(request=request, template_name="users/registration.html", context={"register_form": form})


class UserDetailView(generic.DetailView):
    model = User
    template_name = 'users/user_detail.html'


class UserUpdate(generic.edit.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/user_edit.html'
    success_url = '../'

    def get_object(self):
        return self.request.user.profile


class UsersListView(generic.ListView):
    model = Profile
    template_name = 'users/users_list.html'
    context_object_name = 'users_list'
    queryset = Profile.objects.all()


class ColorChangeView(generic.edit.UpdateView):
    model = Profile
    form_class = ChangeColorForm
    template_name = 'users/color_edit.html'
    success_url = '../'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.user.profile.balance >= 100:
            if form.is_valid():
                request.user.profile.balance -= 100
                request.user.profile.color = request.POST['color']
                request.user.profile.save()
                return HttpResponseRedirect('../')
            else:
                return HttpResponse(f'<h1> Unknown color </h1> '
                                    f'<a href="/users/{request.user.id}/style"> Try again </a>')
        else:
            return HttpResponse('<h1> Insufficient funds </h1> <a href="/"> Take the survey </a>')
