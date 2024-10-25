from flask import render_template
from dataclasses import dataclass


@dataclass
class Error:
    code: int
    name: str
    description: str


def error_not_found(e):
    """Retorna la vista de error 404 cuando no se
    encontró la página solicitada.

    Argumentos:
    e -- la excepción
    """
    error = Error(404, "Not found",
                  "The requested URL was not found on the server.")

    return render_template("pages/error.html", error=error), error.code


def no_autorizado(e):
    """Retorna la vista de error 401 cuando no se
    tiene autorización para acceder.

    Argumentos:
    e -- la excepción
    """
    error = Error(401, "No autorizado", "No tiene autorización para acceder")

    return render_template("pages/error.html", error=error), error.code


def prohibido(e):
    """Retorna la vista de error 403 cuando no se tiene permiso para acceder.

    Argumentos:
    e -- la excepción
    """
    error = Error(403, "Prohibido", "No tiene permiso para acceder")

    return render_template("pages/error.html", error=error), error.code
