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
from app.ai.vark_forms_integration import VARKFormsIntegration
from datetime import datetime
import json
from config import Config

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

@bp.route('/profile')
@login_required
def profile():
    """Perfil del estudiante con estadísticas detalladas"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    
    return render_template('student/profile.html', 
                         title='Mi Perfil',
                         student=student)

@bp.route('/profile/learning-style', methods=['POST'])
@login_required
def update_learning_style():
    """Actualizar manualmente el estilo de aprendizaje detectado (VARK)"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))

    student = current_user.student_profile
    style = (request.form.get('learning_style') or '').upper()

    valid = {'V', 'A', 'R', 'K'}
    if style not in valid:
        flash('Estilo no válido. Usa V, A, R o K.', 'error')
        return redirect(url_for('student.profile'))

    # Solo actualiza el dominante; puntajes se mantienen si existen
    student.dominant_learning_style = style
    db.session.commit()
    flash('Estilo de aprendizaje actualizado.', 'success')
    return redirect(url_for('student.profile'))

@bp.route('/resources')
@login_required
def resources():
    """Recursos de aprendizaje del estudiante"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('student/resources.html',
                         title='Recursos de Aprendizaje')

@bp.route('/all-courses')
@login_required
def all_courses():
    """Todos los cursos con enlaces a Drive"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('student/all_courses.html',
                         title='Todos los Cursos')

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

@bp.route('/course/<int:course_id>/units')
@login_required
def course_units(course_id):
    """Ver unidades del curso con enlaces a Drive"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    course = Course.query.get_or_404(course_id)
    
    return render_template('student/course_units.html',
                         title=f'Unidades - {course.name}',
                         course=course)

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

    # Si hay un formulario externo configurado para este curso, redirigir a ese flujo
    name = (course.name or '').lower()
    external_form_url = None
    if 'química' in name or 'quimica' in name:
        external_form_url = Config.DIAGNOSTIC_FORMS.get('quimica')
    elif 'técnica' in name or 'tecnica' in name:
        external_form_url = Config.DIAGNOSTIC_FORMS.get('tecnica_complementaria')
    elif 'humanística' in name or 'humanistica' in name or 'social' in name:
        external_form_url = Config.DIAGNOSTIC_FORMS.get('humanistica')
    elif 'matemát' in name or 'matemat' in name:
        external_form_url = Config.DIAGNOSTIC_FORMS.get('matematica')

    if external_form_url:
        return redirect(url_for('student.diagnostic_external_form', course_id=course_id))
    
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
    
    # Obtener preguntas del examen (flujo genérico solo si no hay formulario externo)
    questions = get_diagnostic_questions(course_id, diagnostic.total_questions)
    
    return render_template('student/diagnostic_exam.html',
                         title='Examen Diagnóstico',
                         course=course,
                         diagnostic=diagnostic,
                         questions=questions)

@bp.route('/diagnostic/form/<int:course_id>')
@login_required
def diagnostic_external_form(course_id):
    """Mostrar formulario de diagnóstico externo (Google Forms) por curso"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))

    student = current_user.student_profile
    course = Course.query.get_or_404(course_id)

    # Resolver URL del formulario según el nombre del curso
    name = (course.name or '').lower()
    form_url = None
    if 'química' in name or 'quimica' in name:
        form_url = Config.DIAGNOSTIC_FORMS.get('quimica')
    elif 'técnica' in name or 'tecnica' in name:
        form_url = Config.DIAGNOSTIC_FORMS.get('tecnica_complementaria')
    elif 'humanística' in name or 'humanistica' in name or 'social' in name:
        form_url = Config.DIAGNOSTIC_FORMS.get('humanistica')
    elif 'matemát' in name or 'matemat' in name:
        form_url = Config.DIAGNOSTIC_FORMS.get('matematica')

    if not form_url:
        flash('No hay formulario de diagnóstico configurado para este curso.', 'warning')
        return redirect(url_for('student.course_detail', course_id=course_id))

    return render_template('student/diagnostic_external_form.html',
                         title=f'Diagnóstico - {course.name}',
                         course=course,
                         form_url=form_url)

@bp.route('/diagnostic/<int:course_id>', methods=['POST'])
@login_required
def submit_diagnostic(course_id):
    """Procesar respuestas del examen diagnóstico"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    course = Course.query.get_or_404(course_id)
    
    # Obtener el examen diagnóstico
    diagnostic = DiagnosticExam.query.filter_by(
        course_id=course_id,
        student_id=student.id,
        is_completed=False
    ).first()
    
    if not diagnostic:
        flash('No se encontró el examen diagnóstico.', 'error')
        return redirect(url_for('student.course_detail', course_id=course_id))
    
    # Procesar respuestas (simulado - en producción vendría de Google Forms)
    total_questions = diagnostic.total_questions
    correct_answers = 0
    
    # Contar respuestas correctas (simulado)
    import random
    correct_answers = random.randint(int(total_questions * 0.6), total_questions)
    
    # Actualizar examen
    diagnostic.is_completed = True
    diagnostic.completed_at = datetime.utcnow()
    diagnostic.total_score = correct_answers
    diagnostic.percentage = (correct_answers / total_questions) * 100
    
    # Actualizar perfil del estudiante
    student.diagnostic_completed = True
    student.diagnostic_score = diagnostic.percentage
    student.diagnostic_date = datetime.utcnow()
    
    db.session.commit()
    
    flash(f'¡Examen completado! Tu calificación: {diagnostic.percentage:.1f}%', 'success')
    return redirect(url_for('student.course_detail', course_id=course_id))

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
    return redirect(url_for('student.course_selection'))

@bp.route('/course-selection')
@login_required
def course_selection():
    """Página de selección de cursos después del VARK"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    
    # Verificar que haya completado el VARK
    if not student.dominant_learning_style:
        flash('Debes completar el cuestionario VARK primero.', 'warning')
        return redirect(url_for('student.vark_external_form'))
    
    # Obtener cursos disponibles (no matriculados)
    enrolled_course_ids = [e.course_id for e in student.enrollments]
    available_courses = Course.query.filter(
        Course.id.notin_(enrolled_course_ids),
        Course.status == 'active'
    ).all()
    
    # Obtener información del perfil VARK
    vark_style_names = {
        'V': 'Visual',
        'A': 'Auditivo', 
        'R': 'Lectura/Escritura',
        'K': 'Kinestésico'
    }
    
    vark_descriptions = {
        'V': 'Prefieres aprender con diagramas, gráficos e imágenes',
        'A': 'Prefieres explicaciones orales y contenido de audio',
        'R': 'Prefieres leer textos y tomar notas detalladas',
        'K': 'Prefieres actividades prácticas y experiencias hands-on'
    }
    
    return render_template('student/course_selection.html',
                         title='Seleccionar Curso',
                         student=student,
                         available_courses=available_courses,
                         vark_style_name=vark_style_names.get(student.dominant_learning_style, ''),
                         vark_description=vark_descriptions.get(student.dominant_learning_style, ''))

@bp.route('/enroll-course/<int:course_id>')
@login_required
def enroll_course(course_id):
    """Matricular estudiante en un curso"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    course = Course.query.get_or_404(course_id)
    
    # Verificar que no esté ya matriculado
    existing_enrollment = next((e for e in student.enrollments if e.course_id == course_id), None)
    if existing_enrollment:
        flash('Ya estás matriculado en este curso.', 'info')
        return redirect(url_for('student.course_detail', course_id=course_id))
    
    # Crear matrícula
    from app.models import CourseEnrollment
    enrollment = CourseEnrollment(
        student_id=student.id,
        course_id=course_id,
        enrollment_date=datetime.utcnow(),
        is_active=True
    )
    
    db.session.add(enrollment)
    db.session.commit()
    
    flash(f'¡Te has matriculado exitosamente en {course.name}!', 'success')
    return redirect(url_for('student.diagnostic_exam', course_id=course_id))

@bp.route('/vark-external')
@login_required
def vark_external_form():
    """Redirigir al formulario VARK externo de Google Forms"""
    if current_user.user_type.value != 'student':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    student = current_user.student_profile
    
    # Verificar si ya completó el cuestionario VARK
    if student.dominant_learning_style:
        flash('Ya completaste el cuestionario de estilos de aprendizaje.', 'info')
        return redirect(url_for('student.dashboard'))
    
    # Obtener URL del formulario VARK
    vark_integration = VARKFormsIntegration()
    form_url = vark_integration.get_vark_form_url()
    
    return render_template('student/vark_external_form.html',
                         title='Cuestionario de Estilos de Aprendizaje',
                         form_url=form_url,
                         student_id=student.id)

@bp.route('/vark-completed/<int:student_id>', methods=['POST'])
def vark_completed_webhook(student_id):
    """Webhook para procesar respuestas del formulario VARK externo"""
    try:
        # Obtener datos del formulario
        form_data = request.form.to_dict()
        
        # Procesar respuestas usando la integración VARK
        vark_integration = VARKFormsIntegration()
        result = vark_integration.process_vark_responses_from_forms(student_id, form_data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Respuestas VARK procesadas exitosamente',
                'vark_scores': result['vark_scores'],
                'dominant_style': result['dominant_style']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/vark-manual-sync/<int:student_id>', methods=['POST'])
@login_required
def vark_manual_sync(student_id):
    """Sincronización manual de respuestas VARK desde Google Forms"""
    if current_user.user_type.value != 'student':
        return jsonify({'success': False, 'error': 'Acceso denegado'}), 403
    
    student = current_user.student_profile
    if student.id != student_id:
        return jsonify({'success': False, 'error': 'Acceso denegado'}), 403
    
    try:
        # Obtener datos del formulario (simulado por ahora)
        # En una implementación real, esto vendría de la API de Google Forms
        form_data = request.json or {}
        
        if not form_data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos del formulario'
            }), 400
        
        # Procesar respuestas
        vark_integration = VARKFormsIntegration()
        result = vark_integration.process_vark_responses_from_forms(student_id, form_data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Perfil VARK actualizado exitosamente',
                'vark_scores': result['vark_scores'],
                'dominant_style': result['dominant_style'],
                'learning_preferences': result['learning_preferences']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
    # Preguntas básicas de matemáticas
    basic_questions = [
        {'text': '¿Cuánto es 5 + 3?', 'options': {'A': '6', 'B': '7', 'C': '8', 'D': '9'}, 'correct': 'C'},
        {'text': '¿Cuánto es 12 - 4?', 'options': {'A': '6', 'B': '7', 'C': '8', 'D': '9'}, 'correct': 'C'},
        {'text': '¿Cuánto es 6 × 2?', 'options': {'A': '10', 'B': '11', 'C': '12', 'D': '13'}, 'correct': 'C'},
        {'text': '¿Cuánto es 20 ÷ 4?', 'options': {'A': '4', 'B': '5', 'C': '6', 'D': '7'}, 'correct': 'B'},
        {'text': '¿Cuánto es 10 + 15?', 'options': {'A': '20', 'B': '25', 'C': '30', 'D': '35'}, 'correct': 'B'},
        {'text': '¿Cuánto es 30 - 12?', 'options': {'A': '16', 'B': '17', 'C': '18', 'D': '19'}, 'correct': 'C'},
        {'text': '¿Cuánto es 7 × 3?', 'options': {'A': '19', 'B': '20', 'C': '21', 'D': '22'}, 'correct': 'C'},
        {'text': '¿Cuánto es 24 ÷ 6?', 'options': {'A': '3', 'B': '4', 'C': '5', 'D': '6'}, 'correct': 'B'},
        {'text': '¿Cuánto es 9 + 8?', 'options': {'A': '15', 'B': '16', 'C': '17', 'D': '18'}, 'correct': 'C'},
        {'text': '¿Cuánto es 25 - 7?', 'options': {'A': '16', 'B': '17', 'C': '18', 'D': '19'}, 'correct': 'C'},
        {'text': '¿Cuánto es 4 × 5?', 'options': {'A': '18', 'B': '19', 'C': '20', 'D': '21'}, 'correct': 'C'},
        {'text': '¿Cuánto es 36 ÷ 9?', 'options': {'A': '3', 'B': '4', 'C': '5', 'D': '6'}, 'correct': 'B'},
        {'text': '¿Cuánto es 11 + 14?', 'options': {'A': '23', 'B': '24', 'C': '25', 'D': '26'}, 'correct': 'C'},
        {'text': '¿Cuánto es 40 - 15?', 'options': {'A': '23', 'B': '24', 'C': '25', 'D': '26'}, 'correct': 'C'},
        {'text': '¿Cuánto es 8 × 4?', 'options': {'A': '30', 'B': '31', 'C': '32', 'D': '33'}, 'correct': 'C'},
        {'text': '¿Cuánto es 45 ÷ 5?', 'options': {'A': '7', 'B': '8', 'C': '9', 'D': '10'}, 'correct': 'C'},
        {'text': '¿Cuánto es 13 + 9?', 'options': {'A': '20', 'B': '21', 'C': '22', 'D': '23'}, 'correct': 'C'},
        {'text': '¿Cuánto es 50 - 18?', 'options': {'A': '30', 'B': '31', 'C': '32', 'D': '33'}, 'correct': 'C'},
        {'text': '¿Cuánto es 9 × 5?', 'options': {'A': '43', 'B': '44', 'C': '45', 'D': '46'}, 'correct': 'C'},
        {'text': '¿Cuánto es 64 ÷ 8?', 'options': {'A': '6', 'B': '7', 'C': '8', 'D': '9'}, 'correct': 'C'},
        {'text': '¿Cuánto es 17 + 6?', 'options': {'A': '21', 'B': '22', 'C': '23', 'D': '24'}, 'correct': 'C'},
        {'text': '¿Cuánto es 35 - 11?', 'options': {'A': '22', 'B': '23', 'C': '24', 'D': '25'}, 'correct': 'C'},
        {'text': '¿Cuánto es 6 × 7?', 'options': {'A': '40', 'B': '41', 'C': '42', 'D': '43'}, 'correct': 'C'},
        {'text': '¿Cuánto es 72 ÷ 9?', 'options': {'A': '6', 'B': '7', 'C': '8', 'D': '9'}, 'correct': 'C'},
        {'text': '¿Cuánto es 19 + 12?', 'options': {'A': '29', 'B': '30', 'C': '31', 'D': '32'}, 'correct': 'C'},
    ]
    
    questions = []
    for i in range(min(total_questions, len(basic_questions))):
        q = basic_questions[i]
        questions.append({
            'id': i + 1,
            'text': q['text'],
            'type': 'multiple_choice',
            'options': q['options'],
            'correct_answer': q['correct']
        })
    
    return questions
