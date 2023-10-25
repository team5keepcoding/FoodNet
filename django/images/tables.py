import django_tables2 as tables
from django.db import connection

from images.models import Image,FoodClassification,FoodNutrient,Product,Restaurant


class ImageTable(tables.Table):
    preview = tables.TemplateColumn('<img src="{{record.file.url}}" class="img-fluid" height="100" width="100">')

    class Meta:
        model = Image
        orderable = False

class FoodClassificationTable(tables.Table):

    class Meta:
        model = FoodClassification
        orderable = False
        fields = ['name']

    name = tables.Column(verbose_name='Nombre')

class FoodNutrientTable(tables.Table):

    class Meta:
        model = FoodNutrient
        fields = ['idnutrient', 'quantity']

    # Puedes personalizar el contenido de las celdas si es necesario
    idnutrient = tables.Column(verbose_name='Nutriente')
    quantity = tables.Column(verbose_name='Cantidad(gramos)')

# class ProductTable(tables.Table):
    
#     class Meta:
#         model = Product
#         fields = ['name','idrestaurant', 'description']

#     # Puedes personalizar el contenido de las celdas si es necesario
#     idrestaurant = tables.Column(verbose_name='Restaurante')
#     name = tables.Column(verbose_name='Nombre del Plato')
#     description = tables.Column(verbose_name='Descripcion')

class ProductTable(tables.Table):
    name = tables.Column(verbose_name='Nombre del Plato')
    description = tables.Column(verbose_name='Descripción')
    restaurant_name = tables.Column(verbose_name='Restaurante')


