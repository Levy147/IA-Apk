"""
Script de inicialización de la base de datos para el STI
"""

from app import create_app, db
from app.models import User, Student, Teacher, Course, Question, VARKQuestion, Competency, Resource
from app.models.user import UserType
from app.models.assessment import QuestionType, DifficultyLevel
from app.models.learning import ResourceType
from app.models.progress import CompetencyLevel
from datetime import datetime
import os

def create_sample_data():
    """Crear datos de muestra para el sistema"""
    
    # Crear usuarios de ejemplo
    print("[CREATE] Creando usuarios de ejemplo...")
    
    # Usuario administrador
    admin_user = User(
        email='admin@sti.com',
        first_name='Administrador',
        last_name='STI',
        user_type=UserType.ADMIN
    )
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    
    # Docente de ejemplo
    teacher_user = User(
        email='herbert.galeano@sti.com',
        first_name='Herbert',
        last_name='Galeano',
        user_type=UserType.TEACHER
    )
    teacher_user.set_password('profesor123')
    db.session.add(teacher_user)
    db.session.flush()  # Para obtener el ID
    
    teacher_profile = Teacher(
        user_id=teacher_user.id,
        teacher_id='T001',
        department='Matemáticas',
        specialization='Matemáticas y Estadística',
        years_experience=15
    )
    db.session.add(teacher_profile)
    
    # Estudiantes de ejemplo
    students_data = [
        {
            'email': 'estudiante1@sti.com',
            'first_name': 'Carlos',
            'last_name': 'López',
            'student_id': '2024001',
            'grade_level': 'universidad',
            'school': 'Universidad de San Carlos'
        },
        {
            'email': 'estudiante2@sti.com',
            'first_name': 'Ana',
            'last_name': 'Martínez',
            'student_id': '2024002',
            'grade_level': 'universidad',
            'school': 'Universidad de San Carlos'
        },
        {
            'email': 'estudiante3@sti.com',
            'first_name': 'Luis',
            'last_name': 'Rodríguez',
            'student_id': '2024003',
            'grade_level': 'universidad',
            'school': 'Universidad de San Carlos'
        }
    ]
    
    for student_data in students_data:
        user = User(
            email=student_data['email'],
            first_name=student_data['first_name'],
            last_name=student_data['last_name'],
            user_type=UserType.STUDENT
        )
        user.set_password('estudiante123')
        db.session.add(user)
        db.session.flush()
        
        student_profile = Student(
            user_id=user.id,
            student_id=student_data['student_id'],
            grade_level=student_data['grade_level'],
            school=student_data['school']
        )
        db.session.add(student_profile)
    
    print("[OK] Usuarios creados exitosamente")
    
    # Crear cursos de ejemplo
    print("[COURSE] Creando cursos...")
    
    courses_data = [
        {
            'name': 'Matemática Básica 1',
            'description': 'Curso introductorio de matemáticas que cubre conceptos fundamentales de álgebra, geometría y aritmética. Incluye recursos VARK adaptados a tu estilo de aprendizaje.',
            'code': 'MATH-BAS-1',
            'subject': 'Matemáticas',
            'credits': 4
        },
        {
            'name': 'Química General 1',
            'description': 'Fundamentos de química: estructura atómica, tabla periódica, enlaces químicos y reacciones. Enfoque teórico-práctico con laboratorios.',
            'code': 'QUIM-GEN-1',
            'subject': 'Ciencias',
            'credits': 4
        },
        {
            'name': 'Técnica Complementaria 1',
            'description': 'Curso del área técnica complementaria enfocado en desarrollo de habilidades prácticas y aplicación de conocimientos. Recursos VARK incluidos.',
            'code': 'TEC-COMP-1',
            'subject': 'Área Técnica',
            'credits': 3
        },
        {
            'name': 'Social Humanística 1',
            'description': 'Introducción a las ciencias sociales y humanidades. Estudio de sociedades, cultura, historia y pensamiento social. Recursos VARK adaptados.',
            'code': 'SOC-HUM-1',
            'subject': 'Ciencias Sociales',
            'credits': 3
        }
    ]
    
    courses = []
    for course_data in courses_data:
        course = Course(
            name=course_data['name'],
            description=course_data['description'],
            code=course_data['code'],
            teacher_id=teacher_profile.id,
            grade_level='universidad',
            subject=course_data['subject'],
            credits=course_data['credits'],
            diagnostic_required=True,
            min_diagnostic_questions=25
        )
        db.session.add(course)
        courses.append(course)
    
    db.session.flush()
    
    print(f"[OK] {len(courses)} cursos creados exitosamente")
    
    # Crear competencias
    print("[TARGET] Creando competencias...")
    
    competencies_data = [
        {
            'name': 'Operaciones Básicas',
            'description': 'Dominio de suma, resta, multiplicación y división',
            'code': 'MATH101-001',
            'level': CompetencyLevel.BEGINNER
        },
        {
            'name': 'Álgebra Elemental',
            'description': 'Resolución de ecuaciones lineales y sistemas de ecuaciones',
            'code': 'MATH101-002',
            'level': CompetencyLevel.INTERMEDIATE
        },
        {
            'name': 'Geometría Básica',
            'description': 'Conceptos de ángulos, triángulos y figuras geométricas',
            'code': 'MATH101-003',
            'level': CompetencyLevel.BEGINNER
        },
        {
            'name': 'Funciones y Gráficas',
            'description': 'Comprensión de funciones lineales y cuadráticas',
            'code': 'MATH101-004',
            'level': CompetencyLevel.INTERMEDIATE
        }
    ]
    
    competencies = []
    for comp_data in competencies_data:
        competency = Competency(
            course_id=courses[0].id,  # Matemáticas Básicas
            name=comp_data['name'],
            description=comp_data['description'],
            code=comp_data['code'],
            level=comp_data['level'],
            is_core=True,
            weight=1.0,
            estimated_hours=10
        )
        db.session.add(competency)
        competencies.append(competency)
    
    db.session.flush()
    print("[OK] Competencias creadas exitosamente")
    
    # Crear preguntas de ejemplo
    print("[QUESTION] Creando preguntas de ejemplo...")
    
    questions_data = [
        {
            'text': '¿Cuál es el resultado de 15 + 27?',
            'type': QuestionType.MULTIPLE_CHOICE,
            'difficulty': DifficultyLevel.EASY,
            'option_a': '40',
            'option_b': '42',
            'option_c': '41',
            'option_d': '43',
            'correct_answer': 'B',
            'explanation': '15 + 27 = 42',
            'competency_id': competencies[0].id
        },
        {
            'text': 'Resuelve la ecuación: 2x + 5 = 13',
            'type': QuestionType.MULTIPLE_CHOICE,
            'difficulty': DifficultyLevel.MEDIUM,
            'option_a': 'x = 3',
            'option_b': 'x = 4',
            'option_c': 'x = 5',
            'option_d': 'x = 6',
            'correct_answer': 'B',
            'explanation': '2x + 5 = 13 → 2x = 8 → x = 4',
            'competency_id': competencies[1].id
        },
        {
            'text': '¿Cuál es la suma de los ángulos internos de un triángulo?',
            'type': QuestionType.MULTIPLE_CHOICE,
            'difficulty': DifficultyLevel.EASY,
            'option_a': '90°',
            'option_b': '180°',
            'option_c': '270°',
            'option_d': '360°',
            'correct_answer': 'B',
            'explanation': 'La suma de los ángulos internos de un triángulo siempre es 180°',
            'competency_id': competencies[2].id
        }
    ]
    
    for q_data in questions_data:
        question = Question(
            course_id=courses[0].id,  # Matemáticas Básicas
            competency_id=q_data['competency_id'],
            question_text=q_data['text'],
            question_type=q_data['type'],
            difficulty=q_data['difficulty'],
            option_a=q_data['option_a'],
            option_b=q_data['option_b'],
            option_c=q_data['option_c'],
            option_d=q_data['option_d'],
            correct_answer=q_data['correct_answer'],
            explanation=q_data['explanation'],
            points=1
        )
        db.session.add(question)
    
    print("[OK] Preguntas creadas exitosamente")
    
    # Crear recursos de ejemplo
    print("[RESOURCE] Creando recursos de ejemplo...")
    
    resources_data = [
        {
            'title': 'Video: Operaciones Básicas',
            'description': 'Video explicativo sobre suma, resta, multiplicación y división',
            'type': ResourceType.VIDEO,
            'content_url': 'https://example.com/video-operaciones',
            'difficulty_level': 'easy',
            'duration': 15,
            'visual_score': 0.9,
            'auditory_score': 0.8,
            'reading_score': 0.3,
            'kinesthetic_score': 0.2,
            'competency_id': competencies[0].id
        },
        {
            'title': 'Ejercicios de Álgebra',
            'description': 'Serie de ejercicios para practicar ecuaciones lineales',
            'type': ResourceType.EXERCISE,
            'content_text': 'Resuelve las siguientes ecuaciones...',
            'difficulty_level': 'medium',
            'duration': 30,
            'visual_score': 0.4,
            'auditory_score': 0.2,
            'reading_score': 0.8,
            'kinesthetic_score': 0.6,
            'competency_id': competencies[1].id
        },
        {
            'title': 'Simulación: Geometría Interactiva',
            'description': 'Simulación interactiva para explorar conceptos geométricos',
            'type': ResourceType.SIMULATION,
            'content_url': 'https://example.com/simulacion-geometria',
            'difficulty_level': 'easy',
            'duration': 20,
            'visual_score': 0.8,
            'auditory_score': 0.3,
            'reading_score': 0.4,
            'kinesthetic_score': 0.9,
            'competency_id': competencies[2].id
        }
    ]
    
    for res_data in resources_data:
        resource = Resource(
            course_id=courses[0].id,  # Matemáticas Básicas
            competency_id=res_data['competency_id'],
            title=res_data['title'],
            description=res_data['description'],
            resource_type=res_data['type'],
            content_url=res_data.get('content_url'),
            content_text=res_data.get('content_text'),
            difficulty_level=res_data['difficulty_level'],
            duration=res_data['duration'],
            visual_score=res_data['visual_score'],
            auditory_score=res_data['auditory_score'],
            reading_score=res_data['reading_score'],
            kinesthetic_score=res_data['kinesthetic_score'],
            points=1
        )
        db.session.add(resource)
    
    print("[OK] Recursos creados exitosamente")
    
    # Crear preguntas VARK
    print("[BRAIN] Creando preguntas VARK...")
    
    vark_questions_data = [
        {
            'question_number': 1,
            'question_text': 'Cuando aprendo algo nuevo, prefiero:',
            'option_v': 'Ver diagramas, gráficos o videos',
            'option_a': 'Escuchar explicaciones o discusiones',
            'option_r': 'Leer textos y tomar notas',
            'option_k': 'Hacer actividades prácticas o experimentos'
        },
        {
            'question_number': 2,
            'question_text': 'Para recordar información, me resulta más fácil:',
            'option_v': 'Visualizar imágenes o diagramas',
            'option_a': 'Repetir en voz alta o escuchar',
            'option_r': 'Escribir o leer varias veces',
            'option_k': 'Hacer movimientos o gestos'
        },
        {
            'question_number': 3,
            'question_text': 'Cuando estudio, prefiero:',
            'option_v': 'Usar colores, mapas mentales y diagramas',
            'option_a': 'Discutir con otros o explicar en voz alta',
            'option_r': 'Hacer listas, esquemas y resúmenes',
            'option_k': 'Tomar descansos frecuentes y moverme'
        }
    ]
    
    for vq_data in vark_questions_data:
        vark_question = VARKQuestion(
            question_text=vq_data['question_text'],
            question_number=vq_data['question_number'],
            option_v=vq_data['option_v'],
            option_a=vq_data['option_a'],
            option_r=vq_data['option_r'],
            option_k=vq_data['option_k']
        )
        db.session.add(vark_question)
    
    print("[OK] Preguntas VARK creadas exitosamente")
    
    # Confirmar cambios
    db.session.commit()
    print("[SUCCESS] Base de datos inicializada exitosamente!")
    print("\n[LIST] Credenciales de acceso:")
    print("[ADMIN] Administrador: admin@sti.com / admin123")
    print("[TEACHER] Docente: profesor@sti.com / profesor123")
    print("[STUDENT] Estudiantes: estudiante1@sti.com / estudiante123")
    print("                    estudiante2@sti.com / estudiante123")
    print("                    estudiante3@sti.com / estudiante123")

def main():
    """Función principal"""
    print("[START] Inicializando Sistema de Tutoría Inteligente (STI)")
    print("=" * 60)
    
    # Crear aplicación
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas
        print("[DATABASE] Creando tablas de la base de datos...")
        db.create_all()
        print("[OK] Tablas creadas exitosamente")
        
        # Verificar si ya hay datos
        if User.query.count() > 0:
            print("[WARNING] La base de datos ya contiene datos. ¿Deseas continuar? (y/N)")
            response = input().strip().lower()
            if response != 'y':
                print("[ERROR] Inicialización cancelada")
                return
        
        # Crear datos de muestra
        create_sample_data()
        
        print("\n[TARGET] Inicialización completada!")
        print("[WEB] Puedes acceder al sistema en: http://localhost:5000")

if __name__ == '__main__':
    main()
