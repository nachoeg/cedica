from datetime import datetime

from src.core.database import db
from src.web.handlers.funciones_auxiliares import (booleano_a_palabra,
                                                   fechahora_a_fecha)


class SolicitudUsuario(db.Model):
    """Clase que representa una solicitud para ser usuario del sistema."""
    __tablename__ = "solicitudes"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    aceptada = db.Column(db.Boolean, nullable=False, default=False)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        """Método que devuelve un diccionario con los datos
        de la solicitud: email, activo, fecha_creacion,
        admin_sistema y roles."

        """
        return {
            "email": self.email,
            "aceptada": booleano_a_palabra(self.aceptada),
            "fecha_solicitud": fechahora_a_fecha(self.fecha_solicitud),
        }

    def __repr__(self):
        """Método que devuelve la representación de una solicitud."""
        return f'<Solicitud de usuario #{self.id} email={self.email} \
                  aceptada={self.aceptada} \
                  fecha de solicitud={self.fecha_solicitud}>'
