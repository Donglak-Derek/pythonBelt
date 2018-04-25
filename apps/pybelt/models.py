from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
import bcrypt
import re
from datetime import date
from time import strftime

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if(len(postData['name']) < 3 ):
            errors['name'] = 'Name should have at least 3 charators'
        if(len(postData["username"]) < 3):
            errors['username'] = "Username should have at least 3 charators"

        if len(self.filter(username = postData['username'])) != 0: 
            errors['repeat'] = "Username already exists"

        if (len(postData['password']) < 8):
            errors['password'] = "password must have at least 8 charators"
        if postData['password'] != postData['cpassword']:
            errors['mismatch'] = "password do not match"
        
        if len(errors) == 0:
            userpassword = postData['password']
            userpassword = userpassword.encode('utf-8')
            hashpw = bcrypt.hashpw(userpassword, bcrypt.gensalt())
            return hashpw

        return errors

    def login_validator(self, postData):
        errors = {}
        if (len(self.filter(username = postData['username'])) == 0 ):
            errors['nousername'] = "Username doesnot exists"
        else:
            u = self.filter(username = postData['username'])[0]
            userpassword = postData['password']
            if not bcrypt.checkpw(userpassword.encode('utf-8'), u.password.encode()):
                errors['password'] = "Incorrect password"
        
        if (len(errors) != 0):
            return errors
        return self.filter(username = postData['username'])[0]

class TravelManager(models.Manager):
    def Travel_regi_validator(self, postData):
        errors = {}
        # print postData, "postData"
        if(len(postData['destination']) < 3 ):
            errors['quote_by'] = 'Quote should be at least 3 charators'
        if postData['start_day'] < date.today().strftime("%Y-%m-%d"):
            errors['start_day'] = "starting day should be in future"
        if postData['start_day'] > postData['end_day']:
            errors['end_day'] = "Stating Day shoul not be before the End day"
        
        if (len(errors) != 0):
            return errors

        return errors


#ManyToMany and OneToMany
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    desc = models.TextField()
    start_day = models.DateField()
    end_day = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #for the uploaders name
    # uploader = models.ForeignKey(User, related_name="uploaded_quotes")
    users = models.ManyToManyField(User, related_name = "travels")
    objects = TravelManager()
   
