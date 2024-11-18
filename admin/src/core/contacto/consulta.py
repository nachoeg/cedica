from datetime import datetime
from src.core.database import db
import enum

class Estado(enum.Enum):
        """Clase de tipo enumerativo para gestionar las opciones de estado de las consultas"""

        recibida = "Recibida"
        leida = "Leida"
        atendida = "Atendida"

        @classmethod
        def listar(self):
            return self._member_map_.values()

        def __str__(self):
            return f"{self.value}"



class HistorialEstado(db.Model):
    __tablename__ = "historial_estado"

    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.Enum(Estado), default=Estado.recibida, nullable=False)
    comentario = db.Column(db.Text, nullable=True)
    usuario = db.Column(db.String(100), nullable=False)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consulta.id'), nullable=False)
    consulta = db.relationship('Consulta', backref=db.backref('historiales', lazy=True))


class Consulta(db.Model):
    """Modelo de consulta"""

    __tablename__ = "consulta"

    

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now, nullable=False)
    archivado = db.Column(db.Boolean, nullable=False, default=False)
    estado = db.Column(db.Enum(Estado), default=Estado.recibida, nullable=False)
    comentario = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Consulta {self.id} - {self.nombre}>"

    def to_dict(self):
        return {
            'titulo': self.nombre,
            'email': self.email,
            'mensaje': self.mensaje,
            'fecha': self.fecha.strftime('%d-%m-%Y'),
            'estado': self.estado
        }