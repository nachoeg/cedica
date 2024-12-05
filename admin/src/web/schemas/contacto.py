import re
from marshmallow import Schema, fields, post_dump, validates, ValidationError


class ConsultaSchema(Schema):
    """Esquema para crear nuevas consultas a partir de api/message"""

    titulo = fields.Str(
        required=True,
        validate=lambda x: 1 <= len(x) <= 100,
        error_messages={
            "required": "El título es obligatorio.",
            "validator_failed": "El titulo debe contener entre 1 y 100 caracteres.",
        },
    )
    email = fields.Email(
        required=True,
        validate=lambda x: 1 <= len(x) <= 100,
        error_messages={
            "required": "El correo electrónico es obligatorio.",
            "invalid": "Debe proporcionar un correo electrónico válido.",
            "validator_failed": "El correo debe tener entre 1 y 100 caracteres.",
        },
    )
    mensaje = fields.Str(
        required=True,
        validate=lambda x: 1 <= len(x) <= 500,
        error_messages={
            "required": "El mensaje es obligatorio.",
            "validator_failed": "El mensaje debe contener entre 1 y 500 caracteres.",
        },
    )

    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    closed_at = fields.DateTime(dump_only=True, allow_none=True)

    @validates("titulo")
    def validate_titulo(self, value):
        """
        Verifica que el titulo no este vacio y no sea una cadena de espacios.
        """
        if not value.strip():
            raise ValidationError("El título no puede estar vacío.")

    @validates("mensaje")
    def validate_mensaje(self, value):
        """
        Verifica que el mensaje no este vacio y no sea una cadena de espacios.
        """
        if not value.strip():
            raise ValidationError("El mensaje no puede estar vacío.")

    @post_dump
    def format_response(self, data, **kwargs):
        return {
            "title": data.get("titulo"),
            "email": data.get("email"),
            "description": data.get("mensaje"),
            "status": data.get("status", "created"),
            "created_at": data.get("created_at"),
            "closed_at": data.get("closed_at"),
        }


consulta_schema = ConsultaSchema()
consultas_schema = ConsultaSchema(many=True)
create_consulta_schema = ConsultaSchema()
