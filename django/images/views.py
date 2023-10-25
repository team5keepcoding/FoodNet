
# Create your views here.
import logging
from django.http import Http404
from django.conf import settings
import uuid
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from images.forms import UploadForm
from images.models import Image,Prediccion,FoodClassification,FoodNutrient,Product
from images.tables import ImageTable,FoodClassificationTable,FoodNutrientTable,ProductTable
from google.cloud import storage
import time

logger = logging.getLogger(__name__)


def index_view(request):

    upload_form = UploadForm()

    return render(request, 'images/index.html', {
        'upload_form': upload_form,
    })


@require_http_methods(["POST"])
def upload_view(request):
    upload_form = UploadForm(data=request.POST, files=request.FILES)

    if upload_form.is_valid():
        # Genera un identificador único
        unique_identifier = str(uuid.uuid4())
        # Guarda el formulario sin realizar una confirmación para obtener la instancia del modelo Image
        image = upload_form.save(commit=False)


        # Utiliza el identificador único para nombrar el archivo en GCS
        client = storage.Client()
        bucket = client.bucket(settings.GS_BUCKET_NAME)
        gcs_filename = f'images/{unique_identifier}.jpg'
        blob = bucket.blob(gcs_filename)
        blob.upload_from_file(request.FILES['file'])

        # Asigna el nombre del archivo en GCS al campo 'file' del modelo Image
        image.file = gcs_filename
        print("Prueba gcs_filename:" ,gcs_filename)

        # Guarda la instancia en la base de datos
        image.save()

        request.session['gcs_filename'] = gcs_filename
        request.session.save()

        # Redirige a la vista que muestra la tabla de imágenes
        return HttpResponseRedirect('/image-table/')
    else:
        logger.warning("Something went wrong with uploading the file.")
        logger.warning(request.POST)
        logger.warning(request.FILES)
        # En caso de error, regresa a la vista del formulario de carga
        return render(request, 'images/index.html', {'upload_form': upload_form})

def image_table_view(request):
    gcs_filename = request.session.get('gcs_filename')
    #gcs_filename='webdjango-400208_bucket1/images/sushi.jpg'
    # Mostrar la tabla de imágenes
    try:
        # Intenta seleccionar la fila que coincide con gcs_filename
        image = Image.objects.get(file=gcs_filename)
    except Image.DoesNotExist:
        # Si no se encuentra una imagen con ese nombre de archivo, puedes manejar el error adecuadamente
        raise Http404("La imagen solicitada no existe")
    # images = Image.objects.all()
    # image_table = ImageTable(images)
    # Crea una tabla de imágenes solo con la imagen seleccionada
    image_table = ImageTable([image])

    name_uuid=f'webdjango-400208_bucket1/{gcs_filename}'

    time.sleep(7)
    prediction_obj = Prediccion.objects.get(nombre_uuid=name_uuid)
    print("Prueba prediccion:" ,name_uuid)
    foodclassification = prediction_obj.idfoodclassification
    print("Prueba idfoodclassification:" ,foodclassification)
    FoodClassification_obj = FoodClassification.objects.get(idfoodclassification =foodclassification)
    Food_table = FoodClassificationTable([FoodClassification_obj])

    FoodNutrient_obj = FoodNutrient.objects.filter(idfoodclassification =foodclassification)
    Nutrient_table = FoodNutrientTable(FoodNutrient_obj)


    query = '''
        SELECT p.name, p.description, r.name as restaurant_name
        FROM product p
        INNER JOIN restaurant r ON p.idrestaurant = r.idrestaurant
        WHERE p.idfoodclassification = %s
    '''
    
    Product_table_filter = Product.objects.raw(query, [foodclassification])
    Product_table=ProductTable(Product_table_filter)

    print("Prueba idfoodclassification:" ,foodclassification)
    return render(request, 'images/image_table.html', {'image_table': image_table, 'food_table': Food_table, 'nutrient_table': Nutrient_table,'product_table': Product_table})