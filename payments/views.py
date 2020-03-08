from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from tickets.models import Funding, Ticket
import stripe
import json

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def create_payment(request):
    data = json.loads(request.body)
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=data['amount'],
        currency=data['currency'],
        metadata={'Onion_User_ID': request.user.id, 'ticket': data['ticket']},
    )

    try:
        # Send publishable key and PaymentIntent details to client
        return JsonResponse({'publishableKey': settings.STRIPE_PUBLISHABLE_KEY, 'clientSecret': intent.client_secret, 'intentID': intent.id})
    except Exception as e:
        return JsonResponse(error=str(e)), 403


@csrf_exempt
def update_payment(request):
    data = json.loads(request.body)
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.modify(
        data['intentID'],
        amount=data['amount']
    )

    try:
        # Send publishable key and PaymentIntent details to client
        return JsonResponse({'publishableKey': settings.STRIPE_PUBLISHABLE_KEY, 'clientSecret': intent.client_secret})
    except Exception as e:
        return JsonResponse(error=str(e)), 403


@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        pk = event.data.object.metadata.ticket
        funding = Funding()
        funding.user_id = event.data.object.metadata.Onion_User_ID
        funding.ticket_id = pk
        funding.amount = event.data.object.amount
        funding.payment_id = event.data.object.id
        funding.save()
        ticket = get_object_or_404(Ticket, pk=pk) if pk else None
        amount = Funding.objects.filter(ticket_id=pk).aggregate(Sum('amount'))
        ticket.number_votes = amount.get("amount__sum")
        ticket.save()

    else:
        # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)
