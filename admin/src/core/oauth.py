from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def init_app(app):
    """Inicializa la base de datos con la aplicación de Flask."""
    oauth.init_app(app)

    name = 'google'
    client_id = app.config.get("GOOGLE_CLIENT_ID")
    client_secret = app.config.get("GOOGLE_CLIENT_SECRET")
    access_token_url = "https://accounts.google.com/o/oauth2/token"
    access_token_params = None
    authorize_url = "https://accounts.google.com/o/oauth2/auth"
    authorize_params = None
    api_base_url = "https://www.googleapis.com/oauth2/v1/"
    userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"
    client_kwargs = {'scope': 'openid profile email'}
    server_metadata_url = "htpps://accounts.google.com/.well-known/openid-configuration"

    oauth.register(name=name,
                   client_id=client_id,
                   client_secret=client_secret,
                   access_token_url=access_token_url,
                   access_token_params=access_token_params,
                   authorize_url=authorize_url,
                   authorize_params=authorize_params,
                   api_base_url=api_base_url,
                   userinfo_endpoint=userinfo_endpoint,
                   client_kwargs=client_kwargs,
                   server_metadata_url=server_metadata_url,
                   )

    return app


# from authlib.integrations.flask_client import OAuth


# class Google:
#     def __init__(self, app=None):
#         self._oauth = None
#         if app is not None:
#             self.init_app(app)

#     def init_app(self, app):
#         """Inicializa el cliente de MinIO y lo adjunta
#         al contexto de la app.
#         """
#         name = 'google'
#         client_id = app.config.get("GOOGLE_CLIENT_ID")
#         client_secret = app.config.get("GOOGLE_CLIENT_SECRET")
#         access_token_url = "https://accounts.google.com/o/oauth2/token"
#         access_token_params = None
#         authorize_url = "https://accounts.google.com/o/oauth2/auth"
#         authorize_params = None
#         api_base_url = "https://accounts.googleapis.com/o/oauth2/v1"
#         client_kwargs = {'scope': 'openid profile email'}

#         # inicializa el cliente de oauth
#         self._oauth = OAuth()

#         # adjunta el cliente al contexto de la app
#         # también podría cargarse el cliente
#         app.oauth = self

#         return app

#     def register(self, name, client_id, client_secret, access_token_url,
#                  access_token_params, authorize_url, authorize_params,
#                  api_base_url, client_kwargs):
#         self._oauth.register(name=name,
#                              client_id=client_id,
#                              client_secret=client_secret,
#                              access_token_url=access_token_url,
#                              access_token_params=access_token_params,
#                              authorize_url=authorize_url,
#                              authorize_params=authorize_params,
#                              api_base_url=api_base_url,
#                              client_kwargs=client_kwargs)

#     @property
#     def client(self):
#         """Propiedad para obtener el cliente de MinIO."""
#         return self._client

#     @client.setter
#     def client(self, valor):
#         """Propiedad setter para permitir reasignar el cliente de MinIO."""
#         self._client = valor


# oauth = OAuth()
