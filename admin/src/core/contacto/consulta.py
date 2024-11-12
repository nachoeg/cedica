from datetime import datetime
from src.core.database import db
import enum


class Consulta(db.Model):
    """Modelo de consulta"""

    __tablename__ = "consultas"

    class Estado(enum.Enum):
        """Clase de tipo enumerativo para gestionar las opciones de estado de las consultas"""

        pendiente = "Pendiente"
        en_proceso = "En proceso"
        finalizada = "Finalizada"

        @classmethod
        def listar(self):
            return self._member_map_.values()

        def __str__(self):
            return f"{self.value}"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now, nullable=False)
    estado = db.Column(db.Enum(Estado), default=Estado.pendiente, nullable=False)
    comentario = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Consulta {self.id} - {self.nombre}>"
