import math
from flask import Blueprint, flash, redirect, render_template, request, url_for
from core.usuarios import crear_usuario, listar_usuarios, usuario_por_id
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
        flash(f'Registro exitoso. \
              Alias: {usuario.alias}, email: {usuario.alias}')
        return redirect(url_for('usuarios.registrar_usuario'))
    return render_template('pages/usuarios/registrar_usuario.html', form=form)


@bp.route('/', methods=['GET'])
def listado_usuarios():
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 10))
    email_filtro = request.args.get("email", "")

    cant_resultados, usuarios = listar_usuarios(
        email_filtro, orden, ordenar_por, pagina, cant_por_pagina
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
        email_filtro=email_filtro,
    )


@bp.route('/<int:id>', methods=['GET'])
def ver_usuario(id):
    usuario = usuario_por_id(id)
    return render_template("pages/usuarios/ver_usuario.html", usuario=usuario)


@bp.route('/<int:id>', methods=['GET'])
def editar_usuario(id):
    pass


@bp.route('/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    pass
