from marshmallow import Schema, fields, post_dump


class ConsultaSchema(Schema):
    """Esquema para crear nuevas consultas a partir de api/message"""
    titulo = fields.Str(required=True, validate=lambda x: 1 <= len(x) <= 100)
    email = fields.Email(required=True, validate=lambda x: 1 <= len(x) <= 100)
    mensaje = fields.Str(required=True, validate=lambda x: 1 <= len(x) <= 500)


    status = fields.Str(dump_only=True)  
    created_at = fields.DateTime(dump_only=True) 
    closed_at = fields.DateTime(dump_only=True, allow_none=True) 

    @post_dump
    def format_response(self, data, **kwargs):
        return {
            "title": data.get("titulo"),
            "email": data.get("email"),
            "description": data.get("mensaje"),
            "status": data.get("status", "created"),
            "created_at": data.get("created_at"),
            "closed_at": data.get("closed_at")
        }
    
consulta_schema = ConsultaSchema()
consultas_schema = ConsultaSchema(many=True)
create_consulta_schema = ConsultaSchema()