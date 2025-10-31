"""
Configuración del Sistema de Tutoría Inteligente (STI)
Configuración para desarrollo con XAMPP/MySQL
"""

import os
from datetime import timedelta

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sti-secret-key-2025'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Configuración de sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Configuración de archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    
    # Configuración de Google Forms
    GOOGLE_FORMS_API_KEY = os.environ.get('GOOGLE_FORMS_API_KEY')
    GOOGLE_FORMS_FORM_ID = os.environ.get('GOOGLE_FORMS_FORM_ID')
    
    # Configuración específica del formulario VARK
    VARK_FORM_ID = '1FAIpQLSf9eQT1ZEn_NncQiLdsvej-HZVQuFzjAYkqQU1UV4ORl-Lg9A'
    VARK_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSf9eQT1ZEn_NncQiLdsvej-HZVQuFzjAYkqQU1UV4ORl-Lg9A/viewform'
    
    # Configuración de IA
    AI_MODEL_PATH = 'models/'
    MIN_QUESTIONS_DIAGNOSTIC = 25

    # Formularios de diagnóstico por curso (Google Forms publicados)
    DIAGNOSTIC_FORMS = {
        # Química General
        'quimica': 'https://docs.google.com/forms/d/e/1FAIpQLSduYLWmW6mpTcUqWZSLXMsUPIFJVftN_30KFaqyDhY8buZdcg/viewform',
        # Técnica Complementaria
        'tecnica_complementaria': 'https://docs.google.com/forms/d/e/1FAIpQLSePC8e8B1h0mGQ1BdchXyHlkRVLBHmnzqzmby7evoeLzh-HQg/viewform',
        # Social Humanística 1
        'humanistica': 'https://docs.google.com/forms/d/e/1FAIpQLSf2so9khw6pyEwPhg8E4itLZF1YBPl7lQMF45f3BuTiDm9WKQ/viewform',
        # Matemática Básica 1
        'matematica': 'https://docs.google.com/forms/d/e/1FAIpQLSf9eQT1ZEn_NncQiLdsvej-HZVQuFzjAYkqQU1UV4ORl-Lg9A/viewform'
    }
    
    # Configuración de estilos de aprendizaje VARK
    VARK_QUESTIONS = 16  # Número de preguntas del cuestionario VARK
    
    # Configuración de rutas de aprendizaje
    MAX_LEARNING_PATH_LENGTH = 50
    MIN_MASTERY_THRESHOLD = 0.7  # 70% para considerar dominio

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    # Configuración XAMPP MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:@localhost:3306/sti_database'
    
    # Configuración de logging
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:@localhost:3306/sti_database_prod'
    
    # Configuración de logging
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
