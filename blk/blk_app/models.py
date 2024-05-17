from django.db import models

# Create your models here.

# Create your models here.
class Requests(models.Model):
    r_id=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    user_type=models.CharField(max_length=255)
    mobile=models.CharField(max_length=255)
    p_address=models.CharField(max_length=255)


class Patient(models.Model):
    u_id=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    mobile=models.CharField(max_length=255)
    p_address=models.CharField(max_length=255)

class Record(models.Model):
    r_id=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=255)
    c_date=models.CharField(max_length=255)
    c_time=models.CharField(max_length=255)
    result=models.CharField(max_length=255)
