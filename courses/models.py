from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    min_students = models.IntegerField()
    max_students = models.IntegerField()

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video_link = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')

class Group(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='groups')
    students = models.ManyToManyField(User, related_name='group_set')

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)