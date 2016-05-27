from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime
from django.template import defaultfilters

class UserProfile(models.Model):
    # необходимое поле для связки со встроенной моделью юзера Django
    user		= models.OneToOneField(User)
    # наши добавляемые поля
    sex			= models.CharField(blank=True, max_length=6)
    birthday	= models.DateField(blank=True, null=True)
    city		= models.TextField(blank=True)

    def age(self):
        today = date.today()
        age = today.year - self.birthday.year
        if today.month < self.birthday.month:
            age -= 1
        elif today.month == self.birthday.month and today.day < self.birthday.day:
            age -= 1
        return age

    def json(self):
        return {
            'name':			self.user.first_name,
            'surname':		self.user.last_name,
            'sex':			self.sex,
            'birthdate':	self.birthday,
            'age':			self.age(),
            'city':			self.city,
        }

class Widget(models.Model):
    user		= models.ForeignKey('auth.User')
    message		= models.TextField()
    color		= models.CharField(blank=True, max_length=12, default='primary')
    image		= models.CharField(blank=True, max_length=256)
    position	= models.IntegerField(default=0)
    create_date = models.DateTimeField(default=timezone.now)
    modify_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.modify_date = timezone.now()
        self.save()

    def __str__(self):
        return self.message

    def json(self):
        return {
            'id':		self.pk,
            'message':	self.message,
            'color':	self.color,
            'image':	self.image,
            'created':	defaultfilters.date(self.create_date, 'd b, H:i'),
            'modified':	defaultfilters.date(self.modify_date, 'd b, H:i'),
        }