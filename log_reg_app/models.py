from django.db import models
import bcrypt, re
from django.utils import timezone
from datetime import datetime


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        email = postData.get('email')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if User.objects.filter(email=email).exists():
            errors["email_exist"] = "This email have been already used"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_invalid'] = "Invalid email address!"
        if len(postData['name']) < 3:
            errors["name"] = "Name should be at least 3 characters"
        if len(postData['alias']) < 3:
            errors["alias"] = "Alias should be at least 3 characters"
        if len(postData['password']) < 8:
            errors["password_char"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirmation']:
            errors["password_match"] = "Password doesn't match!"
        return errors
    
    def validator_pwd(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user:
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors["password_wrong"] = "Incorrect email/password"
        else:
            errors["no_user"] = "No user registred with this email"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


