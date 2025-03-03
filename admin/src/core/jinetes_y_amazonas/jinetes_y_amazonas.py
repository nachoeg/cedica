import enum
from sqlalchemy.types import Enum
from src.core.database import db
from src.web.handlers.funciones_auxiliares import calcular_edad


class Diagnostico(db.Model):
    """
    Modelo correspondiente a los diagnósticos de salud de J&A.
    """

    __tablename__ = "diagnosticos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"Diagnostico: {self.value}"


class TipoDeDiscapacidad(db.Model):
    """
    Tabla de tipos de discapacidad
    """
    __tablename__ = "tiposdediscapacidad"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(10))


class Dia(db.Model):
    """
    Tabla de días de la semana
    """

    __tablename__ = "dias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(9))


class Familiar(db.Model):
    """
    Modelo correspondiente a los familiares de J&A.
    """

    __tablename__ = "familiares"

    class NivelEscolaridad(enum.Enum):
        primario = "Primario"
        secundario = "Secundario"
        terciario = "Terciario"
        universitario = "Universitario"

        def __str__(self):
            return f"{self.value}"

    id = db.Column(db.Integer, primary_key=True)

    jya_id = db.Column(db.Integer, db.ForeignKey("jinetesyamazonas.id"))
    jya = db.relationship("JineteOAmazona",
                          cascade="all,delete",
                          back_populates="familiares")

    parentesco = db.Column(db.String(40))
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(30))
    dni = db.Column(db.Integer)
    domicilio_actual = db.Column(db.String(60))
    telefono_actual = db.Column(db.String(15))
    email = db.Column(db.String(20))
    nivel_escolaridad = db.Column(Enum(NivelEscolaridad))
    ocupacion = db.Column(db.String(40))

    def __repr__(self):
        return f"Familiar: {self.nombre} J/A relacionado:\
            {self.jya.nombre} {self.jya.apellido}"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono_actual,
        }


class JineteOAmazona(db.Model):
    """
    Modelo correspondiente a los J&A.
    """

    __tablename__ = "jinetesyamazonas"

    id = db.Column(db.Integer, primary_key=True)

    # información general de la persona
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(30))
    dni = db.Column(db.Integer, unique=True)
    fecha_nacimiento = db.Column(db.DateTime)
    provincia_nacimiento = db.Column(db.String(50))
    localidad_nacimiento = db.Column(db.String(50))
    domicilio_actual = db.Column(db.String(50))
    telefono_actual = db.Column(db.String(15))
    contacto_emer_nombre = db.Column(db.String(100))
    contacto_emer_telefono = db.Column(db.String(15))
    becado = db.Column(db.Boolean)
    porcentaje_beca = db.Column(db.Integer)

    # información de salud
    certificado_discapacidad = db.Column(db.Boolean)
    diagnostico_id = db.Column(db.Integer, db.ForeignKey("diagnosticos.id"))
    diagnostico = db.relationship("Diagnostico")

    diagnostico_otro = db.Column(db.String(30))
    tipo_discapacidad = db.relationship(
                "TipoDeDiscapacidad",
                secondary="tipos_discapacidad_por_jinete",
                lazy=True,
                backref=db.backref("tipos_discapacidad_por_jinete", lazy=True))

    # informacion economica
    class TipoDeAsignacionFamiliar(enum.Enum):
        auhijo = "Asignación Universal por hijo"
        auhdisc = "Asignación Universal por hijo con Discapacidad"
        aaescolar = "Asignación por ayuda escolar anual"

        def __str__(self):
            return f"{self.value}"

    class TipoPension(enum.Enum):
        provincial = "Provincial"
        nacional = "Nacional"

        def __str__(self):
            return f"{self.value}"

    tiene_deuda = db.Column(db.Boolean)
    asignacion_familiar = db.Column(db.Boolean)
    tipo_asignacion_familiar = db.Column(Enum(TipoDeAsignacionFamiliar))
    beneficiario_pension = db.Column(db.Boolean)
    tipo_pension = db.Column(Enum(TipoPension))
    obra_social = db.Column(db.String(30))
    num_afiliado = db.Column(db.BigInteger)
    posee_curatela = db.Column(db.Boolean)
    observaciones_obra_social = db.Column(db.String(100))

    # informacion sobre escolaridad
    nombre_escuela = db.Column(db.String(40))
    direccion_escuela = db.Column(db.String(50))
    telefono_escuela = db.Column(db.String(15))
    grado_escuela = db.Column(db.String(4))
    observaciones_escuela = db.Column(db.String(100))

    # informacion sobre profesionales
    profesionales_a_cargo = db.Column(db.String(200))

    # trabajo en nuestra institucion
    class PropuestaTrabajo(enum.Enum):
        hipoterapia = "Hipoterapia"
        monta_terapeutica = "Monta terapéutica"
        deporte_ecuestre = "Deporte ecuestre adaptado"
        actividades_recreativas = "Actividades recreativas"
        equitacion = "Equitación"

        def __str__(self):
            return f"{self.value}"

    class Condicion(enum.Enum):
        regular = "Regular"
        de_baja = "De baja"

        def __str__(self):
            return f"{self.value}"

    class Sede(enum.Enum):
        CASJ = "CASJ"
        HLP = "HLP"
        otro = "Otro"

        def __str__(self):
            return f"{self.value}"

    propuesta_trabajo = db.Column(Enum(PropuestaTrabajo))
    condicion = db.Column(Enum(Condicion))
    sede = db.Column(Enum(Sede))

    profesor_id = db.Column(db.Integer, db.ForeignKey("miembro.id"))
    profesor = db.relationship("Miembro", foreign_keys=[profesor_id])

    conductor_caballo_id = db.Column(db.Integer, db.ForeignKey("miembro.id"))
    conductor_caballo = db.relationship("Miembro",
                                        foreign_keys=[conductor_caballo_id])

    caballo_id = db.Column(db.Integer, db.ForeignKey("ecuestres.id"))
    caballo = db.relationship("Ecuestre",
                              foreign_keys=[caballo_id])

    auxiliar_pista_id = db.Column(db.Integer, db.ForeignKey("miembro.id"))
    auxiliar_pista = db.relationship("Miembro",
                                     foreign_keys=[auxiliar_pista_id])

    # Relacion con los días
    dias_asignados = db.relationship(
        "Dia",
        secondary="dias_por_jinete",
        lazy=True,
        backref=db.backref("dias_por_jinetes", lazy=True)
    )

    documentos = db.relationship("Archivo_JYA", back_populates="jya")
    familiares = db.relationship("Familiar", back_populates="jya")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "tiene_deuda": ("TIENE DEUDA" if self.tiene_deuda else "-"),
            "edad": calcular_edad(self.fecha_nacimiento),
            "profesionales_a_cargo": (
                self.profesionales_a_cargo
                if self.profesionales_a_cargo else "-"),
        }

    def __repr__(self):
        return f"<Jinete-Amazona #{self.id}\
          nombre:{self.nombre}, apellido: {self.apellido}>"

    # Tabla intermedia para almacenar los días que asiste
    # cada jinete a la institución
    dias = db.Table(
        "dias_por_jinete",
        db.Column(
            "jinete_id", db.Integer, db.ForeignKey("jinetesyamazonas.id"),
            primary_key=True
        ),
        db.Column("dia_id", db.Integer, db.ForeignKey("dias.id"),
                  primary_key=True),
    )

    # Tabla intermedia para almacenar los tipos de discapacidad
    # por cada jinete (relacion muchos a muchos)
    tipos_disc = db.Table(
        "tipos_discapacidad_por_jinete",
        db.Column("jinete_id", db.Integer,
                  db.ForeignKey("jinetesyamazonas.id"),
                  primary_key=True),
        db.Column("tipo_discapacidad", db.Integer,
                  db.ForeignKey("tiposdediscapacidad.id"), primary_key=True)
    )
