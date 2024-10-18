from src.core.database import db
from datetime import datetime
import enum
from sqlalchemy.types import Enum

class Archivo_JYA(db.Model):
    __tablename__ = "archivos_jya"

    class TipoArchivo(enum.Enum):
        entrevista = "Entrevista"
        evaluacion = "Evaluacion"
        planificacion = "Planificacion"
        evolucion = "Evolución"
        cronica = "Cronica"
        documental = "Documental"
        
        def __str__(self):
            return f'{self.value}'
        
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(50))
    fecha_subida = db.Column(db.DateTime)
    tipo_archivo = db.Column(Enum(TipoArchivo))
