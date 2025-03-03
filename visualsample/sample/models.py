from django.db import models

# Create your models here.

class Salesman(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=100)
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Route(models.Model):
    name = models.CharField(max_length=100)
    cities = models.ManyToManyField(City)
    salesmen = models.ManyToManyField(Salesman)

    def __str__(self):
        return self.name