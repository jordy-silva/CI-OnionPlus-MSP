from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import UserLoginForm, UserRegistrationForm


# Create your views here.


def login(request):
    """Render a login page"""
    redirect_to = request.GET.get('next')
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You are logged in!")
                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                else:
                    return redirect(reverse('index'))
            else:
                login_form.add_error(
                    None, "Incorrect Username or password")
        else:
            messages.error(request, 'Please fix the errors')
    else:
        login_form = UserLoginForm()
    signin_form = UserRegistrationForm()
    context = {
        'login_form': login_form,
        'signin_form': signin_form
    }
    return render(request, 'index.html', context)


def logout(request):
    """User log out"""
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect(reverse('index'))


def signup(request):
    """Render a user registration page"""
    redirect_to = request.GET.get('next')
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            instance = registration_form.save(commit=False)
            instance.username = instance.email
            instance.save()
            user = auth.authenticate(username=request.POST['email'],
                                     password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered")
        else:
            messages.error(request, "Unable to register your account")
            messages.error(request, "Fix the errors")
    else:
        registration_form = UserRegistrationForm()
    if redirect_to != 'None':
        return HttpResponseRedirect(redirect_to)
    else:
        login_form = UserLoginForm()
        context = {
            'login_form': login_form,
            'signin_form': registration_form
        }
        return render(request, 'index.html', context)

def profile(request):
    """ Create a view to show user's profile page """
    errors = False
    if request.method == 'POST':
        pwd_change_form = PasswordChangeForm(request.user, request.POST)
        if pwd_change_form.is_valid():
            user = pwd_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated')
        else:
            messages.error(request, 'Please fix the errors')
            errors = True
    else:
        pwd_change_form = PasswordChangeForm(request.user)
    return render(request, "profile.html", {
        'pwd_change_form': pwd_change_form,
        'errors': errors
    })
