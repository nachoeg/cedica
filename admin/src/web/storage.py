from minio import Minio


class Storage:
    def __init__(self, app=None):
        self._client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Inicializa el cliente de MinIO y lo adjunta
        al contexto de la app.
        """
        minio_server = app.config.get("MINIO_SERVER")
        access_key = app.config.get("MINIO_ACCESS_KEY")
        secret_key = app.config.get("MINIO_SECRET_KEY")
        secure = app.config.get("MINIO_SECURE", False)

        # inicializa el cliente de MinIO
        self._client = Minio(minio_server=minio_server, access_key=access_key,
                             secret_key=secret_key, secure=secure)

        # adjunta el cliente al contexto de la app
        # también podría cargarse el cliente
        app.storage = self

        return app

    @property
    def client(self):
        """Propiedad para obtener el cliente de MinIO."""
        return self._client

    @client.setter
    def client(self, valor):
        """Propiedad setter para permitir reasignar el cliente de MinIO."""
        self._client = valor


storage = Storage()
