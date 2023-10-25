import requests
import pandas as pd
pd.set_option("display.max_rows", 1000)
df = pd.DataFrame(columns=['text', 'label', 'knownAs','ENERC_KCAL','PROCNT','FAT','FIBTG'])


#Descarga de datos de la app edamam api


class_name = {'Baked Potato': 0,
 'Crispy Chicken': 1,
 'Donut': 2,
 'Fries': 3,
 'Hot Dog': 4,
 'Sandwich': 5,
 'Tacos': 6,#taco
 'Taquitos': 7,#taquito
 'apple_pie': 8,
 'burger': 9,
 'butter_naan': 10,
 'chai': 11,
 'chapati': 12,
 'cheesecake': 13,
 'chicken_curry': 14,
 'chole_bhature': 15,
 'dal_makhani': 16,
 'fried_rice': 17,
 'ice_cream': 18,
 'idli': 19,
 'jalebi': 20,
 'rolls': 21,#kaathi_rolls
 'kadai_paneer': 22,
 'masala_dosa': 23,
 'momos': 24,
 'omelette': 25,
 'pakora': 26, #pakode
 'pav_bhaji': 27,
 'pizza': 28,
 'sushi': 29}

for name_food in class_name.keys():
    namefood = name_food.replace("_", " ")
    params = {
        'app_id': 'def66646',
        'app_key': 'fb8b403e45f204f2ffebed4c152b9055',
        'ingr': namefood,
        'nutrition-type':'cooking'
    }
    url = f"https://api.edamam.com/api/food-database/v2/parser?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    response = requests.get(url)

    if response.status_code == 200:
        # Analizar la respuesta JSON
        data = response.json()
        if(data['parsed'] != []):
        
            new_row = pd.DataFrame({'text':      [data['text']], 
                                    'label':     [data['parsed'][0]["food"]["label"]],
                                    'knownAs':   [data['parsed'][0]["food"]["knownAs"]],
                                    'ENERC_KCAL':[str(round(data['parsed'][0]["food"]["nutrients"]["ENERC_KCAL"], 2))], 
                                    'PROCNT':    [str(round(data['parsed'][0]["food"]["nutrients"]["PROCNT"], 2))],
                                    'FAT':       [str(round(data['parsed'][0]["food"]["nutrients"]["FAT"], 2))], 
                                    'FIBTG':     [str(round(data['parsed'][0]["food"]["nutrients"]["FIBTG"], 2))  if ("FIBTG" in data['parsed'][0]["food"]["nutrients"]) else 0],
                                    'CHOCDF':    [str(round(data['parsed'][0]["food"]["nutrients"]["CHOCDF"], 2)) if ("CHOCDF" in data['parsed'][0]["food"]["nutrients"]) else 0]
                                    })
            df = pd.concat([df,new_row], ignore_index=True)          
            if (namefood.lower() == data['parsed'][0]["food"]["label"].lower()) and (namefood.lower() == data['parsed'][0]["food"]["knownAs"].lower()):
                continue
        print("*****************"+str(len(data['hints'])))
        for tam in range(0,len(data['hints'])):
            new_row = pd.DataFrame({'text':      [data['text']], 
                                    'label':     [data['hints'][tam]["food"]["label"]],
                                    'knownAs':   [data['hints'][tam]["food"]["knownAs"]],
                                    'ENERC_KCAL':[str(round(data['hints'][tam]["food"]["nutrients"]["ENERC_KCAL"], 2))], 
                                    'PROCNT':    [str(round(data['hints'][tam]["food"]["nutrients"]["PROCNT"], 2))],
                                    'FAT':       [str(round(data['hints'][tam]["food"]["nutrients"]["FAT"], 2))], 
                                    'FIBTG':     [str(round(data['hints'][tam]["food"]["nutrients"]["FIBTG"], 2))  if ("FIBTG" in data['hints'][tam]["food"]["nutrients"]) else 0],
                                    'CHOCDF':    [str(round(data['hints'][tam]["food"]["nutrients"]["CHOCDF"], 2)) if ("CHOCDF" in data['hints'][tam]["food"]["nutrients"]) else 0]
                                    })

            df = pd.concat([df,new_row], ignore_index=True)
            if (namefood.lower() == data['hints'][tam]["food"]["label"].lower()) and (namefood.lower() == data['hints'][tam]["food"]["knownAs"].lower()):
                break
    else:
        print("Error en la solicitud:", response.status_code)

df = df[df['text'].str.lower() == df['label'].str.lower()][df['label'].str.lower() == df['knownAs'].str.lower()]
df =df[['text','ENERC_KCAL','PROCNT','FAT','FIBTG','CHOCDF']]
df =df.rename(columns={"text": "Nombre", "ENERC_KCAL": "Caloria", "PROCNT": "Proteina",'FAT':'Grasa','FIBTG':'Fibra','CHOCDF':'Carbohidrato'})

df.to_csv("EdamamApi.csv",index=False,sep=";")