from django.db import models
from django.conf import settings

# Create your models here.

class Cource(models.Model):
    title = models.CharField('タイトル', max_length=128)
    start = models.CharField('住所', max_length=120)
    spot1 = models.CharField('住所', max_length=120)
    spot2 = models.CharField('住所', max_length=120)
    spot3 = models.CharField('住所', max_length=120)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成者", on_delete=models.CASCADE, default=0)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.title
