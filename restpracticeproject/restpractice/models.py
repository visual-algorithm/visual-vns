import uuid
from django.db import models
from django.conf import settings

# Create your models here.

class Salesman(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField('備考', blank=True)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成者", on_delete=models.CASCADE)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.name
    
class City(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE)
    description = models.TextField('備考', blank=True)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成者", on_delete=models.CASCADE)
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
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成者", on_delete=models.CASCADE)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.name
    
class Solution(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="unknown")
    ans = models.JSONField(default=list)
    path = models.JSONField(default=list)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    
# class Result(models.Model):
#     uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     ans = models.JSONField(default=list)
#     created_at = models.DateTimeField("作成日", auto_now_add=True)

# class Item(models.Model):
#     uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100, default="unknown")
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成者", on_delete=models.CASCADE)


# class City(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Salesman(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Route(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100)
#     cities = models.ManyToManyField(City, related_name="routes")

#     def __str__(self):
#         return self.name
