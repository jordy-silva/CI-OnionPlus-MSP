from django.shortcuts import render, redirect, get_object_or_404
from tickets.models import Ticket
from tickets.forms import TicketForm

# Create your views here.
def all_bugs(request):
    """ Create a view to show all Bug tickets """
    tickets = Ticket.objects.filter(ticket_type='BUG')
    return render(request, "tickets.html", {"tickets": tickets})

def all_features(request):
    """ Create a view to show all feature tickets """
    tickets = Ticket.objects.filter(ticket_type='FEATURE')
    return render(request, "tickets.html", {"tickets": tickets, "type": "FEATURE"})

def create_ticket(request, pk=None):
    """ Create a view to show all feature tickets """
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect(all_features)
    else:
        form = TicketForm(instance=ticket)
        return render(request, 'ticketform.html', {'form': form})