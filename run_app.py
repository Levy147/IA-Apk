#!/usr/bin/env python3
"""
Script simplificado para ejecutar el STI
"""

import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔄 Iniciando Sistema de Tutoría Inteligente...")
    
    # Importar y crear la aplicación
    from app import create_app, db, login_manager
    from app.models import User, Student, Teacher, Course, Question, DiagnosticExam, LearningPath, Resource, Progress
    
    # Crear la aplicación
    app = create_app()
    
    @login_manager.user_loader
    def load_user(user_id):
        """Cargar usuario para Flask-Login"""
        return User.query.get(int(user_id))
    
    print("✅ Aplicación creada exitosamente")
    
    # Crear tablas si no existen
    with app.app_context():
        print("🔄 Inicializando base de datos...")
        db.create_all()
        print("✅ Base de datos inicializada")
        
        # Sincronizar preguntas VARK
        try:
            from app.ai.vark_forms_integration import VARKFormsIntegration
            vark_integration = VARKFormsIntegration()
            result = vark_integration.sync_vark_questions_to_database()
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"⚠️  VARK sync warning: {result['error']}")
        except Exception as e:
            print(f"⚠️  VARK sync warning: {e}")
    
    print("🚀 Iniciando servidor web...")
    print("🌐 Accede a: http://localhost:5000")
    print("📊 Dashboard: http://localhost:5000/student/dashboard")
    print("🔧 Presiona Ctrl+C para detener")
    print("=" * 50)
    
    # Ejecutar la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Asegúrate de que todas las dependencias estén instaladas:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
