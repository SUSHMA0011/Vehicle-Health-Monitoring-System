from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class user(models.Model):
    firstname = models.CharField(max_length=25)
    license = models.CharField(max_length=25)
    contact = models.CharField(max_length=10)
    password = models.CharField(max_length=128)  # Store hashed passwords
    is_active = models.IntegerField(default=0)

   
class Tyre(models.Model):
    vnumber=models.CharField(max_length=10)
    driver_name = models.CharField(max_length=100)
    tyrenumber= models.CharField(max_length=100)
    tyre_type = models.CharField(max_length=100)
    date = models.DateField()
    kilometer = models.FloatField()
    bill_number = models.CharField(max_length=100)
    amount = models.FloatField()
    tyreimage=models.ImageField(null=True, blank=True, upload_to="tyreimage/")


class fuel(models.Model):
    vnumber=models.CharField(max_length=10)
    driverName = models.CharField(max_length=100)
    date = models.DateField()
    billNumber = models.CharField(max_length=100)
    fuelStation = models.CharField(max_length=100)
    liter = models.FloatField()
    amount= models.FloatField()
    readings= models.FloatField()
    fuelimage=models.ImageField(null=True,blank=True,upload_to="fuelimage/")   


class Mileage(models.Model):
    lastFilledKilometer = models.CharField(max_length=100)
    presentKilometer = models.CharField(max_length=100)
    numberOfLiter = models.CharField(max_length=100)
    # calculatedMileage = models.CharField(max_length=100)



class admin(models.Model):
    name=models.CharField(max_length=25)
    password=models.CharField(max_length=10)


class vehicle(models.Model):
    name=models.CharField(max_length=25)
    model=models.CharField(max_length=25)
    vnumber=models.CharField(max_length=10)
    cnumber=models.CharField(max_length=17)
       

     



    