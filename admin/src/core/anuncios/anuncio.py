import enum
from sqlalchemy import Enum
from datetime import datetime
from src.core.database import db
from src.web.handlers.funciones_auxiliares import fechahora


class Estado(enum.Enum):
    bo = "Borrador"
    pu = "Publicado"
    ar = "Archivado"

    def __str__(self):
        return f"{self.value}"

    @classmethod
    def listar(self):
        return self._member_map_.values()


class Anuncio(db.Model):
    """Clase que representa un anuncio del sistema."""
    __tablename__ = "anuncios"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False, unique=True)
    copete = db.Column(db.String(500), nullable=False)
    contenido = db.Column(db.String(3000), nullable=False)

    fecha_publicacion = db.Column(db.DateTime)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    fecha_ultima_actualizacion = db.Column(db.DateTime, default=datetime.now,
                                           onupdate=datetime.now)

    estado = db.Column(Enum(Estado), default="borrador")

    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    autor = db.relationship('Usuario', back_populates='anuncios')

    def to_dict(self):
        """Método que devuelve un diccionario con los datos
        del anuncio: titulo, fecha_creacion, estado
        """
        return {
            "titulo": self.titulo,
            "copete": self.copete,
            "autor": self.autor.alias,
            "creacion": fechahora(self.fecha_creacion),
            "publicacion": fechahora(self.fecha_publicacion)
            if self.fecha_publicacion is not None else "-",
            "ultima_actualizacion": fechahora(self.fecha_ultima_actualizacion),
            "estado": self.estado,
        }

    def __repr__(self):
        """Método que devuelve la representación de un anuncio."""
        return f'<Anuncio#{self.id} titulo={self.titulo}, \
            fecha de creacion={self.fecha_creacion} \
            fecha última actualización={self.fecha_ultima_actualizacion} \
            autor={self.autor.alias}>'
