from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Info(models.Model):
    name = models.CharField(max_length=60)
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    days = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    cycle = models.PositiveIntegerField(validators=[MinValueValidator(10), MaxValueValidator(100)])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Hello(models.Model):
    name = models.CharField(max_length=50)
