from django.db import models
from django.conf import settings

# Create your models here.

class Route(models.Model):
    title = models.CharField('タイトル', max_length=128)
    depot = models.CharField('拠点', max_length=120)
    spot1 = models.CharField('訪問1', max_length=120)
    spot2 = models.CharField('訪問2', max_length=120)
    spot3 = models.CharField('訪問3', max_length=120)
    spot4 = models.CharField('訪問4', max_length=120)
    spot5 = models.CharField('訪問5', max_length=120)
    spot6 = models.CharField('訪問6', max_length=120)
    spot7 = models.CharField('訪問7', max_length=120)
    spot8 = models.CharField('訪問8', max_length=120)
    spot9 = models.CharField('訪問9', max_length=120)
    spot10 = models.CharField('訪問10', max_length=120)
    spot11 = models.CharField('訪問11', max_length=120)
    spot12 = models.CharField('訪問12', max_length=120)
    spot13 = models.CharField('訪問13', max_length=120)
    spot14 = models.CharField('訪問14', max_length=120)
    spot15 = models.CharField('訪問15', max_length=120)
    spot16 = models.CharField('訪問16', max_length=120)
    spot17 = models.CharField('訪問17', max_length=120)
    spot18 = models.CharField('訪問18', max_length=120)
    spot19 = models.CharField('訪問19', max_length=120)
    spot20 = models.CharField('訪問20', max_length=120)
    description = models.TextField('備考', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成者", on_delete=models.CASCADE)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.title