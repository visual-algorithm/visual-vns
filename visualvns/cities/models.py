from django.db import models
from django.conf import settings

# Create your models here.

class Cities(models.Model):
    title = models.CharField('タイトル', max_length=128)
    depot = models.TextField('拠点', blank=True)
    city1 = models.TextField('都市1', blank=True)
    