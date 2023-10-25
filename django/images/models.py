from django.db import models

# Create your models here.

class Image(models.Model):
    title = models.CharField(max_length=128)
    file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title}"

class Prediccion(models.Model):
    idprediccion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, default='Default name')
    nombre_uuid = models.CharField(max_length=255, default='Default name')
    url = models.CharField(max_length=255,default='Default url')
    idfoodclassification = models.IntegerField()
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'prediccion'


class FoodClassification(models.Model):
    idfoodclassification = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=50, default='Default name')
    description = models.CharField(max_length=255, default='Default decripcion')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'foodclassification'

class FoodNutrient(models.Model):
    idfoodnutrient = models.CharField(max_length=30, primary_key=True)
    idfoodclassification = models.CharField(max_length=30, db_column='idfoodclassification')
    idmeasure = models.CharField(max_length=50, db_column='idmeasure')
    idnutrient = models.CharField(max_length=255, db_column='idnutrient')
    quantity = models.FloatField()

    def __str__(self):
        return self.idfoodnutrient
    
    class Meta:
        db_table = 'foodnutrient'



class Restaurant(models.Model):
    idrestaurant = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    rating = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.name
    
    class Meta:
            db_table = 'Restaurant'

class Product(models.Model):
    idrestaurant = models.CharField(max_length=255) 
    name = models.CharField(max_length=2000)
    description = models.CharField(max_length=2000,primary_key=True)
    idfoodclassification = models.CharField(max_length=30, db_column='idfoodclassification')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'