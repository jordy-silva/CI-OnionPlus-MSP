from django.conf.urls import url, include
from payments.views import create_payment, update_payment, webhook

urlpatterns = [
    url(r'^create-payment-intent', create_payment, name="create_payment"),
    url(r'^update-payment-intent', update_payment, name="update_payment"),
    url(r'^webhook', webhook, name="webhook"),
]
