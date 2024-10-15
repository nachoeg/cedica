from src.core.database import db
from datetime import datetime
import enum
from sqlalchemy.types import Enum

class Diagnostico(db.Model):
    __tablename__ = "diagnosticos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))

    def __repr__(self):
        return f'Diagnostico: {self.value}'

class JineteOAmazona(db.Model):
    __tablename__ = "jinetesyamazonas"

    id = db.Column(db.Integer, primary_key=True)

    #información general de la persona
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(30))
    dni = db.Column(db.Integer)
    edad = db.Column(db.Integer)
    fecha_nacimiento = db.Column(db.DateTime)
    provincia_nacimiento = db.Column(db.String(50))
    localidad_nacimiento = db.Column(db.String(50))
    domicilio_actual = db.Column(db.String(50))
    telefono_actual = db.Column(db.Integer)
    contacto_emer_nombre = db.Column(db.String(100))
    contacto_emer_telefono = db.Column(db.Integer)
    becado = db.Column(db.Boolean)
    porcentaje_beca = db.Column(db.String(100))

    #información de salud

    class TipoDeDiscapacidad(enum.Enum):
        mental = "Mental"
        motora = "Motora"
        sensorial = "Sensorial"
        visceral = "Visceral"

        def __str__(self):
            return f'{self.value}'    

    certificado_discapacidad = db.Column(db.Boolean)
    diagnostico_id = db.Column(db.Integer, db.ForeignKey("diagnosticos.id"))
    diagnostico_otro = db.Column(db.String(30))
    tipo_discapacidad = db.Column(Enum(TipoDeDiscapacidad))



    #informacion economica
    class TipoDeAsignacionFamiliar(enum.Enum):
        auhijo = "Asignación Universal por hijo"
        auhdisc = "Asignación Universal por hijo con Discapacidad"
        aaescolar = "Asignación por ayuda escolar anual"

        def __str__(self):
            return f'{self.value}' 


    class TipoPension(enum.Enum):
        provincial = "Provincial"
        nacional = "Nacional"
        
        def __str__(self):
            return f'{self.value}'

    
    asignacion_familiar = db.Column(db.Boolean)
    tipo_asignacion_familiar = db.Column(Enum(TipoDeAsignacionFamiliar))
    beneficiario_pension = db.Column(db.Boolean)
    tipo_pension = db.Column(Enum(TipoPension))
    obra_social = db.Column(db.String(30))
    num_afiliado = db.Column(db.Integer)
    posee_curatela = db.Column(db.Boolean)
    observaciones_obra_social = db.Column(db.String(100))

    #informacion sobre escolaridad
    nombre_escuela = db.Column(db.String(40))
    direccion_escuela = db.Column(db.String(50))
    telefono_escuela = db.Column(db.Integer)
    grado_escuela = db.Column(db.Integer)
    observaciones_escuela = db.Column(db.String(100))

    #informacion sobre profesionales
    profesionales_a_cargo = db.Column(db.String(200))

    #trabajo en nuestra institucion
    class PropuestaTrabajo(enum.Enum):
        hipoterapia = "Hipoterapia"
        monta_terapeutica = "Monta terapéutica"
        deporte_ecuestre = "Deporte ecuestre adaptado"
        actividades_recreativas = "Actividades recreativas"
        equitacion = "Equitación"
        
        def __str__(self):
            return f'{self.value}'


    class Condicion(enum.Enum):
        regular = "Regular"
        de_baja = "De baja"

        def __str__(self):
            return f'{self.value}'

    class Sede(enum.Enum):
        CASJ = "CASJ"
        HLP = "HLP"
        otro = "Otro"

        def __str__(self):
            return f'{self.value}'

    propuesta_trabajo = db.Column(Enum(PropuestaTrabajo))
    condicion = db.Column(Enum(Condicion))
    sede = db.Column(Enum(Sede))
    #profesor -> relacion con la tabla de miembros del equipo
    #conductor_caballo -> relacion con la tabla de miembros del equipo 
    #caballo -> relacion con la tabla de caballos
    #auxiliar de pista -> relacion con la tabla de miembros de equipo

    #TODO armar tabla de familiares a cargo
    #familiares a cargo
    #acá voy a tener que tener una tabla de familiares? es muchos a muchos
    #TODO armar tabla de dias de asistencia
    #dias
    #acá voy a tener que tener una tabla de dias? es muchos a muchos
    
    def __repr__(self):
        return f'<Jinete-Amazona #{self.id} nombre:{self.nombre}, apellido: {self.apellido}>'