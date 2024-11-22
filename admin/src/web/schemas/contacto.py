from marshmallow import Schema
from marshmallow import fields


class ConsultaSchema(Schema):
    titulo = fields.Str(required=True, validate=lambda x: 1 <= len(x) <= 100)
    email = fields.Email(required=True, validate=lambda x: 1 <= len(x) <= 100)
    mensaje = fields.Str(required=True, validate=lambda x: 1 <= len(x) <= 500)

consulta_schema = ConsultaSchema()
consultas_schema = ConsultaSchema(many=True)
create_consulta_schema = ConsultaSchema()