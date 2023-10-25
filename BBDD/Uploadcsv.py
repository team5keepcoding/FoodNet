from google.cloud import storage

### Subir fichero .csv al bucker de GCP

def uploadfilecsv(project_id,
               bucket_name,
               file,
               local_path,
               remote_path):
    
    local_file_path = f'{local_path}{file}'

    remote_file_name = f'{remote_path}{file}'

    # Crea una instancia del cliente de Google Cloud Storage.
    client = storage.Client(project=project_id)

    # Accede al bucket especificado.
    bucket = client.get_bucket(bucket_name)

    # Carga el archivo en el bucket.
    blob = bucket.blob(remote_file_name)

    if blob.exists():
        return f"El archivo gs://{bucket_name}/{remote_file_name} ya existe en el bucket."
    else:
        blob.upload_from_filename(local_file_path)
        return f"Archivo {local_file_path} \nsubido a gs://{bucket_name}/{remote_file_name}"

# print(
#         uploadfilecsv( project_id   = 'id proyecto',
#                     bucket_name     = 'nombre bucket',
#                     file            = 'nombre.fichero',
#                     local_path      = 'C:/ruta/al/archivo/local/' ,
#                     remote_path     = 'CarpetaGCP/')
# )

print(
        uploadfilecsv( project_id   = 'firstdeploy-401708',
                    bucket_name     = 'firstdeploy1010',
                    file            = 'EDA.ipynb',
                    local_path      = 'C:/Users/Bart/Desktop/final/Datasets/EdamamApi/' ,
                    remote_path     = 'Datasets/')
)