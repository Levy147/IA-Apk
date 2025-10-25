"""
Sistema de Tutoría Inteligente (STI)
Paquete principal de la aplicación
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
import os
import logging

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name=None):
    """Factory function para crear la aplicación"""
    app = Flask(__name__)
    
    # Configuración
    config_name = config_name or os.environ.get('FLASK_CONFIG') or 'default'
    from config import config
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Configurar login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # Configurar logging
    if not app.debug and not app.testing:
        logging.basicConfig(level=logging.INFO)
        logging.info('STI startup')
    
    # Importar modelos después de inicializar la app
    with app.app_context():
        from app.models import User, Student, Teacher, Course, Question, DiagnosticExam, LearningPath, Resource, Progress
    
    # Registrar blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.student import bp as student_bp
    app.register_blueprint(student_bp, url_prefix='/student')
    
    from app.teacher import bp as teacher_bp
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Crear directorios necesarios
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AI_MODEL_PATH'], exist_ok=True)
    
    # Context processors
    @app.context_processor
    def inject_user():
        from flask_login import current_user
        return dict(current_user=current_user)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app
