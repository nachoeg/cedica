from flask import Blueprint, render_template, request, redirect, url_for
from src.core.ecuestre import listar_ecuestres


bp = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")


@bp.get("/")
def index():
    ecuestres = listar_ecuestres()
    return render_template("ecuestre.html", ecuestres=ecuestres)
