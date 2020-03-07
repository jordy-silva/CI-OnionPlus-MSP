from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib import auth, messages
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
                return redirect(reverse('index'))
    else:
        login_form = UserLoginForm()
        return redirect(reverse('index'))


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
            messages.error(request, registration_form.error_messages)
    else:
        registration_form = UserRegistrationForm()
    if redirect_to:
        return HttpResponseRedirect(redirect_to)
    else:
        return redirect(reverse('index'))

def profile(request):
    """ Create a view to show user's profile page """
    return render(request, "profile.html")
