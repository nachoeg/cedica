from datetime import datetime
import enum
from sqlalchemy.types import Enum
from sqlalchemy import event
from flask import current_app
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona
from src.web.handlers.funciones_auxiliares import fechahora_a_fecha
from src.core.database import db


class TipoArchivo(enum.Enum):
    entrevista = "Entrevista"
    evaluacion = "Evaluacion"
    planificacion = "Planificacion"
    evolucion = "Evolución"
    cronica = "Cronica"
    documental = "Documental"

    @classmethod
    def listar(self):
        return self._member_map_.values()

    def __str__(self):
        return f"{self.value}"


class Archivo_JYA(db.Model):
    __tablename__ = "archivos_jya"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.now)
    url = db.Column(db.String(100), nullable=False)
    tipo_archivo = db.Column(Enum(TipoArchivo))
    jya_id = db.Column(db.Integer, db.ForeignKey("jinetesyamazonas.id"))
    jya = db.relationship("JineteOAmazona", back_populates="documentos")
    externo = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "fecha_subida": fechahora_a_fecha(self.fecha_subida),
            "tipo_archivo": self.tipo_archivo.value
            if self.tipo_archivo else None,
        }

    def __repr__(self):
        return f"<Archivo #{self.id} titulo: {self.titulo}\
          tipo de archivo: {self.tipo_archivo}"


@event.listens_for(Archivo_JYA, "before_delete")
def antes_de_eliminar(mapper, connection, target):
    """Eliminar archivo asociado en MinIO
    antes de eliminar el documento de la base de datos."""
    if not target.externo:
        client = current_app.storage.client
        client.remove_object("grupo17", target.url)


@event.listens_for(JineteOAmazona, "before_delete")
def antes_de_eliminar_jinete_y_amazona(mapper, connection, target):
    """Eliminar archivos asociados en MinIO
    antes de eliminar el jinete/amazona de la base de datos."""
    client = current_app.storage.client
    documentos = Archivo_JYA.query.filter_by(jya_id=target.id).all()
    for documento in documentos:
        if not documento.externo:
            client.remove_object("grupo17", documento.url)
