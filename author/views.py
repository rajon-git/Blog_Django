from django.shortcuts import render,redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post

# Create your views here.
def register(request):
    if request.method == 'POST':
        register_forms = forms.RegistrationForm(request.POST)
        if register_forms.is_valid():
            register_forms.save()
            messages.success(request, 'Account Created Successfully')
            return redirect('register')
    else:
        register_forms = forms.RegistrationForm()
    return render(request, 'register.html',{'form': register_forms, 'type':'Register'})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user = authenticate(username = user_name, password = user_pass)
            if user is not None:
                messages.success(request, 'User Login Successfully')
                login(request,user)
                return redirect("profile")
            else:
                messages.warning(request, 'Logged in information is incorrect')
                return redirect("register")
    else:
        form = AuthenticationForm()
    return render(request, 'register.html',{'form':form, 'type':'Login'})

@login_required
def profile(request):
    data = Post.objects.filter(author = request.user)
    return render(request, 'profile.html', {'data':data})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.UserDataChangeForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Account update successfully')
            return redirect("profile")
    else:
        profile_form = forms.UserDataChangeForm(instance = request.user)
    return render(request, 'update_profile.html', {'form':profile_form, 'type':'Profile'})


def passowrd_change(request):
    if request.method == 'POST':
        pass_form = PasswordChangeForm(request.user, data=request.POST)
        if pass_form.is_valid():
            pass_form.save()
            messages.success(request, 'Password Change Successfully')
            update_session_auth_hash(request, pass_form.user)
            return redirect("profile")
        
    else:
        pass_form = PasswordChangeForm(user = request.user)
    return render(request, 'pass_change.html', {'form':pass_form})

def user_logout(request):
    logout(request)
    return redirect('login')