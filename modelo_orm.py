from peewee import *


sqlite_db = SqliteDatabase('./TP-POO-Navarro-Feige-GonzalezRoisler/obras_urbanas.db', pragmas={'journal_mode': 'wal'})

"""Conexion a base de datos"""
try:
    sqlite_db.connect()
except OperationalError as e:
    print("Se ha generado un error en la conexion con la base de datos.", e)
    exit()

"""Clase base para las entidades de la base de datos"""
class BaseModel(Model):
    class Meta:
        database = sqlite_db

"""Entidad Etapa"""
class Etapa(BaseModel):
    id_etapa = AutoField(primary_key=True)
    nombre_etapa = TextField(unique= True, null=False)

    def __str__(self) -> str:
        return self.nombre_etapa
    
    class Meta:
        db_table = "Etapas"

"""Entidad Tipo de obra"""
class Tipo(BaseModel):
    id_tipo = AutoField(primary_key=True)
    nombre_tipo = TextField(unique= True, null=False)

    def __str__(self) -> str:
        return self.nombre_tipo
    
    class Meta:
        db_table = "tipo_de_obra"

"""Entidad Responsable de Area"""
class AreaResponsable(BaseModel):
    id_responsable = AutoField(primary_key=True)
    nombre_responsable = TextField(unique= True, null=False)

    def __str__(self) -> str:
        return self.nombre_responsable
    
    class Meta:
        db_table = "responsable_de_area"

"""Entidad Fuente de Financiamiento"""
class FuenteFinanciamiento(BaseModel):
    id_financiamiento = AutoField(primary_key=True)
    nombre_financiamiento = TextField(unique= True, null=False)
    
    def __str__(self) -> str:
        return self.nombre_financiamiento
    
    class Meta:
        db_table = "fuentes_de_financiamiento"

"""Entidad Empresa"""
class Empresa(BaseModel):
    id_empresa = AutoField(primary_key=True)
    nombre_empresa = TextField(unique= True, null=False)
    
    def __str__(self) -> str:
        return self.nombre_empresa
      
    class Meta:
        db_table = "Empresas"

"""Entidad Barrios"""
class Barrios(BaseModel):
    id_barrio = AutoField(primary_key=True)
    nombre_barrio = TextField(unique= True, null=False)
    comuna_barrio = IntegerField(null = False)
   
    def __str__(self) -> str:
        return self.nombre_barrio
    
    class Meta:
        db_table = "Barrios"

"""Entidad Contratacion"""
class Contratacion(BaseModel):
    id_contratacion = AutoField (primary_key = True)
    contratacion = TextField(unique = True)

    def __str__(self) -> str:
        return self.contratacion
    
    class Meta:
        db_table = "Tipo de Contratacion"

"""Entidadd Obra"""
class Obra(BaseModel):
    id = AutoField(primary_key=True)
    nombre = TextField(null= False)
    etapa = ForeignKeyField(Etapa,backref="obras")
    tipo = ForeignKeyField(Tipo, backref="obras")
    area_responsable = ForeignKeyField(AreaResponsable,backref="obras")
    descripcion = TextField(null = False)
    barrio = ForeignKeyField(Barrios,backref="obras")
    monto_contratado = FloatField(null= True,default=0)
    direccion = TextField(null=True)
    latitud = FloatField(null= False)
    longitud = FloatField(null= False)
    fecha_inicio = DateField(null=True)
    fecha_fin_inicial = DateField(null=True)
    plazo_meses = IntegerField(null=True)
    porcentaje = IntegerField(null=True)
    licitacion_oferta_empresa = ForeignKeyField(Empresa, backref= 'obras') 
    licitacion_anio = IntegerField(null=True)
    contratacion_obra = ForeignKeyField(Contratacion, backref= 'obras')
    nro_contratacion = TextField(null=True)
    beneficiarios = TextField(null=True)
    mano_obra = IntegerField(null=True)
    destacada = BooleanField(default=False) 
    fuente_financiamiento = ForeignKeyField(FuenteFinanciamiento,backref="obras")
    porcentaje_avance = FloatField()
    
    class Meta:
        db_table = "obras"
    
    def __str__(self):
        return f"{self.nombre}: obra {self.etapa.nombre_etapa} en {self.barrio.nombre_barrio}"
   
    """Metodo Nuevo proyecto"""
    @classmethod
    def nuevo_proyecto(cls):        

    # Solicitar los datos del nuevo proyecto al usuario. Si bien da la opcion, se debe ingresar Proyecto para realizarlo en funcion del requerimiento del TP
        nombre = input("Nombre del proyecto: ")
        descripcion = input("Descripción del proyecto: ")
        
        # Verificar si la etapa "Proyecto" existe en la base de datos
        etapa_proyecto = Etapa.get_or_none(nombre_etapa="Proyecto")
        if etapa_proyecto is None:
            # Si la etapa "Proyecto" no existe, crearla y guardarla en la base de datos
            try:
                etapa_proyecto = Etapa.create(nombre_etapa="Proyecto")
                print("Se ha creado la etapa 'Proyecto'.")
            except Exception as e:
                print("Ocurrió un error al crear la etapa 'Proyecto':", e)
                return
        
        # Solicitar al usuario los valores de tipo de obra, área responsable y barrio
        tipo_obra = input("Tipo de obra: ")
        area_responsable = input("Área responsable: ")
        barrio = input("Barrio: ")
        
        
        # Verificar si los valores ingresados existen en la base de datos
        tipo_existente = Tipo.get_or_none(nombre_tipo=tipo_obra)
        area_responsable_existente = AreaResponsable.get_or_none(nombre_responsable=area_responsable)
        barrio_existente = Barrios.get_or_none(nombre_barrio=barrio)


        # Opcional: Si el tipo de obra no existe, dar la opción de crearlo
        if tipo_existente is None:
            crear_tipo = input("El tipo de obra ingresado no existe. ¿Desea crearlo? (s/n): ")
            if crear_tipo.lower() == "s":
                try:
                    tipo_existente = Tipo.create(nombre_tipo=tipo_obra)
                    print(f"Se ha creado el tipo de obra '{tipo_obra}'.")
                except Exception as e:
                    print("Ocurrió un error al crear el tipo de obra:", e)
                    return
            else:
                return        
        # Opcional: Si el área responsable no existe, dar la opción de crearlo
        if area_responsable_existente is None:
            crear_area_responsable = input("El área responsable ingresada no existe. ¿Desea crearla? (s/n): ")
            if crear_area_responsable.lower() == "s":
                try:
                    area_responsable_existente = AreaResponsable.create(nombre_responsable=area_responsable)
                    print(f"Se ha creado el área responsable '{area_responsable}'.")
                except Exception as e:
                    print("Ocurrió un error al crear el área responsable:", e)
                    return
            else:
                return
        
        # Opcional: Si el barrio no existe, dar la opción de crearlo
        if barrio_existente is None:
            crear_barrio = input("El barrio ingresado no existe. ¿Desea crearlo? (s/n): ")
            if crear_barrio.lower() == "s":
                try:
                    comuna_barrio = int(input("Número de comuna del barrio: "))
                    barrio_existente = Barrios.create(nombre_barrio=barrio, comuna_barrio=comuna_barrio)
                    print(f"Se ha creado el barrio '{barrio}'.")
                except Exception as e:
                    print("Ocurrio un error al crear un barrio:", e)
                    return
            else:
                return
        
        # Crear una nueva instancia del modelo Obra con los datos capturados
        obra = Obra(
            nombre=nombre,
            descripcion=descripcion,
            etapa=etapa_proyecto,
            contratacion_obra=tipo_existente,
            area_responsable=area_responsable_existente,
            barrio=barrio_existente,
            porcentaje_avance=0.0,
            plazo_meses=0,
            mano_obra=0

            
        )
        
        # Guardar el nuevo proyecto en la base de datos
        try:
            obra.save()
            print("El proyecto se ha guardado exitosamente.")
        except Exception as e:
            print("Ocurrió un error al guardar el proyecto:", e)

    """Metodo Iniciar contratacion"""
    def iniciar_contratacion():
        # Solicitar los datos de la contratación al usuario
        tipo_contratacion = input("Tipo de contratación: ")
        nro_contratacion = input("Número de contratación: ")
        
        # Verificar si el tipo de contratación existe en la base de datos
        
        tipo_contratacion_existente = Contratacion.get_or_none(nombre_tipo_contratacion=tipo_contratacion)
        if tipo_contratacion_existente is None:
            crear_tipo_contratacion = input("El tipo de contratación ingresado no existe en la base de datos. ¿Desea crearla? (s/n): ")
            if crear_tipo_contratacion.lower() == "s":
                try:
                    tipo_contratacion_existente = Contratacion.create(nombre_tipo_contratacion=tipo_contratacion)
                    print(f"Se ha creado el área responsable '{tipo_contratacion}'.")
                except Exception as e:
                    print("Ocurrió un error al crear el área responsable:", e)
                    return
            else:
                return
            
        
        # Obtener la obra más reciente de la base de datos
        obra = Obra.select().order_by(Obra.id.desc()).first()
        if obra is None:
            obra_existente = input("No se encontró ninguna obra en la base de datos. ¿Desea crearla? (s/n)")
            if obra_existente.lower()=="s":
                try:
                    Obra.nuevo_proyecto()
                    print("se ha creado una obra nueva. Vuelva a intentar la contratacion")
                except Exception as e:
                    print("Ocurrió un error al crear el área responsable:", e)
                    return
                else:
                    return
        
        # Asignar los datos de contratación a la obra
        obra.contratacion_obra= tipo_contratacion_existente
        obra.nro_contratacion = nro_contratacion
        
        # Guardar los cambios en la base de datos
        try:
            obra.save()
            print("Se ha iniciado la contratación de la obra exitosamente.")
        except Exception as e:
            print("Ocurrió un error al iniciar la contratación de la obra:", e)
    
    """Metodo adjudicar obra"""
    def adjudicar_obra():
        # Solicitar los datos de la adjudicación al usuario
        nombre_empresa = input("Nombre de la empresa adjudicada: ")
        nro_expediente = input("Número de expediente: ")
        
        # Verificar si la empresa adjudicada existe en la base de datos
        empresa_adjudicada = Empresa.get_or_none(nombre_empresa=nombre_empresa)
        if empresa_adjudicada is None:
            # Si la empresa no existe, dar la opción de crearla
            crear_empresa = input("La empresa adjudicada ingresada no existe. ¿Desea crearla? (s/n): ")
            if crear_empresa.lower() == "s":
                try:
                    empresa_adjudicada = Empresa.create(nombre_empresa=nombre_empresa)
                    print(f"Se ha creado la empresa '{nombre_empresa}'.")
                except Exception as e:
                    print("Ocurrió un error al crear la empresa:", e)
                    return
            else:
                return
        
        # Obtener la obra más reciente de la base de datos
        try:
            obra = Obra.select().order_by(Obra.id.desc()).first()
        except Exception as e:
            print("Ocurrió un error al obtener la obra:", e)
            return
        
        if obra is None:
            print("No se encontró ninguna obra en la base de datos.")
            return
        
        # Asignar los datos de adjudicación a la obra
        obra.empresa_adjudicada = empresa_adjudicada
        obra.nro_expediente = nro_expediente
        
        # Guardar los cambios en la base de datos
        try:
            obra.save()
            print("Se ha adjudicado la obra exitosamente.")
        except Exception as e:
            print("Ocurrió un error al adjudicar la obra:", e)

    """Metodo iniciar obra"""
    def iniciar_obra():
        # Solicitar los datos del inicio de la obra al usuario
        destacada = input("¿Es una obra destacada? (s/n): ")
        fecha_inicio = input("Fecha de inicio (AAAA-MM-DD): ")
        fecha_fin_inicial = input("Fecha de finalización inicial (AAAA-MM-DD): ")
        nombre_fuente_financiamiento = input("Nombre de la fuente de financiamiento: ")
        mano_obra = input("Cantidad de mano de obra: ")
        
        # Verificar si la fuente de financiamiento existe en la base de datos
        try:
            fuente_financiamiento = FuenteFinanciamiento.get(nombre_financiamiento=nombre_fuente_financiamiento)
        except FuenteFinanciamiento.DoesNotExist:
            # Opcional: Si la fuente de financiamiento no existe, dar la opción de crearla
            crear_fuente = input("La fuente de financiamiento ingresada no existe. ¿Desea crearla? (s/n): ")
            if crear_fuente.lower() == "s":
                try:
                    fuente_financiamiento = FuenteFinanciamiento.create(nombre_financiamiento=nombre_fuente_financiamiento)
                    print(f"Se ha creado la fuente de financiamiento '{nombre_fuente_financiamiento}'.")
                except Exception as e:
                    print("Ocurrió un error al crear la fuente de financiamiento:", e)
                    return
            else:
                return
        
        # Obtener la obra más reciente de la base de datos
        try:
            obra = Obra.select().order_by(Obra.id.desc()).first()
        except Exception as e:
            print("Ocurrió un error al obtener la obra:", e)
            return
        
        if obra is None:
            print("No se encontró ninguna obra en la base de datos.")
            return
        
        # Asignar los datos del inicio de la obra
        obra.destacada = destacada.lower() == "s"
        obra.fecha_inicio = fecha_inicio
        obra.fecha_fin_inicial = fecha_fin_inicial
        obra.fuente_financiamiento = fuente_financiamiento
        obra.mano_obra = mano_obra
        
        # Guardar los cambios en la base de datos
        try:
            obra.save()
            print("Se ha iniciado la obra exitosamente.")
        except Exception as e:
            print("Ocurrió un error al iniciar la obra:", e)

    """Metodo actualizar porcentaje de avance"""
    def actualizar_porcentaje_avance():
        # Obtener la obra más reciente de la base de datos
        obra = Obra.select().order_by(Obra.id.desc()).first()
        if obra is None:
            print("No se encontró ninguna obra en la base de datos.")
            return
        
        # Solicitar el nuevo porcentaje de avance al usuario
        nuevo_porcentaje = input("Ingrese el nuevo porcentaje de avance: ")
        
        # Actualizar el valor del atributo porcentaje_avance
        obra.porcentaje_avance = nuevo_porcentaje
        
        # Guardar los cambios en la base de datos
        try:
            obra.save()
            print("Se ha actualizado el porcentaje de avance exitosamente.")
        except Exception as e:
            print("Ocurrió un error al actualizar el porcentaje de avance:", e)

    """Metodo incrementar plazo"""
    def incrementar_plazo():
        # Obtener la obra más reciente de la base de datos
        obra = Obra.select().order_by(Obra.id.desc()).first()
        if obra is None:
            print("No se encontró ninguna obra en la base de datos.")
            return
        
        # Solicitar la cantidad de meses a incrementar al usuario
        incremento_meses = input("Ingrese la cantidad de meses a incrementar: ")
        
        # Validar que la cantidad ingresada sea un número entero positivo
        try:
            incremento_meses = int(incremento_meses)
            if incremento_meses <= 0:
                raise ValueError
        except ValueError:
            print("La cantidad ingresada debe ser un número entero positivo.")
            return
        
        # Incrementar el valor del atributo plazo_meses
        obra.plazo_meses += incremento_meses
        
        # Guardar los cambios en la base de datos
        try:
            obra.save()
            print("Se ha incrementado el plazo de la obra exitosamente.")
        except Exception as e:
            print("Ocurrió un error al incrementar el plazo de la obra:", e)

    """Metodo incrementar mano de obra"""
    def incrementar_mano_obra():
        # Obtener la obra más reciente de la base de datos
        obra = Obra.select().order_by(Obra.id.desc()).first()
        if obra is None:
            print("No se encontró ninguna obra en la base de datos.")
            return
        
        # Solicitar la cantidad de mano de obra a incrementar al usuario
        incremento_mano_obra = input("Ingrese la cantidad de mano de obra a incrementar: ")
        
        # Validar que la cantidad ingresada sea un número entero positivo
        try:
            incremento_mano_obra = int(incremento_mano_obra)
            if incremento_mano_obra <= 0:
                raise ValueError
        except ValueError:
            print("La cantidad ingresada debe ser un número entero positivo.")
            return
        
        # Incrementar el valor del atributo mano_obra
        obra.mano_obra += incremento_mano_obra
        
        # Guardar los cambios en la base de datos
        try:
            obra.save()
            print("Se ha incrementado la cantidad de mano de obra exitosamente.")
        except Exception as e:
            print("Ocurrió un error al incrementar la cantidad de mano de obra:", e)

    """Metodo finalizar obra"""
    def finalizar_obra():
        # Obtener la obra más reciente de la base de datos
        obra = Obra.select().order_by(Obra.id.desc()).first()
        if obra is None:
            print("No se encontró ninguna obra en la base de datos.")
            return
        
        # Actualizar el valor del atributo etapa a "Finalizada"
        obra.etapa = "Finalizada"
        
        # Actualizar el valor del atributo porcentaje_avance a 100
        obra.porcentaje_avance = 100
        
        # Guardar los cambios en la base de datos
        try:
            obra.save()
            print("La obra se ha finalizado exitosamente.")
        except Exception as e:
            print("Ocurrió un error al finalizar la obra:", e)

    """Metodo rescindir obra"""
    def rescindir_obra():
        # Obtener la obra más reciente de la base de datos
        obra = Obra.select().order_by(Obra.id.desc()).first()
        if obra is None:
            print("No se encontró ninguna obra en la base de datos.")
            return
        
        # Actualizar el valor del atributo etapa a "Rescindida"
        obra.etapa = "Rescindida"
        
        # Guardar los cambios en la base de datos
        try:
            obra.save()
            print("La obra se ha rescindido exitosamente.")
        except Exception as e:
            print("Ocurrió un error al rescindir la obra:", e)