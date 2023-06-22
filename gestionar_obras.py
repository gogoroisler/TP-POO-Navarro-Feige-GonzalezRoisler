import pandas as pd
from modelo_orm import BaseModel, Obra
from abc import ABC, abstractmethod

#Definicion de clase abstracta GestionarObra
class GestionarObra(ABC):
    @classmethod
    def conectar_db(cls):
        # Realizar la conexión a la base de datos
        BaseModel.database.connect()
        print("Conexión a la base de datos establecida.")

    @classmethod
    def mapear_orm(cls):
        # Crear la estructura de la base de datos (tablas y relaciones)
        BaseModel.create_tables([Obra])
        print("Estructura de la base de datos creada.")
   
    @classmethod
    def limpiar_datos(cls, df):
        # Eliminar filas con datos nulos o no accesibles del DataFrame
        df_clean = df.dropna()
        print("Datos limpios.")

        return df_clean
    
    @classmethod
    def cargar_datos(cls, df):
        # Persistir los datos en la base de datos
        for _, row in df.iterrows():
            # Obtener los valores de cada columna del DataFrame
            nombre = row['nombre']
            ubicacion = row['ubicacion']
            fecha_inicio = row['fecha_inicio']
            fecha_fin = row['fecha_fin']
            costo = row['costo']

            # Crear una nueva instancia de la clase Obra y guardarla en la base de datos
            Obra.create(nombre=nombre, ubicacion=ubicacion, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, costo=costo)

        print("Datos cargados en la base de datos.")

    @classmethod
    def extraer_datos(cls):
        #leer dataset usando pandas
        df = pd.read_csv("observatorio-de-obras-urbanas.csv")

        # Limpiar los datos del dataset
        df_clean = cls.limpiar_datos(df)

        # Cargar los datos en la base de datos
        cls.cargar_datos(df_clean)
    
        
