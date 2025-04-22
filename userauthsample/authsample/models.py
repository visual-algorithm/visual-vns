import uuid
from django.contrib.auth.models import User
from django.db import models

class Salesman(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField('備考', blank=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="salesmen")

    def __str__(self):
        return self.name

class City(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE)
    description = models.TextField('備考', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cities")
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.name
    
class Solution(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="unknown")
    description = models.TextField('備考', blank=True)
    ans = models.JSONField(default=list)
    path = models.JSONField(default=list)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)
    
    def __str__(self):
        return self.name
    
class Route(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    depot = models.ForeignKey(City, related_name='depot', on_delete=models.CASCADE)
    cities = models.ManyToManyField(City)
    salesmen = models.ManyToManyField(Salesman)
    description = models.TextField('備考', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="routes")
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.name