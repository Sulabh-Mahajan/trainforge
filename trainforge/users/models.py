from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Subscription(models.Model):
    PLAN_CHOICES = [
        ('free',  'Free'),
        ('pro',   'Pro'),
        ('elite', 'Elite'),
    ]
    plan_name     = models.CharField(max_length=20, choices=PLAN_CHOICES)
    max_customers = models.IntegerField()
    ai_included   = models.BooleanField(default=False)

class Trainer(models.Model):
    CERTIFICATION_CHOICES = [
        ('cert3', 'Certificate III in Fitness'),
        ('cert4', 'Certificate IV in Fitness'),
        ('acsm',  'ACSM Certified Personal Trainer'),
        ('nasm',  'NASM-CPT'),
        ('ace',   'ACE Personal Trainer'),
        ('other', 'Other'),
    ]

    user                  = models.OneToOneField(User, on_delete=models.CASCADE)
    experience            = models.CharField(max_length=20)
    doj                   = models.DateField()
    is_archive            = models.BooleanField(default=False)
    primary_certification = models.CharField(max_length=50, choices=CERTIFICATION_CHOICES, blank=True, null=True)
    subscription          = models.ForeignKey(Subscription, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class TrainerSpecialization(models.Model):
    SPECIALIZATION_CHOICES = [
        ('strength',    'Strength & Conditioning'),
        ('weight_loss', 'Weight Loss'),
        ('hiit',        'HIIT & Cardio'),
        ('flexibility', 'Flexibility & Mobility'),
        ('sports',      'Sports Performance'),
        ('rehab',       'Rehabilitation'),
        ('nutrition',   'Nutrition Coaching'),
        ('group',       'Group Training'),
    ]

    trainer        = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)

    def __str__(self):
        return f"{self.trainer} - {self.specialization}"

class Client(models.Model):
    SEX_CHOICES = [
        ('male',   'Male'),
        ('female', 'Female'),
        ('other',  'Other'),
    ]
    first_name            = models.CharField(max_length=100)
    last_name             = models.CharField(max_length=100)
    email                 = models.EmailField()
    phone                 = models.CharField(max_length=20)
    trainer               = models.ForeignKey(Trainer, on_delete=models.PROTECT)
    sex                   = models.CharField(max_length=10, choices=SEX_CHOICES)
    age                   = models.IntegerField()
    height                = models.DecimalField(max_digits=5, decimal_places=2)
    weight                = models.DecimalField(max_digits=5, decimal_places=2)
    initial_fitness_level = models.TextField()
    created_at            = models.DateTimeField(auto_now_add=True)
    is_archive            = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

