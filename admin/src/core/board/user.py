from src.core.database import db

class User(db.Model):
    _tablename_="users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, nullable=False)

    def _repr_(self):
        return f'<User #{self.id} email="{self.email}" alias="{self.alias}" activo={self.activo}'