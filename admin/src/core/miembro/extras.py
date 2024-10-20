from src.core.database import db


class Profesion(db.Model):
    __tablename__ = "profesion"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True) 
    
    
class PuestoLaboral(db.Model):
    __tablename__ = "puesto_laboral"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True) 

    
class CondicionDeTrabajo(db.Model):
    __tablename__ = "condicion_trabajo"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

class TipoDeDocumentoMiembro(db.Model):
    __tablename__ = "tipos_de_documento_miembro"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String, nullable=False)
    
class DocumentoMiembro(db.Model):
    __tablename__ = "documentos_miembro"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    url = db.Column(db.String(100), nullable=False)

    tipo_de_documento_id = db.Column(
        db.Integer, db.ForeignKey("tipos_de_documento_miembro.id"), nullable=False
    )
    tipo_de_documento = db.relationship("TipoDeDocumentoMiembro", backref="documentos_miembro")

    miembro_id = db.Column(db.Integer, db.ForeignKey("miembro.id"), nullable=False)
    miembro = db.relationship("Miembro", backref="documentos_miembro")

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "fecha": self.fecha,
            "tipo": self.tipo_de_documento.tipo if self.tipo_de_documento else None,
        }

    def __repr__(self):
        return f'<Documento #{self.id} nombre="{self.nombre}" fecha="{self.fecha}" tipo="{self.tipo}" url="{self.url}"">'
