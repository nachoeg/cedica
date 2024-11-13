from core.anuncios.anuncio import Anuncio
from src.core.database import db


def crear_anuncio(titulo, copete, contenido, autor_id, estado="borrador"):
    """Crea un objeto de tipo Anuncio con los datos que recibe por
    parámetro y lo devuelve.
    """
    anuncio = Anuncio(titulo=titulo, copete=copete, contenido=contenido,
                      autor_id=autor_id, estado=estado)
    db.session.add(anuncio)
    db.session.commit()

    return anuncio
