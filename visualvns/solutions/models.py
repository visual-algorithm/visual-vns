from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

# Create your models here.

class Salesman(models.Model):
    salesman_name = models.CharField(max_length=32)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成者", on_delete=models.CASCADE)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    update_at = models.DateTimeField("更新日", auto_now=True)
    
    def __str__(self):
        return self.salesman_name

class City(models.Model):
    city_name = models.CharField('タイトル', max_length=128)
    address = models.TextField('住所', blank=True)
    salesman = models.ForeignKey(Salesman, related_name="salesman", on_delete=models.CASCADE)
    description = models.TextField('備考', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成者", on_delete=models.CASCADE)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    update_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.city_name

class Route(models.Model):
    route_name = models.CharField(max_length=32)
    route_description = models.TextField('注意点', blank=True)
    depot = models.ForeignKey(City, related_name='depot', on_delete=models.CASCADE)
    cities = models.ManyToManyField(City, related_name='routes')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成者", on_delete=models.CASCADE)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    update_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.route_name