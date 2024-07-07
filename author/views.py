from django.shortcuts import render, redirect
from .forms import RegistrationForm, ChnageUserData
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post

#class based view
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account Created Successfully!!')
            return redirect('loginPage')
    else:
        register_form = RegistrationForm()
    return render(request, 'register.html', {'form': register_form, 'type':'Register'})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            passd = form.cleaned_data['password']
            user = authenticate(username = user_name, password = passd)
            if user is not None:
                messages.success(request, 'Successfully loged In!!')
                login(request, user)
                return redirect('profilePage')
            else:
                messages.warning(request, 'Log in credentials are in correct!!')
                return redirect('register')
    else:
        form = AuthenticationForm()
    return render(request, 'register.html', {'form':form, 'type':'Login'}) 


class UserLoginView(LoginView):
    template_name = 'register.html'
    # success_url = reverse_lazy('profilePage')

    def get_success_url(self):
        return reverse_lazy('profilePage')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.waring(self.request, 'Logged is unsuccessful')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Login'
        return context
    
# class UserLogoutView(LogoutView):
#     template_name = 'logged_out.html'


@login_required
def profile(request):
    data = Post.objects.filter(author = request.user)
    return render(request, 'profile.html', {'data' : data})

@login_required
def u_profile(request):
    if request.method == 'POST':
        profile_form = ChnageUserData(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated successfully')
            return redirect('profilePage')
    else:
        profile_form = ChnageUserData(instance = request.user)
    return render(request, 'update_profile.html', {'form': profile_form})


def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully!!')
            update_session_auth_hash
            return redirect('profilePage')
    else:
        form =  PasswordChangeForm(user = request.user)
    return render(request, 'pass_change.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('homepage')