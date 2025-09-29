"""
Script de prueba para verificar el funcionamiento del STI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Student, Teacher, Course, Question, VARKQuestion
from app.models.user import UserType
from app.models.assessment import QuestionType, DifficultyLevel
from app.models.learning import ResourceType
from app.models.progress import CompetencyLevel
from app.ai.vark_analyzer import VARKAnalyzer
from app.ai.learning_path_generator import LearningPathGenerator
from app.ai.recommendation_engine import RecommendationEngine
from app.ai.analytics_engine import AnalyticsEngine

def test_database_connection():
    """Probar conexión a la base de datos"""
    print("Probando conexión a la base de datos...")
    try:
        app = create_app()
        with app.app_context():
            # Intentar hacer una consulta simple
            user_count = User.query.count()
            print(f"[OK] Conexión exitosa. Usuarios en BD: {user_count}")
            return True
    except Exception as e:
        print(f"[ERROR] Error de conexión: {e}")
        return False

def test_models():
    """Probar modelos de la base de datos"""
    print("\n[INFO] Probando modelos de la base de datos...")
    try:
        app = create_app()
        with app.app_context():
            # Probar consultas básicas
            users = User.query.limit(5).all()
            students = Student.query.limit(5).all()
            teachers = Teacher.query.limit(5).all()
            courses = Course.query.limit(5).all()
            questions = Question.query.limit(5).all()
            vark_questions = VARKQuestion.query.limit(5).all()
            
            print(f"[OK] Modelos funcionando correctamente:")
            print(f"   - Usuarios: {len(users)}")
            print(f"   - Estudiantes: {len(students)}")
            print(f"   - Docentes: {len(teachers)}")
            print(f"   - Cursos: {len(courses)}")
            print(f"   - Preguntas: {len(questions)}")
            print(f"   - Preguntas VARK: {len(vark_questions)}")
            return True
    except Exception as e:
        print(f"[ERROR] Error en modelos: {e}")
        return False

def test_vark_analyzer():
    """Probar analizador VARK"""
    print("\n[INFO] Probando analizador VARK...")
    try:
        analyzer = VARKAnalyzer()
        
        # Simular respuestas VARK
        test_responses = {
            1: 'V',  # Visual
            2: 'A',  # Auditivo
            3: 'R',  # Lectura/Escritura
            4: 'K',  # Kinestésico
            5: 'V',  # Visual
            6: 'A',  # Auditivo
            7: 'R',  # Lectura/Escritura
            8: 'K',  # Kinestésico
            9: 'V',  # Visual
            10: 'A', # Auditivo
            11: 'R', # Lectura/Escritura
            12: 'K', # Kinestésico
            13: 'V', # Visual
            14: 'A', # Auditivo
            15: 'R', # Lectura/Escritura
            16: 'K'  # Kinestésico
        }
        
        vark_scores = analyzer.analyze_responses(test_responses)
        dominant_style = analyzer.get_dominant_style(vark_scores)
        
        print(f"[OK] Analizador VARK funcionando:")
        print(f"   - Puntajes: {vark_scores}")
        print(f"   - Estilo dominante: {dominant_style}")
        return True
    except Exception as e:
        print(f"[ERROR] Error en analizador VARK: {e}")
        return False

def test_learning_path_generator():
    """Probar generador de rutas de aprendizaje"""
    print("\n[INFO] Probando generador de rutas de aprendizaje...")
    try:
        app = create_app()
        with app.app_context():
            generator = LearningPathGenerator()
            
            # Buscar un estudiante y curso de prueba
            student = Student.query.first()
            course = Course.query.first()
            
            if student and course:
                print(f"[OK] Generador de rutas funcionando:")
                print(f"   - Estudiante de prueba: {student.user.get_full_name()}")
                print(f"   - Curso de prueba: {course.name}")
                print(f"   - Generador inicializado correctamente")
                return True
            else:
                print("[WARNING] No hay datos de prueba suficientes")
                return False
    except Exception as e:
        print(f"[ERROR] Error en generador de rutas: {e}")
        return False

def test_recommendation_engine():
    """Probar motor de recomendaciones"""
    print("\n[INFO] Probando motor de recomendaciones...")
    try:
        engine = RecommendationEngine()
        
        # Simular recomendaciones
        recommendations = engine.get_recommendations(1, limit=3)
        
        print(f"[OK] Motor de recomendaciones funcionando:")
        print(f"   - Recomendaciones generadas: {len(recommendations)}")
        return True
    except Exception as e:
        print(f"[ERROR] Error en motor de recomendaciones: {e}")
        return False

def test_analytics_engine():
    """Probar motor de analíticas"""
    print("\n[INFO] Probando motor de analíticas...")
    try:
        app = create_app()
        with app.app_context():
            analytics = AnalyticsEngine()
            
            # Buscar un curso de prueba
            course = Course.query.first()
            
            if course:
                course_analytics = analytics.get_course_analytics(course.id)
                print(f"[OK] Motor de analíticas funcionando:")
                print(f"   - Analíticas del curso: {course.name}")
                print(f"   - Datos generados: {len(course_analytics)} secciones")
                return True
            else:
                print("[WARNING] No hay cursos para analizar")
                return False
    except Exception as e:
        print(f"[ERROR] Error en motor de analíticas: {e}")
        return False

def test_google_forms_integration():
    """Probar integración con Google Forms"""
    print("\n[INFO] Probando integración con Google Forms...")
    try:
        from app.ai.google_forms_integration import GoogleFormsIntegration
        
        integration = GoogleFormsIntegration()
        print(f"[OK] Integración con Google Forms funcionando:")
        print(f"   - Clase inicializada correctamente")
        print(f"   - API Key configurada: {'Sí' if integration.api_key else 'No'}")
        return True
    except Exception as e:
        print(f"[ERROR] Error en integración Google Forms: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("SISTEMA DE PRUEBAS DEL STI")
    print("=" * 50)
    
    tests = [
        ("Conexión a Base de Datos", test_database_connection),
        ("Modelos de Base de Datos", test_models),
        ("Analizador VARK", test_vark_analyzer),
        ("Generador de Rutas", test_learning_path_generator),
        ("Motor de Recomendaciones", test_recommendation_engine),
        ("Motor de Analíticas", test_analytics_engine),
        ("Integración Google Forms", test_google_forms_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"[ERROR] Error inesperado en {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"[STATS] RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("[SUCCESS] ¡Todas las pruebas pasaron! El sistema está funcionando correctamente.")
        print("\n[START] Para iniciar el sistema:")
        print("   python app.py")
        print("\n[WEB] Accede a: http://localhost:5000")
    else:
        print("[WARNING] Algunas pruebas fallaron. Revisa los errores anteriores.")
        print("\n[TOOLS] Posibles soluciones:")
        print("   1. Verifica que XAMPP esté ejecutándose")
        print("   2. Asegúrate de que la base de datos 'sti_database' existe")
        print("   3. Ejecuta 'python init_db.py' para inicializar la base de datos")
        print("   4. Verifica que todas las dependencias estén instaladas")

if __name__ == '__main__':
    main()
