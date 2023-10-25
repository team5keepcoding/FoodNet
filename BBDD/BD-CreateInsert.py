import psycopg2
import gcsfs

### Creación de tablas y inserción de datos en BBDD
### El bucket debe contener una carpeta Datasets con los archivos Products.csv y Restaurants.csv


####################### Datos conexión ###############################

user = 'postgres'
password = 'team5'
host = '34.78.34.185'
port = '5432'
database = 'sysapp'

bucket_name = 'firstdeploy1010'

### El bucket debe contener una carpeta Datasets con los archivos Products.csv y Restaurants.csv

######################## Conexion######################################

connection = psycopg2.connect(
    host = host,
    port = port,
    database = database,
    user = user,
    password = password
)
cursor = connection.cursor()


#####################Tablas Nutrientes########################

Table_creation_Nutrient = '''
    CREATE table IF NOT EXISTS nutrient (
	idnutrient  VARCHAR(20)   	PRIMARY KEY,
	name 		VARCHAR(50)  	Unique NOT NULL,
	description VARCHAR(255) 	NOT NULL
    );
'''

cursor.execute(Table_creation_Nutrient)
connection.commit()

insert_nutrient_stmt = ("""
                INSERT INTO nutrient(idnutrient,name,description)
                VALUES (%s, %s, %s);
                """)

cursor.executemany(
                        insert_nutrient_stmt,
                        [
                            ('Calorias'     ,'Calorias'         ,'Energy'),
                            ('Protein'      ,'Protein'          ,'Protein'),
                            ('Grasa'        ,'Grasa'            ,'Total lipid (fat)'), 
                            ('Fibra'        ,'Fibra'            ,'Fiber, total dietary'),
                            ('Carbohidratos','Carbohidratos'    ,'Protein')
                        ]
                    )
connection.commit()



#####################Tablas Measure########################

Table_creation_Measure = '''
    CREATE table IF NOT EXISTS measure (
        idmeasure 	VARCHAR(20)  	PRIMARY KEY,
        name 		VARCHAR(50) 	UNIQUE NOT NULL,
        description VARCHAR(255) 	UNIQUE NOT NULL
    );
'''

cursor.execute(Table_creation_Measure)
connection.commit()

insert_measure_stmt = ("""
                        INSERT INTO measure(idmeasure,name,description)
                        VALUES (%s, %s, %s);
                        """)

cursor.executemany(
                        insert_measure_stmt,
                        [
                            ('G','Grams','Gramos'),
                            ('MG','MiliGrams','Miligramos')
                        ]
                    )
connection.commit()


######################## foodclasification ###############################

Table_creation_foodclasification = '''
    CREATE table IF NOT EXISTS foodclassification(
        idfoodclassification 	VARCHAR(30)  	PRIMARY KEY,
        name         			VARCHAR(50) 	NOT NULL,
        description	 			VARCHAR(255) 	NOT null
    );
'''

cursor.execute(Table_creation_foodclasification)
connection.commit()

insert_foodclasification2_stmt = ("""
                INSERT INTO foodclassification(idfoodclassification,name,description)
                VALUES (%s, %s, %s);
                """)

cursor.executemany( insert_foodclasification2_stmt,
                        [
                            ('0','Baked Potato','Baked Potato'),
                            ('1','Crispy Chicken','Crispy Chicken'),
                            ('2','Donut','Donut'),
                            ('3','Fries','Fries'),
                            ('4','Hot Dog','Hot Dog'),
                            ('5','Sandwich','Sandwich'),
                            ('6','Tacos','Tacos'),
                            ('7','Taquitos','Taquitos'),
                            ('8','apple pie','apple pie'),
                            ('9','burger','burger'),
                            ('10','butter naan','butter naan'),
                            ('11','chai','chai'),
                            ('12','chapati','chapati'),
                            ('13','cheesecake','cheesecake'),
                            ('14','chicken curry','chicken curry'),
                            ('15','chole bhature','chole bhature'),
                            ('16','dal makhani','dal makhani'),
                            ('17','fried rice','fried rice'),
                            ('18','ice cream','ice cream'),
                            ('19','idli','idli'),
                            ('20','jalebi','jalebi'),
                            ('21','rolls','rolls'),
                            ('22','kadai paneer','kadai paneer'),
                            ('23','masala dosa','masala dosa'),
                            ('24','momos','momos'),
                            ('25','omelette','omelette'),
                            ('26','pakora','pakora'),
                            ('27','pav bhaji','pav bhaji'),
                            ('28','pizza','pizza'),
                            ('29','sushi','sushi')
                        ]
                    )
connection.commit()


######################## Food Nutrient ###############################

Table_creation_foodnutrient = '''
    CREATE table IF NOT EXISTS foodnutrient(
        idfoodnutrient			VARCHAR(30)  	PRIMARY KEY,
        idfoodclassification    VARCHAR(30)     References foodclassification(idfoodclassification),
        idmeasure         		VARCHAR(50) 	References measure(idmeasure),
        idnutrient	 			VARCHAR(255) 	References nutrient(idnutrient),
        Quantity				float
    );
'''

cursor.execute(Table_creation_foodnutrient)
connection.commit()

insert_foodnutrient_stmt = ("""
                INSERT INTO foodnutrient(idfoodnutrient,idfoodclassification,idmeasure,idnutrient,Quantity)
                VALUES (%s,%s,%s,%s,%s);
                """)


cursor.executemany(insert_foodnutrient_stmt,
                        [
                            ('Baked Potato_ENERC_KCAL',0,'G','Calorias',95.0),   
                            ('Baked Potato_PROCNT',0,'G','Protein',2.63),        
                            ('Baked Potato_FAT',0,'G','Grasa',0.13),
                            ('Baked Potato_FIBTG',0,'G','Fibra',2.3),
                            ('Baked Potato_CHOCDF',0,'G','Carbohidratos',21.4),  
                            ('Crispy Chicken_ENERC_KCAL',1,'G','Calorias',187.0),
                            ('Crispy Chicken_PROCNT',1,'G','Protein',33.4),      
                            ('Crispy Chicken_FAT',1,'G','Grasa',4.71),
                            ('Crispy Chicken_FIBTG',1,'G','Fibra',0.0),
                            ('Crispy Chicken_CHOCDF',1,'G','Carbohidratos',0.51),
                            ('Donut_ENERC_KCAL',2,'G','Calorias',421.0),
                            ('Donut_PROCNT',2,'G','Protein',6.14),
                            ('Donut_FAT',2,'G','Grasa',22.7),
                            ('Donut_FIBTG',2,'G','Fibra',2.1),
                            ('Donut_CHOCDF',2,'G','Carbohidratos',47.9),
                            ('Fries_ENERC_KCAL',3,'G','Calorias',180.05),
                            ('Fries_PROCNT',3,'G','Protein',2.97),
                            ('Fries_FAT',3,'G','Grasa',12.31),
                            ('Fries_FIBTG',3,'G','Fibra',1.83),
                            ('Fries_CHOCDF',3,'G','Carbohidratos',15.27),
                            ('Hot Dog_ENERC_KCAL',4,'G','Calorias',211.0),
                            ('Hot Dog_PROCNT',4,'G','Protein',19.3),
                            ('Hot Dog_FAT',4,'G','Grasa',14.04),
                            ('Hot Dog_FIBTG',4,'G','Fibra',0.0),
                            ('Hot Dog_CHOCDF',4,'G','Carbohidratos',1.75),
                            ('Sandwich_ENERC_KCAL',5,'G','Calorias',164.32),
                            ('Sandwich_PROCNT',5,'G','Protein',7.46),
                            ('Sandwich_FAT',5,'G','Grasa',8.1),
                            ('Sandwich_FIBTG',5,'G','Fibra',2.22),
                            ('Sandwich_CHOCDF',5,'G','Carbohidratos',15.95),
                            ('Tacos_ENERC_KCAL',6,'G','Calorias',158.52),
                            ('Tacos_PROCNT',6,'G','Protein',8.02),
                            ('Tacos_FAT',6,'G','Grasa',8.94),
                            ('Tacos_FIBTG',6,'G','Fibra',2.04),
                            ('Tacos_CHOCDF',6,'G','Carbohidratos',11.99),
                            ('Taquitos_ENERC_KCAL',7,'G','Calorias',176.85),
                            ('Taquitos_PROCNT',7,'G','Protein',10.0),
                            ('Taquitos_FAT',7,'G','Grasa',9.67),
                            ('Taquitos_FIBTG',7,'G','Fibra',1.88),
                            ('Taquitos_CHOCDF',7,'G','Carbohidratos',13.03),
                            ('apple pie_ENERC_KCAL',8,'G','Calorias',265.0),
                            ('apple pie_PROCNT',8,'G','Protein',2.4),
                            ('apple pie_FAT',8,'G','Grasa',12.5),
                            ('apple pie_FIBTG',8,'G','Fibra',0.0),
                            ('apple pie_CHOCDF',8,'G','Carbohidratos',37.1),
                            ('burger_ENERC_KCAL',9,'G','Calorias',182.66),
                            ('burger_PROCNT',9,'G','Protein',14.24),
                            ('burger_FAT',9,'G','Grasa',8.98),
                            ('burger_FIBTG',9,'G','Fibra',0.62),
                            ('burger_CHOCDF',9,'G','Carbohidratos',11.46),
                            ('butter naan_ENERC_KCAL',10,'G','Calorias',274.76),
                            ('butter naan_PROCNT',10,'G','Protein',6.92),
                            ('butter naan_FAT',10,'G','Grasa',8.89),
                            ('butter naan_FIBTG',10,'G','Fibra',1.81),
                            ('butter naan_CHOCDF',10,'G','Carbohidratos',41.42),
                            ('chai_ENERC_KCAL',11,'G','Calorias',41.6),
                            ('chai_PROCNT',11,'G','Protein',1.39),
                            ('chai_FAT',11,'G','Grasa',1.63),
                            ('chai_FIBTG',11,'G','Fibra',0.45),
                            ('chai_CHOCDF',11,'G','Carbohidratos',5.7),
                            ('chapati_ENERC_KCAL',12,'G','Calorias',297.0),
                            ('chapati_PROCNT',12,'G','Protein',11.2),
                            ('chapati_FAT',12,'G','Grasa',7.45),
                            ('chapati_FIBTG',12,'G','Fibra',4.9),
                            ('chapati_CHOCDF',12,'G','Carbohidratos',46.4),
                            ('cheesecake_ENERC_KCAL',13,'G','Calorias',321.0),
                            ('cheesecake_PROCNT',13,'G','Protein',5.5),
                            ('cheesecake_FAT',13,'G','Grasa',22.5),
                            ('cheesecake_FIBTG',13,'G','Fibra',0.4),
                            ('cheesecake_CHOCDF',13,'G','Carbohidratos',25.5),
                            ('chicken curry_ENERC_KCAL',14,'G','Calorias',141.11),
                            ('chicken curry_PROCNT',14,'G','Protein',9.43),
                            ('chicken curry_FAT',14,'G','Grasa',8.54),
                            ('chicken curry_FIBTG',14,'G','Fibra',1.18),
                            ('chicken curry_CHOCDF',14,'G','Carbohidratos',6.88),
                            ('chole bhature_ENERC_KCAL',15,'G','Calorias',187.93),
                            ('chole bhature_PROCNT',15,'G','Protein',6.0),
                            ('chole bhature_FAT',15,'G','Grasa',8.25),
                            ('chole bhature_FIBTG',15,'G','Fibra',3.69),
                            ('chole bhature_CHOCDF',15,'G','Carbohidratos',23.76),
                            ('dal makhani_ENERC_KCAL',16,'G','Calorias',139.88),
                            ('dal makhani_PROCNT',16,'G','Protein',5.56),
                            ('dal makhani_FAT',16,'G','Grasa',6.32),
                            ('dal makhani_FIBTG',16,'G','Fibra',3.91),
                            ('dal makhani_CHOCDF',16,'G','Carbohidratos',16.65),
                            ('fried rice_ENERC_KCAL',17,'G','Calorias',172.84),
                            ('fried rice_PROCNT',17,'G','Protein',5.58),
                            ('fried rice_FAT',17,'G','Grasa',5.67),
                            ('fried rice_FIBTG',17,'G','Fibra',1.24),
                            ('fried rice_CHOCDF',17,'G','Carbohidratos',24.54),
                            ('ice cream_ENERC_KCAL',18,'G','Calorias',205.03),
                            ('ice cream_PROCNT',18,'G','Protein',3.16),
                            ('ice cream_FAT',18,'G','Grasa',11.94),
                            ('ice cream_FIBTG',18,'G','Fibra',0.71),
                            ('ice cream_CHOCDF',18,'G','Carbohidratos',22.35),
                            ('idli_ENERC_KCAL',19,'G','Calorias',565.0),
                            ('idli_PROCNT',19,'G','Protein',6.36),
                            ('idli_FAT',19,'G','Grasa',0.62),
                            ('idli_FIBTG',19,'G','Fibra',5.0),
                            ('idli_CHOCDF',19,'G','Carbohidratos',26.31),
                            ('jalebi_ENERC_KCAL',20,'G','Calorias',234.56),
                            ('jalebi_PROCNT',20,'G','Protein',2.14),
                            ('jalebi_FAT',20,'G','Grasa',8.03),
                            ('jalebi_FIBTG',20,'G','Fibra',0.6),
                            ('jalebi_CHOCDF',20,'G','Carbohidratos',39.46),
                            ('rolls_ENERC_KCAL',21,'G','Calorias',252.0),
                            ('rolls_PROCNT',21,'G','Protein',6.71),
                            ('rolls_FAT',21,'G','Grasa',8.37),
                            ('rolls_FIBTG',21,'G','Fibra',2.26),
                            ('rolls_CHOCDF',21,'G','Carbohidratos',37.71),
                            ('kadai paneer_ENERC_KCAL',22,'G','Calorias',74.53),
                            ('kadai paneer_PROCNT',22,'G','Protein',3.7),
                            ('kadai paneer_FAT',22,'G','Grasa',4.14),
                            ('kadai paneer_FIBTG',22,'G','Fibra',1.57),
                            ('kadai paneer_CHOCDF',22,'G','Carbohidratos',6.57),
                            ('masala dosa_ENERC_KCAL',23,'G','Calorias',153.37),
                            ('masala dosa_PROCNT',23,'G','Protein',3.79),
                            ('masala dosa_FAT',23,'G','Grasa',4.9),
                            ('masala dosa_FIBTG',23,'G','Fibra',2.5),
                            ('masala dosa_CHOCDF',23,'G','Carbohidratos',23.45),
                            ('momos_ENERC_KCAL',24,'G','Calorias',178.58),
                            ('momos_PROCNT',24,'G','Protein',7.3),
                            ('momos_FAT',24,'G','Grasa',8.21),
                            ('momos_FIBTG',24,'G','Fibra',1.3),
                            ('momos_CHOCDF',24,'G','Carbohidratos',18.88),
                            ('omelette_ENERC_KCAL',25,'G','Calorias',161.09),
                            ('omelette_PROCNT',25,'G','Protein',8.97),
                            ('omelette_FAT',25,'G','Grasa',12.42),
                            ('omelette_FIBTG',25,'G','Fibra',0.62),
                            ('omelette_CHOCDF',25,'G','Carbohidratos',3.32),
                            ('pakora_ENERC_KCAL',26,'G','Calorias',175.38),
                            ('pakora_PROCNT',26,'G','Protein',4.68),
                            ('pakora_FAT',26,'G','Grasa',10.18),
                            ('pakora_FIBTG',26,'G','Fibra',3.33),
                            ('pakora_CHOCDF',26,'G','Carbohidratos',17.19),
                            ('pav bhaji_ENERC_KCAL',27,'G','Calorias',99.25),
                            ('pav bhaji_PROCNT',27,'G','Protein',2.69),
                            ('pav bhaji_FAT',27,'G','Grasa',3.6),
                            ('pav bhaji_FIBTG',27,'G','Fibra',2.27),
                            ('pav bhaji_CHOCDF',27,'G','Carbohidratos',14.96),
                            ('pizza_ENERC_KCAL',28,'G','Calorias',268.0),
                            ('pizza_PROCNT',28,'G','Protein',10.4),
                            ('pizza_FAT',28,'G','Grasa',12.3),
                            ('pizza_FIBTG',28,'G','Fibra',2.2),
                            ('pizza_CHOCDF',28,'G','Carbohidratos',29.0),
                            ('sushi_ENERC_KCAL',29,'G','Calorias',126.96),
                            ('sushi_PROCNT',29,'G','Protein',4.18),
                            ('sushi_FAT',29,'G','Grasa',2.75),
                            ('sushi_FIBTG',29,'G','Fibra',0.76),
                            ('sushi_CHOCDF',29,'G','Carbohidratos',20.9)
                        ]
                    )
connection.commit()


##################### Tabla prediction ########################

Table_creation_prediction = '''
    CREATE TABLE  IF NOT EXISTS prediccion(
    idprediccion                serial primary key ,
    nombre                      varchar(255),
    nombre_uuid                 varchar(255),
    url                         varchar(255),
    idfoodclassification        VARCHAR(30) references foodclassification(idfoodclassification)
)
'''

cursor.execute(Table_creation_prediction)
connection.commit()


#####################Tablas Platform########################

Table_creation_Platform = '''
    CREATE table IF NOT EXISTS platform (
	idplatform  VARCHAR(20)   	PRIMARY KEY,
	name 		VARCHAR(50)  	Unique NOT NULL,
	description VARCHAR(255) 	NOT NULL
    );
'''

cursor.execute(Table_creation_Platform)
connection.commit()

insert_platform_stmt = ("""
                INSERT INTO  platform(idPlatform,name,description)
                VALUES (%s, %s, %s);
                """)

cursor.executemany(
                        insert_platform_stmt,
                        [
                            ('Glovo'     ,'Glovo'     ,'Plataforma glovo'),
                            ('JustEat'   ,'JustEat'   ,'Plataforma Just Eat')
                        ]
                    )
connection.commit()

##################### Tabla Resaturantes ########################

Table_creation_restaurante = '''
    CREATE TABLE  IF NOT EXISTS restaurant(
    idrestaurant                varchar(255) primary key ,
    name                        varchar(255),
    url                         varchar(255),
    Rating                      VARCHAR(255), 
    address                     VARCHAR(255), 
    latitude                    float,
    longitude                   float,
    idplatform                  VARCHAR(20) references platform(idplatform)
    )
'''

cursor.execute(Table_creation_restaurante)
connection.commit()


fs = gcsfs.GCSFileSystem()
with fs.open(f'{bucket_name}/Datasets/Restaurants.csv') as f:
    # Notice that we don't need the csv module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'restaurant', sep=';')
    connection.commit()  
    f.close()

##################### Tabla Product ########################

Table_creation_product = '''
    CREATE TABLE  IF NOT EXISTS product(
    idproduct                   varchar(200) primary key,
    idrestaurant                varchar(255) references restaurant(idrestaurant),
    name                        varchar(2000),
    description                 varchar(2000),
    idfoodclassification 	    VARCHAR(30)  references foodclassification(idfoodclassification)
    )
'''

cursor.execute(Table_creation_product)
connection.commit()


fs = gcsfs.GCSFileSystem()
with fs.open(f'{bucket_name}/Datasets/Products.csv',mode='rb',encoding='utf8') as f:
    # Notice that we don't need the csv module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'product', sep=';')
    connection.commit()  
    f.close()

#####################Cierre conexion######################################

if connection:
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
