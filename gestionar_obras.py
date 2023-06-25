import pandas as pd
from modelo_orm import *
from abc import ABC, abstractmethod
import csv

obra_csv = './TP-POO-Navarro-Feige-GonzalezRoisler/observatorio-de-obras-urbanas.csv'

"""Definicion de clase abstracta GestionarObra"""
class GestionarObra(ABC):
    
    """Metodo de clase conectar base de datos"""
    @classmethod
    def conectar_db(cls):
        # Realizar la conexión a la base de datos
        BaseModel.database.connect()
        print("Conexión a la base de datos establecida.")

    """Metodo de clase mapear orm"""
    @classmethod
    def mapear_orm(cls):
        # Crear la estructura de la base de datos (tablas y relaciones)
        BaseModel.create_tables([Obra])
        print("Estructura de la base de datos creada.")
   
    """Metodo de clase limpiar datos"""
    @classmethod
    def limpiar_datos(cls, df):
        # Eliminar filas con datos nulos o no accesibles del DataFrame
        df_clean = df.dropna()
        print("Datos limpios.")

        return df_clean
    
    """Metodo de clase cargar datos"""
    @classmethod
    def cargar_datos(cls, df):
        for _, row in df.iterrows():
            nombre = row['nombre']
            ubicacion = row['ubicacion']
            fecha_inicio = row['fecha_inicio']
            fecha_fin = row['fecha_fin']
            costo = row['costo']
            Obra.create(nombre=nombre, ubicacion=ubicacion, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, costo=costo)
        print("Datos cargados en la base de datos.")

    """Metodo de clase extraer datos"""
    @classmethod
    def extraer_datos(cls):
        #leer dataset usando pandas
        df = pd.read_csv("observatorio-de-obras-urbanas.csv")

        # Limpiar los datos del dataset
        df_clean = cls.limpiar_datos(df)

        # Cargar los datos en la base de datos
        cls.cargar_datos(df_clean)
    
    """Metodo de clase nueva obra"""
    @classmethod
    def nueva_obra(cls):
        try:
            # Obtener los valores requeridos del usuario por teclado
            nombre = input("Ingrese el nombre de la obra: ")
            descripcion = input("Ingrese la descripción de la obra: ")
            direccion = input("Ingrese la dirección de la obra: ")
            latitud = float(input("Ingrese la latitud de la obra: "))
            longitud = float(input("Ingrese la longitud de la obra: "))

            etapa = input("Ingrese la etapa de la obra: ")
            try:
                # Buscar la instancia de Etapa correspondiente al valor ingresado
                etapa_obra = Etapa.get(Etapa.nombre_etapa == etapa)
            except Etapa.DoesNotExist:
                print("La etapa ingresada no existe en la base de datos.")
                return None

            tipo = input("Ingrese el tipo de obra: ")
            try:
                # Buscar la instancia de Tipo correspondiente al valor ingresado
                tipo_obra = Tipo.get(Tipo.nombre_tipo == tipo)
            except Tipo.DoesNotExist:
                print("El tipo de obra ingresado no existe en la base de datos.")
                return None

            area_responsable = input("Ingrese el área responsable de la obra: ")
            try:
                # Buscar la instancia de AreaResponsable correspondiente al valor ingresado
                area_obra = AreaResponsable.get(AreaResponsable.nombre_responsable == area_responsable)
            except AreaResponsable.DoesNotExist:
                print("El área responsable ingresada no existe en la base de datos.")
                return None

            barrio = input("Ingrese el barrio de la obra: ")
            try:
                # Buscar la instancia de Barrios correspondiente al valor ingresado
                barrio_obra = Barrios.get(Barrios.nombre_barrio == barrio)
            except Barrios.DoesNotExist:
                print("El barrio ingresado no existe en la base de datos.")
                return None

            # Crear la nueva instancia de Obra
            nueva_obra = Obra(nombre=nombre, descripcion=descripcion, direccion=direccion, latitud=latitud,
                            longitud=longitud, etapa=etapa_obra, tipo=tipo_obra, area_responsable=area_obra,
                            barrio=barrio_obra)

            # Guardar la nueva instancia en la base de datos
            nueva_obra.save()

            # Retornar la nueva instancia de Obra
            return nueva_obra

        except OperationalError as e:
            print("Se ha generado un error en la conexión con la base de datos.", e)
            return None

    """Metodo de clase obtener indicadores"""
    @classmethod
    def obtener_indicadores(cls):
        try:
            opcion = input("Ingrese la opción deseada (a-g): ")

            if opcion == 'a':
                # Listado de todas las áreas responsables
                areas_responsables = [area.nombre_responsable for area in AreaResponsable.select()]
                print("Listado de todas las áreas responsables:")
                for area in areas_responsables:
                    print(area)

            elif opcion == 'b':
                # Listado de todos los tipos de obra
                tipos_obra = [tipo.nombre_tipo for tipo in Tipo.select()]
                print("Listado de todos los tipos de obra:")
                for tipo in tipos_obra:
                    print(tipo)

            elif opcion == 'c':
                # Cantidad de obras que se encuentran en cada etapa
                etapas_obras = Etapa.select()
                print("Cantidad de obras por etapa:")
                for etapa in etapas_obras:
                    cantidad_obras_etapa = Obra.select().where(Obra.etapa == etapa).count()
                    print(etapa.nombre_etapa, ":", cantidad_obras_etapa)

            elif opcion == 'd':
                # Cantidad de obras por tipo de obra
                tipos_obras = Tipo.select()
                print("Cantidad de obras por tipo de obra:")
                for tipo in tipos_obras:
                    cantidad_obras_tipo = Obra.select().where(Obra.tipo == tipo).count()
                    print(tipo.nombre_tipo, ":", cantidad_obras_tipo)

            elif opcion == 'e':
                # Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3
                comunas = [1, 2, 3]
                print("Listado de barrios en las comunas 1, 2 y 3:")
                for comuna in comunas:
                    barrios_comuna = Barrios.select().where(Barrios.comuna == comuna)
                    for barrio in barrios_comuna:
                        print(barrio.nombre_barrio)

            elif opcion == 'f':
                # Cantidad de obras "Finalizadas" en la comuna 1
                comuna = 1
                obras_finalizadas_comuna = Obra.select().where(Obra.etapa == Etapa.get(Etapa.nombre_etapa == "Finalizada"),
                                                            Obra.barrio.comuna == comuna).count()
                print("Cantidad de obras 'Finalizadas' en la comuna 1:", obras_finalizadas_comuna)

            elif opcion == 'g':
                # Cantidad de obras "Finalizadas" en un plazo menor o igual a 24 meses
                plazo_limite = 24
                obras_finalizadas_plazo = Obra.select().where(Obra.etapa == Etapa.get(Etapa.nombre_etapa == "Finalizada"),
                                                            Obra.plazo_meses <= plazo_limite).count()
                print("Cantidad de obras 'Finalizadas' en un plazo menor o igual a 24 meses:", obras_finalizadas_plazo)

            else:
                print("Opción inválida. Intente nuevamente.")

        except Exception as e:
            print("Ocurrió un error al obtener los indicadores:", e)


if __name__=='__main__':
    gestordeobra= GestionarObra()
    gestordeobra.cargar_datos()
    obra1 = gestordeobra.nueva_obra()
    obra1.iniciar_contratacion()
    obra1.adjudicar_obra()
    obra1.iniciar_obra()
    obra1.actualizar_porcentaje_avance()
    obra1.incrementar_plazo()
    obra1.finalizar_obra()