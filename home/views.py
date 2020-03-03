from django.shortcuts import render
from accounts.forms import UserLoginForm, UserRegistrationForm

# Create your views here.
def index(request):
    """Render the index page"""
    redirect_to = request.GET.get('next')
    login_form = UserLoginForm()
    signin_form = UserRegistrationForm()
    return render(request, 'index.html', {'login_form': login_form, 'signin_form': signin_form, 'redirect_to': redirect_to})