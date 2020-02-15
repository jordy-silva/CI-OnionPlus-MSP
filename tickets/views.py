from django.shortcuts import render
from tickets.models import Ticket

# Create your views here.
def all_bugs(request):
    tickets = Ticket.objects.filter(ticket_type='BUG')
    return render(request, "tickets.html", {"tickets": tickets})

def all_features(request):
    tickets = Ticket.objects.filter(ticket_type='FEATURE')
    return render(request, "tickets.html", {"tickets": tickets, "type": "FEATURE"})
