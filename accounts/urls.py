from django.conf.urls import url, include
from accounts.views import login, logout, signup

urlpatterns = [
    url(r'^login/', login, name="login"),
    url(r'^logout/', logout, name="logout"),
    url(r'^signup/', signup, name="signup"),
]
