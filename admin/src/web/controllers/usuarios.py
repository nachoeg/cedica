import math
from flask import Blueprint, flash, redirect, render_template, request, url_for
from core.usuarios import crear_usuario, listar_usuarios
from core.usuarios.usuario_forms import UsuarioForm

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@bp.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    form = UsuarioForm(request.form)
    if form.validate_on_submit():
        # raise Exception(f'{form.roles.data}')
        usuario = crear_usuario(form.email.data, form.contraseña.data, 
                                form.alias.data, form.admin_sistema.data, 
                                form.roles.data)
        flash(f'Se ha registrado correctamente al \
              usuario {usuario.alias}')
        return redirect(url_for('usuarios.registrar_usuario'))
    return render_template('pages/usuarios/registrar_usuario.html', form=form)


@bp.get("/")
def index():
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 10))
    nombre_filtro = request.args.get("nombre", "")

    cant_resultados, usuarios = listar_usuarios(
        nombre_filtro, orden, ordenar_por, pagina, cant_por_pagina
        )

    cant_paginas = math.ceil(cant_resultados / cant_por_pagina)

    return render_template(
        "pages/usuarios/listado_usuarios.html",
        usuarios=usuarios,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        nombre_filtro=nombre_filtro,
    )
