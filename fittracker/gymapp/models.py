from django.db import models
from django.contrib.auth.models import User


class MemberShipPlan(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - ₹{self.price} - {self.duration_days} Days"


class Member(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)
    join_date = models.DateField(auto_now_add=True)
    plan = models.ForeignKey(MemberShipPlan,on_delete=models.SET_NULL,null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Trainer(models.Model):
    
    SPECIALIZATION_CHOICES = [
        ('strength', 'Strength Training'),
        ('weight_loss', 'Weight Loss'),
        ('muscle_building', 'Muscle Building'),
        ('bodybuilding', 'Bodybuilding'),
        ('functional', 'Functional Training'),
        ('cardio', 'Cardio & Endurance'),
        ('crossfit', 'CrossFit'),
        ('yoga', 'Yoga & Flexibility'),
        ('hiit', 'HIIT Training'),
        ('sports', 'Sports Training'),
        ('group', 'Group Fitness'),
    ]

    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=150,choices=SPECIALIZATION_CHOICES)
    contact = models.CharField(max_length=10)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Attendance(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)

class Payment(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=200)