from django.shortcuts import render
from accounts.forms import UserLoginForm

# Create your views here.
def index(request):
    """Render the index page"""
    login_form = UserLoginForm()
    return render(request, 'index.html', {'login_form': login_form})