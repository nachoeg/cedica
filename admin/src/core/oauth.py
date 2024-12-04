from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def init_app(app):
    """Inicializa la base de datos con la aplicación de Flask."""
    oauth.init_app(app)

    name = 'google'
    client_id = app.config.get("GOOGLE_CLIENT_ID")
    client_secret = app.config.get("GOOGLE_CLIENT_SECRET")
    authorize_params = {'prompt': 'consent'}  # pide autoriz. con cada ingreso
    client_kwargs = {'scope': 'openid profile email'}
    s_m_url = "https://accounts.google.com/.well-known/openid-configuration"

    oauth.register(name=name,
                   client_id=client_id,
                   client_secret=client_secret,
                   authorize_params=authorize_params,
                   client_kwargs=client_kwargs,
                   server_metadata_url=s_m_url,
                   )

    return app
