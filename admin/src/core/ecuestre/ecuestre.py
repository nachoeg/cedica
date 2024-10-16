from src.core.database import db


class TipoDeJyA(db.Model):
    __tablename__ = "tipo_de_jya"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.tipo


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

    # Relacion entrenadores (miembros del equipo).
    entrenadores = db.relationship(
        "Miembro",
        secondary="entrenadores_ecuestre",
        lazy=True,
        backref=db.backref("entrenadores_ecuestres", lazy=True),
    )

    # Relacion conductores (miembros del equipo).
    conductores = db.relationship(
        "Miembro",
        secondary="conductores_ecuestre",
        lazy=True,
        backref=db.backref("conductores_ecuestres", lazy=True),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_nacimiento": self.fecha_nacimiento,
            "sexo": self.sexo,
            "raza": self.raza,
            "pelaje": self.pelaje,
            "es_compra": self.es_compra,
            "fecha_ingreso": self.fecha_ingreso,
            "sede": self.sede,
            "tipo_de_jya": self.tipo_de_jya.tipo if self.tipo_de_jya else None,
            "entrenadores": " / ".join(
                [
                    entrenador.nombre + " " + entrenador.apellido
                    for entrenador in self.entrenadores
                ]
            ),
            "conductores": " / ".join(
                [
                    conductor.nombre + " " + conductor.apellido
                    for conductor in self.conductores
                ]
            ),
        }

    def __repr__(self):
        return f'<Ecuestre #{self.id} nombre="{self.nombre}" fecha_nacimiento="{self.fecha_nacimiento}" sexo="{self.sexo}" raza="{self.raza}" pelaje="{self.pelaje}" es_compra="{self.es_compra}" fecha_ingreso="{self.fecha_ingreso}" sede="{self.sede}" tipo_de_jya="{self.tipo_de_jya}">'


# tabla intermedia para la relación muchos a muchos entre ecuestres y entrenadores
entrenadores_ecuestre = db.Table(
    "entrenadores_ecuestre",
    db.Column(
        "ecuestre_id", db.Integer, db.ForeignKey("ecuestre.id"), primary_key=True
    ),
    db.Column("miembro_id", db.Integer, db.ForeignKey("miembro.id"), primary_key=True),
)

# tabla intermedia para la relación muchos a muchos entre ecuestres y conductores
conductores_ecuestre = db.Table(
    "conductores_ecuestre",
    db.Column(
        "ecuestre_id", db.Integer, db.ForeignKey("ecuestre.id"), primary_key=True
    ),
    db.Column("miembro_id", db.Integer, db.ForeignKey("miembro.id"), primary_key=True),
)
