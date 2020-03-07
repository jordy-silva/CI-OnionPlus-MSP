from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from tickets.models import Ticket, Comment, Vote
from tickets.forms import TicketForm, CommentForm
from accounts.forms import UserLoginForm, UserRegistrationForm


# Create your views here.


def all_bugs(request):
    """ Create a view to show all Bug tickets """
    tickets = Ticket.objects.filter(ticket_type='BUG')
    voted = Vote.objects.filter(user_id=request.user.id).values_list('ticket_id', flat=True)
    login_form = UserLoginForm()
    signin_form = UserRegistrationForm()
    context = {
        "tickets": tickets,
        "voted": voted,
        "type": "BUG",
        "login_form": login_form,
        "signin_form": signin_form
    }
    return render(request, "tickets.html", context)


def all_features(request):
    """ Create a view to show all feature tickets """
    tickets = Ticket.objects.filter(ticket_type='FEATURE')
    login_form = UserLoginForm()
    signin_form = UserRegistrationForm()
    context = {
        "tickets": tickets,
        "type": "FEATURE",
        "login_form": login_form,
        "signin_form": signin_form
    }
    return render(request, "tickets.html", context)


@login_required(login_url='/')
def create_ticket(request, ticket_type):
    """ Create a view to show all feature tickets """
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket added")
            if ticket_type == "FEATURE":
                return redirect(all_features)
            else:
                return redirect(all_bugs)
    else:
        form = TicketForm()
        form.fields["ticket_type"].initial = ticket_type
        return render(request, 'ticketform.html', {'form': form})


@login_required()
def add_comment(request, pk, uid):
    """ Create a view to allow adding comments to a ticket """
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment added")
            return redirect('show_comments', pk)
    else:
        form = CommentForm(initial={'ticket_id': pk, 'user_id': uid})
        return render(request, "commentform.html", {'ticket': ticket, 'form': form})


def show_comments(request, pk):
    """ Create a view that shows a ticket and all it's comments """
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    comments = Comment.objects.filter(ticket_id=pk)
    return render(request, "showcomments.html", {'ticket': ticket, 'comments': comments})


@login_required()
def thumb_up(request, pk):
    """ Allow for a user to upvote a ticket """
    vote = Vote()
    vote.user_id = request.user.id
    vote.ticket_id = pk
    vote.save()
    ticket = get_object_or_404(Ticket, pk=pk) if pk else None
    ticket.number_votes = Vote.objects.filter(ticket_id=pk).count()
    ticket.save()
    messages.success(request, "Vote added")
    return redirect('show_comments', pk)
