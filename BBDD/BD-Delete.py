import psycopg2


####Borrar tabla BBDD


###################### Datos conexión ###############################

# #Check CredentialsBBDD.txt para credenciales

# user = <user>
# password = <password>
# host = <host>
# port = <port>
# database = <database>


######################## Conexion######################################

connection = psycopg2.connect(
    host = host,
    port = port,
    database = database,
    user = user,
    password = password
)
cursor = connection.cursor()


# cursor.execute("DROP SCHEMA IF EXISTS public CASCADE;")
# connection.commit()

cursor.execute("CREATE SCHEMA IF NOT EXISTS public;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS nutrient CASCADE;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS measure CASCADE;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS foodclassification CASCADE;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS foodnutrient CASCADE;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS prediccion CASCADE;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS platform CASCADE;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS restaurant CASCADE;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS product CASCADE;")
connection.commit()

if connection:
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")