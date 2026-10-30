import logging

from flask import Flask

from .config import KONFIGURACJE
from .converters import RegionConverter
import time
from flask import g


def create_app(nazwa_konfiguracji="rozwojowa"):
    app = Flask(__name__)
    @app.before_request
    def before_request():
        g.start = time.perf_counter()

    @app.after_request
    def after_request(response):
        if hasattr(g, 'start'):
            czas = (time.perf_counter() - g.start) * 1000
            response.headers['X-Czas-Ms'] = f"{czas:.2f}"
        return response


    app.config.from_object(KONFIGURACJE[nazwa_konfiguracji])
    app.logger.setLevel(logging.INFO)

    from .routes_api import api_bp
    from .routes_panel import panel_bp
    app.url_map.converters["region"] = RegionConverter

    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
        # Rejestracja tego samego interfejsu pod drugim przedrostkiem (API v2)
    app.register_blueprint(api_bp, url_prefix="/api/v2", name="api_v2")
    
    # Rejestracja ujednoliconej obsługi błędów
    from .errors import zarejestruj_obsluge_bledow
    zarejestruj_obsluge_bledow(app)

    return app

