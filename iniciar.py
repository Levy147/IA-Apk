#!/usr/bin/env python3
"""
Script simplificado para ejecutar el STI
Versión sin dependencias de Machine Learning
"""

import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("  SISTEMA DE TUTORÍA INTELIGENTE (STI)")
print("=" * 60)
print()

try:
    print("🔄 [1/4] Cargando módulos de Flask...")
    
    # Importar y crear la aplicación
    from app import create_app, db, login_manager
    
    print("✅ [2/4] Módulos cargados exitosamente")
    
    # Crear la aplicación
    print("🔄 [3/4] Inicializando aplicación...")
    app = create_app()
    
    # Importar modelos
    try:
        from app.models import User, Student, Teacher, Course, Question, DiagnosticExam, LearningPath, Resource, Progress
        
        @login_manager.user_loader
        def load_user(user_id):
            """Cargar usuario para Flask-Login"""
            return User.query.get(int(user_id))
            
    except ImportError as e:
        print(f"⚠️  Advertencia: No se pudieron importar todos los modelos: {e}")
    
    print("✅ [4/4] Aplicación creada exitosamente")
    print()
    
    # Crear tablas si no existen
    with app.app_context():
        print("🔄 Inicializando base de datos...")
        try:
            db.create_all()
            print("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"⚠️  Advertencia base de datos: {e}")
            print("   (La base de datos MySQL debe estar corriendo en XAMPP)")
    
    print()
    print("=" * 60)
    print("🚀 SERVIDOR WEB INICIADO")
    print("=" * 60)
    print()
    print("📍 Accede a la aplicación en:")
    print("   🌐 http://localhost:5000")
    print("   🌐 http://127.0.0.1:5000")
    print()
    print("📊 Rutas disponibles:")
    print("   • Inicio: http://localhost:5000/")
    print("   • Login: http://localhost:5000/auth/login")
    print("   • Registro: http://localhost:5000/auth/register")
    print()
    print("🔧 Presiona Ctrl+C para detener el servidor")
    print("=" * 60)
    print()
    
    # Ejecutar la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print()
    print("❌ ERROR DE IMPORTACIÓN")
    print("=" * 60)
    print(f"Error: {e}")
    print()
    print("💡 Solución:")
    print("   Instala las dependencias con:")
    print("   pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF")
    print("=" * 60)
    sys.exit(1)
    
except Exception as e:
    print()
    print("❌ ERROR INESPERADO")
    print("=" * 60)
    print(f"Error: {e}")
    print()
    import traceback
    traceback.print_exc()
    print("=" * 60)
    sys.exit(1)

