from django.db import models

import re

from datetime import date
from datetime import datetime
# Create y

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # --------name validation ----------
        if len(postData['firstNameLabel']) < 2:
            errors['firstNameLabel'] = "First name should not be less than 2 characters"
        if len(postData['lastNameLabel']) < 2:
            errors['lastNameLabel'] = "Last name should not be less than 2 characters"
        # --------Email validation ----------
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['emailLabel']):
                errors['emailLabel'] = "Invalid email address"
        # --------password validation ----------       
        if len(postData['passwordLabel']) < 8:
            errors['passwordLabel'] = "Password should be at least than 8 characters"
        if postData['passwordLabel'] != postData['passwordConfirmLabel']:
            errors['pw_confirm'] = "please ensure the password matches confirmation"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    password = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

#Validation for entering trips here
class TripManager(models.Manager):
    def basic_validator_two(self, postData):
        errors = {}
        if len(postData['destinationLabel']) < 3:
            errors['destinationLabel'] = "Destination must consist of 3 characters"
        if len(postData['startDateLabel']) < 10:
            errors['startDateLabel'] = "Start date must be entered"
        # elif datetime.strptime(postData['startDateLabel'], '%Y-%m-%d') > datetime.now():
        #     errors['startDateLabel'] = "need current date"
        if len(postData['endDateLabel']) < 10:
            errors['endDateLabel'] = "End date must be entered"
        # elif datetime.strptime(postData['endDateLabel'], '%Y-%m-%d') > datetime.now():
        #     errors['endDateLabel'] = "need current date"
        if len(postData['planLabel']) <3:
            errors['planLabel'] = "The plan must be provided at least 10 characters"
        
        return errors


class Trip(models.Model):
    destination = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()

    owner = models.ForeignKey(
        User,
        related_name="trips",
        on_delete=models.CASCADE  
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager() 