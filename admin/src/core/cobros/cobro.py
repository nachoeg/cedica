from src.core.database import db
from datetime import datetime
import enum
from sqlalchemy.types import Enum

from src.web.handlers.funciones_auxiliares import fechahora_a_fecha


class MedioDePago(enum.Enum):
    """Clase de tipo enumerativo para gestionar
    las opciones de medios de pago de cobros
    """

    efectivo = "Efectivo"
    credito = "Tarjeta de crédito"
    debito = "Tarjeta de débito"
    otro = "Otro medio de pago"

    @classmethod
    def listar(self):
        return self._member_map_.values()

    def __str__(self):
        return f"{self.value}"


class Cobro(db.Model):
    """Modelo de cobros"""

    __tablename__ = "cobros"

    id = db.Column(db.Integer, primary_key=True)
    fecha_pago = db.Column(db.DateTime, default=datetime.now)
    medio_de_pago = db.Column(Enum(MedioDePago), nullable="False")
    monto = db.Column(db.Double, nullable=False)
    observaciones = db.Column(db.String(100))
    recibio_el_dinero_id = db.Column(
        db.Integer, db.ForeignKey("miembro.id"), nullable=False
    )
    recibio_el_dinero = db.relationship("Miembro")

    joa_id = db.Column(
        db.Integer,
        db.ForeignKey("jinetesyamazonas.id", ondelete="CASCADE"),
        nullable=False,
    )

    joa = db.relationship("JineteOAmazona")

    def to_dict(self):
        return {
            "id": self.id,
            "fecha_pago": fechahora_a_fecha(self.fecha_pago),
            "medio_de_pago": self.medio_de_pago,
            "monto": self.monto,
            "observaciones": self.observaciones,
            "joa": (
                self.joa.nombre + " " + self.joa.apellido
                if self.joa else None
            ),
            "recibio_el_dinero": (
                self.recibio_el_dinero.nombre + " "
                + self.recibio_el_dinero.apellido
                if self.recibio_el_dinero else None
            ),
        }

    def __repr__(self):
        return f'<Cobro #{self.id},\
        fecha de pago={self.fecha_pago},\
        medio de pago: {self.medio_de_pago},\
        observaciones: "{self.observaciones}">'
