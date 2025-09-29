"""
Rutas para estudiantes
"""

from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from app.student import bp
from app.models import Student, Course, DiagnosticExam, LearningPath, VARKQuestion, VARKResponse
from app import db
from app.student.forms import VARKForm
from app.ai.learning_path_generator import LearningPathGenerator
from app.ai.vark_analyzer import VARKAnalyzer
import json

@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard del estudiante"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    if not student:
        flash('Perfil de estudiante no encontrado.', 'error')
        return redirect(url_for('auth.logout'))
    
    # Obtener cursos matriculados
    enrollments = student.enrollments
    active_courses = [e.course for e in enrollments if e.is_active]
    
    # Obtener progreso general
    total_progress = sum(e.overall_progress for e in enrollments if e.is_active)
    avg_progress = total_progress / len(active_courses) if active_courses else 0
    
    # Obtener exámenes diagnósticos completados
    completed_diagnostics = DiagnosticExam.query.filter_by(
        student_id=student.id, 
        is_completed=True
    ).count()
    
    # Obtener rutas de aprendizaje activas
    active_learning_paths = LearningPath.query.filter_by(
        student_id=student.id,
        is_active=True
    ).count()
    
    dashboard_data = {
        'student': student,
        'courses': active_courses,
        'avg_progress': avg_progress,
        'completed_diagnostics': completed_diagnostics,
        'active_learning_paths': active_learning_paths,
        'vark_profile': student.get_vark_profile() if student.diagnostic_completed else None
    }
    
    return render_template('student/dashboard.html', title='Mi Dashboard', **dashboard_data)

@bp.route('/courses')
@login_required
def courses():
    """Lista de cursos del estudiante"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    enrollments = student.enrollments
    
    return render_template('student/courses.html', 
                         title='Mis Cursos', 
                         enrollments=enrollments)

@bp.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    """Detalle de un curso específico"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    course = Course.query.get_or_404(course_id)
    
    # Verificar que el estudiante esté matriculado
    enrollment = next((e for e in student.enrollments if e.course_id == course_id), None)
    if not enrollment:
        flash('No estás matriculado en este curso.', 'error')
        return redirect(url_for('student.courses'))
    
    # Obtener examen diagnóstico del curso
    diagnostic = DiagnosticExam.query.filter_by(
        course_id=course_id,
        student_id=student.id
    ).first()
    
    # Obtener ruta de aprendizaje
    learning_path = LearningPath.query.filter_by(
        course_id=course_id,
        student_id=student.id,
        is_active=True
    ).first()
    
    return render_template('student/course_detail.html',
                         title=f'Curso: {course.name}',
                         course=course,
                         enrollment=enrollment,
                         diagnostic=diagnostic,
                         learning_path=learning_path)

@bp.route('/diagnostic/<int:course_id>')
@login_required
def diagnostic_exam(course_id):
    """Examen diagnóstico para un curso"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    course = Course.query.get_or_404(course_id)
    
    # Verificar que el estudiante esté matriculado
    enrollment = next((e for e in student.enrollments if e.course_id == course_id), None)
    if not enrollment:
        flash('No estás matriculado en este curso.', 'error')
        return redirect(url_for('student.courses'))
    
    # Verificar si ya completó el diagnóstico
    existing_diagnostic = DiagnosticExam.query.filter_by(
        course_id=course_id,
        student_id=student.id,
        is_completed=True
    ).first()
    
    if existing_diagnostic:
        flash('Ya completaste el examen diagnóstico para este curso.', 'info')
        return redirect(url_for('student.course_detail', course_id=course_id))
    
    # Obtener o crear examen diagnóstico
    diagnostic = DiagnosticExam.query.filter_by(
        course_id=course_id,
        student_id=student.id
    ).first()
    
    if not diagnostic:
        # Crear nuevo examen diagnóstico
        diagnostic = DiagnosticExam(
            course_id=course_id,
            student_id=student.id,
            title=f"Examen Diagnóstico - {course.name}",
            description="Este examen nos ayudará a personalizar tu experiencia de aprendizaje.",
            total_questions=course.min_diagnostic_questions or 25
        )
        db.session.add(diagnostic)
        db.session.commit()
    
    # Obtener preguntas del examen (simuladas por ahora)
    # En la implementación real, estas vendrían de Google Forms
    questions = get_diagnostic_questions(course_id, diagnostic.total_questions)
    
    return render_template('student/diagnostic_exam.html',
                         title='Examen Diagnóstico',
                         course=course,
                         diagnostic=diagnostic,
                         questions=questions)

@bp.route('/vark-questionnaire')
@login_required
def vark_questionnaire():
    """Cuestionario VARK para identificar estilo de aprendizaje"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    
    # Verificar si ya completó el cuestionario VARK
    if student.dominant_learning_style:
        flash('Ya completaste el cuestionario de estilos de aprendizaje.', 'info')
        return redirect(url_for('student.dashboard'))
    
    # Obtener preguntas VARK
    vark_questions = VARKQuestion.query.order_by(VARKQuestion.question_number).all()
    
    form = VARKForm()
    
    return render_template('student/vark_questionnaire.html',
                         title='Cuestionario de Estilos de Aprendizaje',
                         questions=vark_questions,
                         form=form)

@bp.route('/vark-questionnaire', methods=['POST'])
@login_required
def submit_vark_questionnaire():
    """Procesar respuestas del cuestionario VARK"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    
    # Obtener respuestas del formulario
    responses = {}
    for key, value in request.form.items():
        if key.startswith('question_'):
            question_id = int(key.split('_')[1])
            responses[question_id] = value
    
    # Analizar respuestas VARK
    analyzer = VARKAnalyzer()
    vark_scores = analyzer.analyze_responses(responses)
    
    # Guardar respuestas en la base de datos
    for question_id, response in responses.items():
        vark_response = VARKResponse(
            student_id=student.id,
            question_id=question_id,
            selected_option=response
        )
        db.session.add(vark_response)
    
    # Actualizar perfil VARK del estudiante
    student.update_vark_profile(
        vark_scores['visual'],
        vark_scores['auditory'],
        vark_scores['reading'],
        vark_scores['kinesthetic']
    )
    
    db.session.commit()
    
    flash('¡Cuestionario completado! Tu estilo de aprendizaje ha sido identificado.', 'success')
    return redirect(url_for('student.dashboard'))

@bp.route('/learning-path/<int:path_id>')
@login_required
def learning_path(path_id):
    """Ver ruta de aprendizaje personalizada"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    learning_path = LearningPath.query.get_or_404(path_id)
    
    # Verificar que la ruta pertenece al estudiante
    if learning_path.student_id != student.id:
        flash('Acceso denegado a esta ruta de aprendizaje.', 'error')
        return redirect(url_for('student.dashboard'))
    
    return render_template('student/learning_path.html',
                         title='Mi Ruta de Aprendizaje',
                         learning_path=learning_path)

def get_diagnostic_questions(course_id, total_questions):
    """Obtener preguntas del examen diagnóstico (simulado)"""
    # En la implementación real, esto se integraría con Google Forms
    # Por ahora, retornamos preguntas simuladas
    questions = []
    for i in range(total_questions):
        questions.append({
            'id': i + 1,
            'text': f'Pregunta {i + 1}: ¿Cuál es la respuesta correcta?',
            'type': 'multiple_choice',
            'options': {
                'A': 'Opción A',
                'B': 'Opción B',
                'C': 'Opción C',
                'D': 'Opción D'
            },
            'correct_answer': 'A'
        })
    return questions
