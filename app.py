"""
Sistema de Tutoría Inteligente (STI)
Aplicación principal Flask
"""

from app import create_app, db, login_manager
from app.models import User, Student, Teacher, Course, Question, DiagnosticExam, LearningPath, Resource, Progress

# Crear la aplicación
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    """Cargar usuario para Flask-Login"""
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        print("[OK] Base de datos inicializada")
        print("[START] Sistema de Tutoría Inteligente iniciado")
        print("[WEB] Accede a: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
