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
    fecha_subida = db.Column(db.DateTime,default=datetime.now)
    tipo_archivo = db.Column(Enum(TipoArchivo))
    jya_id = db.Column(db.Integer, db.ForeignKey('jinetesyamazonas.id'))
    jya = db.relationship('JineteOAmazona')
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "fecha_subida": self.fecha_subida,
            "tipo_archivo": self.diagnostico.nombre if self.diagnostico else None,
        }

    def __repr__(self):
        return f'<Archivo #{self.id} titulo: {self.titulo} tipo de archivo_ {self.tipo_archivo}'

