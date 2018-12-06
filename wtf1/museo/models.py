# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Entries(models.Model):
    @property
    def user(self):
        return User.objects.get(pk=self.user_id)

#this model was to store top 5 users seperately in the model
#used for debugging
class top5users(models.Model):
	username=models.CharField(max_length=30)
	totalup=models.IntegerField()
	totaldo=models.IntegerField()
	totalpo=models.IntegerField()

#this model is seperately created and is the same as post_list table on the database.
#this is used to extract information for rss feed
class latest_posts(models.Model):
	pid=models.IntegerField()
	uid=models.IntegerField()
	upvotes=models.IntegerField()
	downvotes=models.IntegerField()
	content=models.CharField(max_length=2451)
	


