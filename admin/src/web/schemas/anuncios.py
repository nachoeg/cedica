from marshmallow import fields
from marshmallow import Schema

class AnuncioSchema(Schema):
    title = fields.String(attribute="titulo")  
    summary = fields.String(attribute="copete")  
    content = fields.String(attribute="contenido") 
    published_at = fields.DateTime(attribute="fecha_publicacion")  
    updated_at = fields.DateTime(attribute="fecha_ultima_actualizacion") 
    author = fields.Function(lambda obj: obj.autor.alias if obj.autor else None) 
    status = fields.String(attribute="estado.value")

anuncio_schema = AnuncioSchema()
anuncios_schema = AnuncioSchema(many=True)