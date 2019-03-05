from django.db import models


class Ticket(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    text = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='tickets', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created', 'owner')
