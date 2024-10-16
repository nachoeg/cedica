from src.core.database import db


class Miembro(db.Model):
    __tablename__ = "miembro"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(10), nullable=False)
    nombreContactoEmergencia = db.Column(db.String(100), nullable=False)
    telefonoContactoEmergencia = db.Column(db.String(25), nullable=False)
    obraSocial = db.Column(db.String(100), nullable=False)
    numeroAfiliado = db.Column(db.String(100), nullable=False)

    # relacion con condicion
    condicion_id = db.Column(db.Integer, db.ForeignKey('condicion_trabajo.id'), nullable=False)
    condicion_trabajo = db.relationship('CondicionDeTrabajo', backref='miembros')
    
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

    # relacion con usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    usuario = db.relationship('Usuario', backref='miembro', uselist=False)

    activo = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Miembro #{self.id} email="{self.email}" alias="{self.alias}" activo={self.activo}'
