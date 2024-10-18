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


class Familiar(db.Model):
    __tablename__="familiares"

    class NivelEscolaridad(enum.Enum):
        primario = "Primario"
        secundario = "Secundario"
        terciario = "Terciario"
        universitario = "Universitario"

        def __str__(self):
            return f'{self.value}'    

    id = db.Column(db.Integer, primary_key=True)

    jya_id = db.Column(db.Integer, db.ForeignKey('jinetesyamazonas.id'))
    jya = db.relationship('JineteOAmazona',cascade = "all,delete")

    parentesco = db.Column(db.String(40))
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(30))
    dni = db.Column(db.Integer)
    domicilio_actual = db.Column(db.String(60))
    celular_actual = db.Column(db.BigInteger)
    email = db.Column(db.String(20))
    nivel_escolaridad = db.Column(Enum(NivelEscolaridad))
    ocupacion = db.Column(db.String(40))

    def __repr__(self):
        return f'Familiar: {self.nombre}'
    
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
    telefono_actual = db.Column(db.BigInteger)
    contacto_emer_nombre = db.Column(db.String(100))
    contacto_emer_telefono = db.Column(db.BigInteger)
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
    diagnostico = db.relationship('Diagnostico')

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

    tiene_deuda = db.Column(db.Boolean)
    asignacion_familiar = db.Column(db.Boolean)
    tipo_asignacion_familiar = db.Column(Enum(TipoDeAsignacionFamiliar))
    beneficiario_pension = db.Column(db.Boolean)
    tipo_pension = db.Column(Enum(TipoPension))
    obra_social = db.Column(db.String(30))
    num_afiliado = db.Column(db.BigInteger)
    posee_curatela = db.Column(db.Boolean)
    observaciones_obra_social = db.Column(db.String(100))

    #informacion sobre escolaridad
    nombre_escuela = db.Column(db.String(40))
    direccion_escuela = db.Column(db.String(50))
    telefono_escuela = db.Column(db.BigInteger)
    grado_escuela = db.Column(db.String(4))
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

    profesor_id = db.Column(db.Integer, db.ForeignKey('miembro.id'))
    profesor = db.relationship('Miembro', foreign_keys=[profesor_id])

    conductor_caballo_id = db.Column(db.Integer, db.ForeignKey('miembro.id'))
    conductor_caballo = db.relationship('Miembro', foreign_keys=[conductor_caballo_id])

    caballo_id = db.Column(db.Integer, db.ForeignKey('ecuestre.id'))
    caballo = db.relationship('Ecuestre', foreign_keys=[caballo_id])

    auxiliar_pista_id = db.Column(db.Integer, db.ForeignKey('miembro.id'))
    auxiliar_pista = db.relationship('Miembro', foreign_keys=[auxiliar_pista_id])

    #TODO armar tabla de familiares a cargo
    #familiares a cargo
    #acá voy a tener que tener una tabla de familiares? es muchos a muchos
    #TODO armar tabla de dias de asistencia
    #dias
    #acá voy a tener que tener una tabla de dias? es muchos a muchos
    
    '''
        Método que devuelve los resultados paginados dada la pagina y la cantidad de elementos por página.
        El parámetro asc se utiliza para que, si se le pasa de manera explícita un 0 como parámetro, 
        se devuelvan los resultados de manera descendente
    '''
    @staticmethod
    def todos_paginados(asc=1, pagina=1, por_pagina=2):
        if asc == 0:
                return JineteOAmazona.query.order_by(JineteOAmazona.nombre.desc()).paginate(page=pagina, per_page=por_pagina)
        else:
            return JineteOAmazona.query.order_by(JineteOAmazona.nombre.asc()).paginate(page=pagina, per_page=por_pagina)


    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "tiene_deuda": self.tiene_deuda,
            "edad": self.edad,
            "fecha_nacimiento": self.fecha_nacimiento,
            "provincia_nacimiento": self.provincia_nacimiento,
            "localidad_nacimiento": self.localidad_nacimiento,
            "domicilio_actual": self.domicilio_actual,
            "telefono_actual": self.telefono_actual,
            "contacto_emer_nombre": self.contacto_emer_nombre,
            "contacto_emer_telefono": self.contacto_emer_telefono,
            "becado": self.becado,
            "porcentaje_beca": self.porcentaje_beca,
            "certificado_discapacidad": self.certificado_discapacidad,
            "diagnostico": self.diagnostico.nombre if self.diagnostico else None,
            "diagnostico_otro": self.diagnostico_otro,
            "tipo_discapacidad": self.tipo_discapacidad,
            "asignacion_familiar": self.asignacion_familiar,
            "tipo_asignacion_familiar": self.tipo_asignacion_familiar,
            "beneficiario_pension": self.beneficiario_pension,
            "tipo_pension": self.tipo_pension,
            "obra_social": self.obra_social,
            "num_afiliado": self.num_afiliado,
            "posee_curatela": self.posee_curatela,
            "observaciones_obra_social": self.observaciones_obra_social,
            "nombre_escuela": self.nombre_escuela,
            "direccion_escuela": self.direccion_escuela,
            "telefono_escuela": self.telefono_escuela,
            "grado_escuela": self.grado_escuela,
            "observaciones_escuela": self.observaciones_escuela,
            "propuesta_trabajo": self.propuesta_trabajo,
            "condicion": self.condicion,
            "sede": self.sede,
            "profesor": self.profesor.nombre if self.profesor else None,
            "conductor_caballo": self.conductor_caballo.nombre if self.conductor_caballo else None,
            "caballo": self.caballo.nombre if self.caballo else None,
            "auxiliar_pista": self.auxiliar_pista.nombre if self.auxiliar_pista else None, 
         }

    def __repr__(self):
        return f'<Jinete-Amazona #{self.id} nombre:{self.nombre}, apellido: {self.apellido}>'