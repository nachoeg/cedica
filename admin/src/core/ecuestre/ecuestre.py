from src.core.database import db


class TipoDeJyA(db.Model):
    __tablename__ = "tipo_de_jya"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)


class Ecuestre(db.Model):
    __tablename__ = "ecuestre"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    raza = db.Column(db.String(100), nullable=False)
    pelaje = db.Column(db.String(100), nullable=False)
    es_compra = db.Column(db.Boolean, nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    sede = db.Column(db.String(100), nullable=False)

    # Relacion con tipo de j&a
    tipo_de_jya_id = db.Column(
        db.Integer, db.ForeignKey("tipo_de_jya.id"), nullable=False
    )
    tipo_de_jya = db.relationship("TipoDeJyA", backref="ecuestre")

    def __repr__(self):
        return f'<Ecuestre #{self.id} nombre="{self.nombre}" fecha_nacimiento="{self.fecha_nacimiento}" sexo="{self.sexo}" raza="{self.raza}" pelaje="{self.pelaje}" es_compra="{self.es_compra}" fecha_ingreso="{self.fecha_ingreso}" sede="{self.sede}" tipo_de_jya="{self.tipo_de_jya}"'
