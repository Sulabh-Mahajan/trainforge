from django.db import models
from users.models import Trainer, Client
from training.models import Exercise


class ClientExerciseProgress(models.Model):

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='exercise_progress'
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='client_progress'
    )

    updated_by = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='progress_updates'
    )

    benchmark_value = models.PositiveIntegerField()

    progress_date = models.DateField()

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-progress_date']

    def __str__(self):
        return (
            f"{self.client} - "
            f"{self.exercise} - "
            f"{self.benchmark_value}"
        )