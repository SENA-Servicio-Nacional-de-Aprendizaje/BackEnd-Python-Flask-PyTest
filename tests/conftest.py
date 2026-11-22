import os

import pytest

from src.app import create_app
from src.models import db

"""Pytest reconoce automáticamente un archivo especial llamado tests/conftest.py.

Cualquier fixture declarado allí queda disponible para todos los archivos de
prueba del proyecto sin necesidad de importarlo manualmente.
"""


@pytest.fixture
def app():
    # Crea y configura una nueva instancia de la app para cada funcion de test
    test_config = {
        # Activa el modo de pruebas
        "TESTING": True,
        # SQLite en memoria en tu PC; en GitHub usa DATABASE_URL (MySQL en integración)
        "SQLALCHEMY_DATABASE_URI": os.environ.get("DATABASE_URL", "sqlite:///:memory:"),
        # Desactiva el rastreador de modificaciones
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

    # Sobreescribe la configuración por defecto con una config de prueba
    app_instance = create_app(test_config=test_config)

    # Crea un contexto de aplicacion para cada funcion de test
    with app_instance.app_context():
        db.create_all()  # Crea todas las tablas necesarias en la base de datos
        yield app_instance  # Entrega la app a cada prueba
        db.session.remove()  # 1. Cierra y limpia la sesión activa de SQLAlchemy
        db.drop_all()  # 2. Elimina todas las tablas
        db.engine.dispose()  # 3. Cierra todas las conexiones del pool


@pytest.fixture
def client(app):
    """Crea un cliente de prueba aislado.

    Provee el cliente de prueba de Flask derivado de la app creada en el fixture anterior.
    """
    return app.test_client()  # El cliente de prueba aislado está listo para usar
