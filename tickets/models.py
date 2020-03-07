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
    user_id = models.IntegerField(default=5555)
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


class Comment(models.Model):
    user_id = models.IntegerField(default=0)
    ticket_id = models.IntegerField(default=0)
    description = models.TextField()
    creation_ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class Vote(models.Model):
    user_id = models.IntegerField(default=0)
    ticket_id = models.IntegerField(default=0)

class Funding(models.Model):
    user_id = models.IntegerField(default=0)
    ticket_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    payment_id = models.CharField(max_length=30)

    def __str__(self):
        return self.payment_id