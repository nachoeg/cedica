from flask import render_template
from dataclasses import dataclass


@dataclass
class Error:
    code: int
    name: str
    description: str


def error_not_found(e):
    """Retorna el template de error cuando no se encontró la página solicitada.

    Argumentos:
    e -- la excepción
    """
    error = Error(404, "Not found", "The requested URL was not found on the server.")

    return render_template("pages/error.html", error=error), error.code
