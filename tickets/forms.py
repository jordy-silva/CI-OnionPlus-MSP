from django import forms
from tickets.models import Ticket, Comment


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('ticket_type', 'subject', 'description')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('user_id', 'ticket_id', 'description')
        widgets = {
            'user_id': forms.HiddenInput(),
            'ticket_id': forms.HiddenInput(),
            'description': forms.Textarea(attrs={'rows':100, 'cols':15})
            }
