from django import forms
from tickets.models import Ticket


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('ticket_type', 'subject', 'description')