import pandas as pd

data = pd.read_csv("1.EdamamApi.csv",sep=";")
print(data.columns)


# Inserts para la tabla nutrientes y food

print("Insert en Nutrientes")
rows = []
for fil in range(0,data.shape[0]):
    text = f"('{data.loc[fil]['Nombre']}_ENERC_KCAL',{fil},'G','Calorias',{data.loc[fil]['Caloria']}),"
    rows.append(text)
    text = f"('{data.loc[fil]['Nombre']}_PROCNT',{fil},'G','Protein',{data.loc[fil]['Proteina']}),"
    rows.append(text)
    text = f"('{data.loc[fil]['Nombre']}_FAT',{fil},'G','Grasa',{data.loc[fil]['Grasa']}),"
    rows.append(text)
    text = f"('{data.loc[fil]['Nombre']}_FIBTG',{fil},'G','Fibra',{data.loc[fil]['Fibra']}),"
    rows.append(text)
    text = f"('{data.loc[fil]['Nombre']}_CHOCDF',{fil},'G','Carbohidratos',{data.loc[fil]['Carbohidrato']}),"
    rows.append(text)
for r in rows:
    print(r)


print("Insert Food")
rows = []
for fil in range(0,data.shape[0]):
    text = f"('{fil}','{data.loc[fil]['Nombre']}','{data.loc[fil]['Nombre']}'),"
    rows.append(text)

for r in rows:
    print(r)

