from django import forms
from tickets.models import Ticket, Comment


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('ticket_type', 'subject', 'description')
        labels = {
            'ticket_type': 'Type of Request',
            'subject': 'Tittle',
            'description': 'Details',
        }
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Enter a short tittle here'})}


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('user_name', 'ticket_id', 'description')
        widgets = {
            'user_name': forms.HiddenInput(),
            'ticket_id': forms.HiddenInput(),
            }
