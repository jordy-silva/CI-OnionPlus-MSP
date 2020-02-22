from django.contrib import admin
from tickets.models import Ticket, Comment, Vote

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Vote)