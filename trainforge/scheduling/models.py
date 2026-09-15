from django.db import models
from users.models import Trainer, Client


class Appointment(models.Model):

    SESSION_TYPE_CHOICES = [
        ('strength_training', 'Strength Training'),
        ('hiit_cardio', 'HIIT & Cardio'),
        ('flexibility_mobility', 'Flexibility & Mobility'),
        ('weight_loss', 'Weight Loss'),
        ('consultation', 'Consultation'),
    ]

    DURATION_CHOICES = [
        (60, '60 Minutes'),
        (90, '90 Minutes'),
        (120, '120 Minutes'),
    ]

    REPEAT_CHOICES = [
        ('none', 'No Repeat'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-Weekly'),
        ('monthly', 'Monthly'),
    ]

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    session_type = models.CharField(
        max_length=50,
        choices=SESSION_TYPE_CHOICES
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    duration = models.PositiveIntegerField(
        choices=DURATION_CHOICES,
        default=60
    )

    repeat = models.CharField(
        max_length=20,
        choices=REPEAT_CHOICES,
        default='none'
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    is_completed = models.BooleanField(default=False)

    is_cancelled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.client} - {self.appointment_date} {self.appointment_time}"