from django.db import models

# Create your models here.


class Ticket(models.Model):
    BUG = 'BUG'
    FEATURE = 'FEATURE'
    TICKET_TYPE_CHOICES = (
        (BUG, 'Bug'),
        (FEATURE, 'Feature'),
    )

    TODO = 'TODO'
    DOING = 'DOING'
    DONE = 'DONE'
    STATUS_CHOICES = (
        (TODO, 'To Do'),
        (DOING, 'Doing'),
        (DONE, 'Done'),
    )
    ticket_type = models.CharField(
        max_length=7,
        choices=TICKET_TYPE_CHOICES,
        default=FEATURE,
    )
    user_id = models.CharField(max_length=254, default="5555")
    subject = models.CharField(max_length=254)
    description = models.TextField()
    creation_ts = models.DateTimeField(auto_now_add=True)
    number_votes = models.IntegerField(default=0)
    status = models.CharField(
        max_length=5,
        choices=STATUS_CHOICES,
        default=TODO,
    )

    def __str__(self):
        return self.subject

