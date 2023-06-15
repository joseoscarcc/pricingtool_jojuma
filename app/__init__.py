from flask import Flask

from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Flask extensions here
    db.init_app(app)
    

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.precios import bp as precios_bp
    app.register_blueprint(precios_bp, url_prefix='/precios')

    from app.graph import bp as graph_bp
    app.register_blueprint(graph_bp, url_prefix='/graph')

    from app.maps import bp as maps_bp
    app.register_blueprint(maps_bp, url_prefix='/maps')

    from app.configuracion import bp as configuracion_bp
    app.register_blueprint(configuracion_bp, url_prefix='/configuracion')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app