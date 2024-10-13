from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from core.usuarios import usuario_por_email_y_contraseña

# definir nombre y sección de url para esta parte
bp = Blueprint("autenticacion", __name__, url_prefix="/")


@bp.route('/iniciar_sesion', methods=('GET', 'POST'))
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        usuario = usuario_por_email_y_contraseña(email, contraseña)

        if usuario is None:
            flash('Usuario y/o contraseña incorrectos', 'error')

        else:
            session.clear()
            session['user'] = usuario.email
            flash('Ha iniciado sesión', 'exito')
            return redirect(url_for('home'))

    return render_template('usuarios/iniciar_sesion.html')