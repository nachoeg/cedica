from src.core.database import db
from sqlalchemy import event
from flask import current_app
from src.web.handlers.funciones_auxiliares import fechahora_a_fecha


class TipoDeJyA(db.Model):
    """
    Modelo correspondiente a los tipos de jinetes y amazonas.
    """

    __tablename__ = "tipos_de_jya"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.tipo


class TipoDeDocumento(db.Model):
    """
    Modelo correspondiente a los tipos de documentos de ecuestres.
    """

    __tablename__ = "tipos_de_documento_ecuestre"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.tipo


class Documento(db.Model):
    """
    Modelo correspondiente a los documentos de ecuestres.
    """

    __tablename__ = "documentos_ecuestre"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    archivo_externo = db.Column(db.Boolean, nullable=False)

    # Relacion con tipo de documento
    tipo_de_documento_id = db.Column(
        db.Integer, db.ForeignKey("tipos_de_documento_ecuestre.id"), nullable=False
    )
    tipo_de_documento = db.relationship("TipoDeDocumento", backref="documentos")

    # Relacion con ecuestre
    ecuestre_id = db.Column(
        db.Integer, db.ForeignKey("ecuestres.id", ondelete="CASCADE"), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha": self.fecha,
            "tipo": self.tipo_de_documento.tipo if self.tipo_de_documento else None,
        }

    def __repr__(self):
        return f'<Documento #{self.id} nombre="{self.nombre}" fecha="{self.fecha}" tipo="{self.tipo}" url="{self.url}" ecuestre="{self.ecuestre}">'


class Ecuestre(db.Model):
    """
    Modelo correspondiente a los ecuestres.
    """

    __tablename__ = "ecuestres"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    raza = db.Column(db.String(100), nullable=False)
    pelaje = db.Column(db.String(100), nullable=False)
    es_compra = db.Column(db.Boolean, nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    sede = db.Column(db.String(100), nullable=False)

    # Relacion con tipo de j&a
    tipo_de_jya_id = db.Column(
        db.Integer, db.ForeignKey("tipos_de_jya.id"), nullable=False
    )
    tipo_de_jya = db.relationship("TipoDeJyA", backref="ecuestre")

    # Relacion entrenadores (miembros del equipo).
    entrenadores = db.relationship(
        "Miembro",
        secondary="entrenadores_ecuestre",
        lazy=True,
        backref=db.backref("entrenadores_ecuestres", lazy=True),
    )

    # Relacion conductores (miembros del equipo).
    conductores = db.relationship(
        "Miembro",
        secondary="conductores_ecuestre",
        lazy=True,
        backref=db.backref("conductores_ecuestres", lazy=True),
    )

    # Relacion con documentos
    documentos = db.relationship(
        "Documento",
        backref="ecuestre",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_nacimiento": fechahora_a_fecha(self.fecha_nacimiento),
            "sexo": self.sexo,
            "raza": self.raza,
            "pelaje": self.pelaje,
            "es_compra": "Compra" if self.es_compra else "Donación",
            "fecha_ingreso": fechahora_a_fecha(self.fecha_ingreso),
            "sede": self.sede,
            "tipo_de_jya": self.tipo_de_jya.tipo if self.tipo_de_jya else None,
            "entrenadores": " / ".join(
                [
                    entrenador.nombre + " " + entrenador.apellido
                    for entrenador in self.entrenadores
                ]
            ),
            "conductores": " / ".join(
                [
                    conductor.nombre + " " + conductor.apellido
                    for conductor in self.conductores
                ]
            ),
        }

    def __repr__(self):
        return f'<Ecuestre #{self.id} nombre="{self.nombre}" fecha_nacimiento="{self.fecha_nacimiento}" sexo="{self.sexo}" raza="{self.raza}" pelaje="{self.pelaje}" es_compra="{self.es_compra}" fecha_ingreso="{self.fecha_ingreso}" sede="{self.sede}" tipo_de_jya="{self.tipo_de_jya}">'


# tabla intermedia para la relación muchos a muchos entre ecuestres y entrenadores
entrenadores_ecuestre = db.Table(
    "entrenadores_ecuestre",
    db.Column(
        "ecuestre_id", db.Integer, db.ForeignKey("ecuestres.id"), primary_key=True
    ),
    db.Column("miembro_id", db.Integer, db.ForeignKey("miembro.id"), primary_key=True),
)

# tabla intermedia para la relación muchos a muchos entre ecuestres y conductores
conductores_ecuestre = db.Table(
    "conductores_ecuestre",
    db.Column(
        "ecuestre_id", db.Integer, db.ForeignKey("ecuestres.id"), primary_key=True
    ),
    db.Column("miembro_id", db.Integer, db.ForeignKey("miembro.id"), primary_key=True),
)


@event.listens_for(Documento, "before_delete")
def before_delete(mapper, connection, target):
    """
    Elimina el archivo asociado en MinIO antes de eliminar el documento de la base de datos.
    """
    if not target.archivo_externo:
        client = current_app.storage.client
        client.remove_object("grupo17", target.url)


@event.listens_for(Ecuestre, "before_delete")
def before_delete_ecuestre(mapper, connection, target):
    """
    Elimina los archivos asociados en MinIO antes de eliminar el ecuestre de la base de datos.
    """
    client = current_app.storage.client
    documentos = Documento.query.filter_by(ecuestre_id=target.id).all()
    for documento in documentos:
        if not documento.archivo_externo:
            client.remove_object("grupo17", documento.url)
