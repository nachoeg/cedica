from src.core.database import db

class Domicilio(db.Model):
    __tablename__ = "domicilio"
    id = db.Column(db.Integer, primary_key=True)
    calle = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    piso = db.Column(db.String(10), nullable=True)
    dpto = db.Column(db.String(10), nullable=True)
    localidad = db.Column(db.String(100), nullable=False)
    miembros = db.relationship('Miembro', backref='domicilio', lazy=True)

class Profesion(db.Model):
    __tablename__ = "profesion"
    id = db.Column(db.Integer, primary_key=True)
    profesion = db.Column(db.String(100), nullable=False, unique=True) 
    
class PuestoLaboral(db.Model):
    __tablename__ = "puesto_laboral"
    id = db.Column(db.Integer, primary_key=True)
    puesto = db.Column(db.String(100), nullable=False, unique=True) 

    
class CondicionDeTrabajo(db.Model):
    __tablename__ = "condicion_trabajo"
    id = db.Column(db.Integer, primary_key=True)
    condicion = db.Column(db.String(100), nullable=False, unique=True)

class Miembro(db.Model):
    __tablename__ = "miembro"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(10), nullable=False)
    
    # relacion con domicilio
    domicilio_id = db.Column(db.Integer, db.ForeignKey('domicilio.id'), nullable=False)
    
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(25), nullable=False)
    
    # relacion con profesion
    profesion_id = db.Column(db.Integer, db.ForeignKey('profesion.id'), nullable=False)
    profesion = db.relationship('Profesion', backref='miembros')   

    # relacion con puesto laboral
    puesto_laboral_id = db.Column(db.Integer, db.ForeignKey('puesto_laboral.id'), nullable=False)
    puesto_laboral = db.relationship('PuestoLaboral', backref='miembros')    

    nombreContactoEmergencia = db.Column(db.String(100), nullable=False)
    telefonoContactoEmergencia = db.Column(db.String(25), nullable=False)
    obraSocial = db.Column(db.String(100), nullable=False)
    numeroAfiliado = db.Column(db.String(100), nullable=False)

    # relacion con condicion
    condicion_id = db.Column(db.Integer, db.ForeignKey('condicion.id'), nullable=False)
    condicion = db.relationship('Condicion', backref='miembros')
    
    activo = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Miembro #{self.id} email="{self.email}" alias="{self.alias}" activo={self.activo}'
