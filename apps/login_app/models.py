from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime, pytz
# from dateutil import tz

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        
        NAME_REGEX = re.compile(r'^[a-zA-Z-]+\s?[a-zA-Z]+$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if not NAME_REGEX.match(postData['fname']):
            errors["fname"] = "First name should contain letters only"
        if len(postData['fname']) < 2:
            errors["fname"] = "First name should be at least 2 characters"
        if not NAME_REGEX.match(postData['lname']):
            errors["lname"] = "Last name should contain letters only"
        if len(postData['lname']) < 2:
            errors["lname"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        u = User.objects.filter(email=postData["email"])
        if len(u) > 0:
            errors["email"] = "Email is already in use"
        if len(postData['pw']) < 8:
            errors["pw"] = "Password should be at least 8 characters"
        if postData["pw"] != postData["pw_conf"]:
            errors["pw"] = "Passwords don't match"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['l_email']):
            errors['l_email'] = "Invalid email address"
        u = User.objects.filter(email=postData["l_email"])
        if not u:
            errors["l_email"] = "Invalid email"
        else:
            user = u[0]
            if not bcrypt.checkpw(postData['l_pw'].encode(), user.password.encode()):
                errors["l_pw"] = "Invalid password"
        return errors

class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['dest']) < 3:
            errors["dest"] = "Destination should be at least 3 characters"
        if not postData['dest'].isalpha():
            errors["dest"] = "Destination should contain letters only"
        if len(postData['plan']) < 3:
            errors["plan"] = "Plan should be at least 3 characters"
        if len(postData['start_date']) < 1 or len(postData['end_date']) < 1:
            errors["start_date"] = "Date shouldn't be blank"
        else:
            current_time = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
            start_date = datetime.datetime.strptime(postData['start_date'], "%Y-%m-%d").replace(tzinfo=pytz.UTC)
            end_date = datetime.datetime.strptime(postData['end_date'], "%Y-%m-%d").replace(tzinfo=pytz.UTC)
            if current_time > start_date:
                errors["start_date"] = "Start date should be future date" 
            if start_date > end_date:
                errors["end_date"] = "End date should be future date" 
        #     if  postData['start_date'] > postData['end_date']:
        #         errors["start_date"] = "Start date should be before end date" 
        if len(postData['end_date']) < 1:
            errors["end_date"] = "End date shouldn't be blank"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __repr__(self):
        return f"<User object: {self.email} ({self.id})>"

class Trip(models.Model):
    owner = models.IntegerField()
    users = models.ManyToManyField(User, related_name="trips")
    dest = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

    def __repr__(self):
        return f"<Trip object: {self.dest} ({self.id})>"
