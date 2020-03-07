from django.shortcuts import render
from accounts.forms import UserLoginForm, UserRegistrationForm

# Create your views here.


def index(request):
    """Render the index page"""
    redirect_to = request.GET.get('next')
    frontend_url = request.META.get('HTTP_REFERER')
    login_form = UserLoginForm()
    signin_form = UserRegistrationForm()
    context = {
        'login_form': login_form,
        'signin_form': signin_form,
        'redirect_to': redirect_to,
        'frontend_url': frontend_url
    }
    return render(request, 'index.html', context)
