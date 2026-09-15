from django.db import models
from users.models import Trainer, Client

# Create your models here.
class TrainingPlan(models.Model):

    GOAL_CHOICES = [
        ('strength', 'Strength'),
        ('weight_loss', 'Weight Loss'),
        ('cardio', 'Cardio'),
        ('mobility', 'Mobility'),
        ('rehabilitation', 'Rehabilitation'),
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all_levels', 'All Levels'),
    ]

    DAYS_PER_WEEK_CHOICES = [
    (1, '1 Day'),
    (2, '2 Days'),
    (3, '3 Days'),
    (4, '4 Days'),
    (5, '5 Days'),
    (6, '6 Days'),
    (7, '7 Days'),  
    ]

    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='training_plans')
    plan_name = models.CharField(max_length=100)
    goal = models.CharField(max_length=30, choices=GOAL_CHOICES)
    duration_weeks = models.PositiveIntegerField()
    days_per_week = models.PositiveIntegerField(choices=DAYS_PER_WEEK_CHOICES)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    short_description = models.TextField()

    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan_name


class Exercise(models.Model):

    training_plan = models.ForeignKey(
        TrainingPlan,
        on_delete=models.CASCADE,
        related_name='exercises'
    )

    exercise_name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField()
    reps_duration = models.CharField(max_length=50)

    rest_seconds = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    weight = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.exercise_name


class ClientTrainingPlan(models.Model):

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='assigned_training_plans'
    )

    training_plan = models.ForeignKey(
        TrainingPlan,
        on_delete=models.CASCADE,
        related_name='client_assignments'
    )

    assigned_by = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='assigned_training_plans'
    )

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)

    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.training_plan}"