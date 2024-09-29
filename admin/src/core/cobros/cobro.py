from src.core.database import db
from datetime import datetime
import enum
from sqlalchemy.types import Enum

class Cobro(db.Model):
    __tablename__ = "cobros"

    class MedioDePago(enum.Enum):
        efectivo = "Efectivo"
        credito = "Tarjeta de crédito"
        debito = "Tarjeta de débito"
        otro = "Otro medio de pago"


    id = db.Column(db.Integer, primary_key=True)
    fecha_pago = db.Column(db.DateTime, default=datetime.now)
    medio_de_pago = db.Column(Enum(MedioDePago))
    monto = db.Column(db.Double, nullable=False)
    observaciones = db.Column(db.String(100))
    #recibio_el_dinero(referencia a tabla de miembros)
    #joa(referencia a tabla de jya)


    def __repr__(self):
        return f'<Cobro #{self.id} fecha de pago={self.fecha_pago}, medio de pago: {self.medio_de_pago}, observaciones: "{self.observaciones}">'