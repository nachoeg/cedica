from datetime import datetime
import enum

from sqlalchemy import Enum
from src.core.database import db
from src.web.handlers.funciones_auxiliares import fechahora_a_fecha


class Anuncio(db.Model):
    """Clase que representa un anuncio del sistema."""
    __tablename__ = "anuncios"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False, unique=True)
    copete = db.Column(db.String(250), nullable=False)
    contenido = db.Column(db.String(350), nullable=False)

    fecha_publicacion = db.Column(db.DateTime)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    fecha_ultima_actualizacion = db.Column(db.DateTime, default=datetime.now,
                                           onupdate=datetime.now)

    class Estado(enum.Enum):
        borrador = "Borrador"
        publicado = "Publicado"
        archivado = "Archivado"

        def __str__(self):
            return f"{self.value}"

    estado = db.Column(Enum(Estado), default="borrador")

    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    autor = db.relationship('Usuario', back_populates='anuncios')

    def to_dict(self):
        """Método que devuelve un diccionario con los datos
        del anuncio: titulo, fecha_creacion, estado
        """
        return {
            "titulo": self.titulo,
            "creacion": fechahora_a_fecha(self.fecha_creacion),
            "estado": self.estado,
        }

    def __repr__(self):
        """Método que devuelve la representación de un anuncio."""
        return f'<Anuncio#{self.id} titulo={self.titulo}, \
            fecha de creacion={self.fecha_creacion} \
            fecha última actualización={self.fecha_ultima_actualizacion} \
            autor={self.autor.alias}>'
