import functions_framework
from cloudevents.http import CloudEvent
import psycopg2
from google.cloud import aiplatform
from google.cloud import storage
from PIL import Image
import numpy as np
import io
import random
import cv2 

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def trigger_photo(cloud_event):
    """This function is triggered by a change in a storage bucket.

    Args:
        cloud_event: The CloudEvent that triggered this function.
    Returns:
        -
    """

    #Obtenemos nombre y bucket del fichero
    data            = cloud_event.data
    bucket          = data["bucket"]
    name            = data["name"]


    if name.endswith(".jpg"):
      
        #Obtenemos foto del bucket y la hacemos publica 
        client = storage.Client()
        bucket_predict = client.bucket(bucket)     
        blob_predict = bucket_predict.blob(name)
        blob_predict.make_public()
        url = blob_predict.public_url


        #Preparamos la foto para hacer la inferencia
        image_data = blob_predict.download_as_bytes()
        IMAGE_SIZE = (200,200)
        im = Image.open(io.BytesIO(image_data))
        im = im.resize(IMAGE_SIZE)
        im = np.array(im,dtype=np.float32)/255
        im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
        im = [im.tolist()]

        #inferencia de la imagen

        endpoint = aiplatform.Endpoint(endpoint_name="projects/firstdeploy-401708/locations/europe-west1/endpoints/2816605742734245888")
        result  = endpoint.predict(instances=im).predictions
        predicted_class =  str(np.argmax(result,axis=1)[0])
    
        #Guardamos el resultado en la bd
        
        connection = psycopg2.connect(
            user = 'firstdeploy',
            password = 'firstdeploy',
            host = '34.38.21.216',
            port = '5432',
            database = 'firstdeploy'
        )
        cursor = connection.cursor()

        insert_prediction_stmt = ("""
                INSERT INTO prediccion(nombre,nombre_uuid,url,idfoodclassification)
                VALUES (%s, %s, %s,%s);
                """)

        cursor.execute(insert_prediction_stmt,(name.split('/')[-1],bucket+"/"+name,url,predicted_class))
        connection.commit()

        return f"Evaluado {name} con valor {str(predicted_class)}"
       
    else:
        return "no photo .jpg"