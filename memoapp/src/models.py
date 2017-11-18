# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models


class Users(models.Model):
	name = models.CharField(max_length=50)

# Create your models here.
class Memo(models.Model):
	date = models.DateField(default=datetime.date.today, null=False)
	meeting_with = models.ManyToManyField(Users)
	meeting_notes = models.TextField(blank=True)
	image_path = models.CharField(max_length=50, null=True)
