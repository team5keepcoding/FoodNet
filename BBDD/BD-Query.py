import psycopg2

#Consultas de pruebas BBDD

user = 'postgres'
password = 'team5'
host = '34.78.34.185'
port = '5432'
database = 'sysapp'


######################## Conexion######################################

connection = psycopg2.connect(
    host = host,
    port = port,
    database = database,
    user = user,
    password = password
)
cursor = connection.cursor()


################################## INSERT INTO Prueba ####################################

# insert_prediction_stmt = ("""
#                 INSERT INTO prediction(nombre,nombre_uuid,url,idfoodclassification)
#                 VALUES (%s, %s,%s, %s);
#                 """)

# cursor.execute(insert_prediction_stmt,("photo1.jpg","photo1","http:ala",2))
# connection.commit()
# cursor.execute(insert_prediction_stmt,("photo2.jpg","photo2",'https:aaaaaaaa',10))
# connection.commit()

######################### SELECT ##################################

postgreSQL_select_Query = """SELECT pre.idfoodclassification , fc.name
                            FROM prediccion as pre  
	                        left join foodclassification as fc on pre.idfoodclassification = fc.idfoodclassification; 
                           """

cursor.execute(postgreSQL_select_Query)

records = cursor.fetchall()

print("---------------------------------------")
for row in records:
    print(row)


######################### SELECT ##################################

postgreSQL_select_Query = """SELECT *
                             FROM foodclassification as fc  
                             left join foodnutrient as fn on fc.idfoodclassification = fn.idfoodclassification; 
                           """

cursor.execute(postgreSQL_select_Query)
print("Selecting rows ")
records = cursor.fetchall()

print("-----------------Comidas con sus nutrientes----------------------")
for row in records:
    print(row)


######################### SELECT ##################################

# postgreSQL_select_Query = """SELECT *
#                              FROM prediccion as pre
#                              left join foodclassification  as fc on pre.idfoodclassification = fc.idfoodclassification
#                              left join product             as c  on pre.idfoodclassification = c.idfoodclassification 
#                              left join restaurant          as r  on c.idrestaurant           = r.idrestaurant;
#                            """

# cursor.execute(postgreSQL_select_Query)
# print("Selecting rows ")
# records = cursor.fetchall()

# print("---------------------------------------")
# for row in records:
#     print(row)


########################## SELECT ####################################

######################### SELECT ##################################

postgreSQL_select_Query = """SELECT r.name , r.url, c.name
                             FROM foodclassification as fc
                             left join product             as c  on fc.idfoodclassification = c.idfoodclassification 
                             left join restaurant          as r  on c.idrestaurant           = r.idrestaurant
                             where fc.idfoodclassification=2::text
                           """

cursor.execute(postgreSQL_select_Query)
print("Selecting rows ")
records = cursor.fetchall()

print("---------------------------------------")
for row in records:
    print(row)



#####################Cierre conexion######################################
if connection:
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
