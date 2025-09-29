"""
Rutas de API REST para el STI
"""

from flask import request, jsonify, current_app
from flask_login import login_required, current_user
from app.api import bp
from app.models import Student, Course, DiagnosticExam, LearningPath, Progress
from app import db
from app.ai.google_forms_integration import GoogleFormsIntegration
from app.ai.learning_path_generator import LearningPathGenerator
import json

@bp.route('/google-forms/responses', methods=['POST'])
def receive_google_forms_responses():
    """Recibir respuestas del examen diagnóstico desde Google Forms"""
    try:
        data = request.get_json()
        
        # Validar datos recibidos
        if not data or 'student_email' not in data or 'responses' not in data:
            return jsonify({'error': 'Datos inválidos'}), 400
        
        # Buscar estudiante por email
        student = Student.query.join(Student.user).filter(
            User.email == data['student_email']
        ).first()
        
        if not student:
            return jsonify({'error': 'Estudiante no encontrado'}), 404
        
        # Procesar respuestas del examen diagnóstico
        google_forms = GoogleFormsIntegration()
        result = google_forms.process_diagnostic_responses(student.id, data['responses'])
        
        if result['success']:
            return jsonify({
                'message': 'Respuestas procesadas exitosamente',
                'diagnostic_id': result['diagnostic_id'],
                'score': result['score']
            })
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        current_app.logger.error(f"Error procesando respuestas de Google Forms: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@bp.route('/learning-path/generate', methods=['POST'])
@login_required
def generate_learning_path():
    """Generar ruta de aprendizaje personalizada"""
    if current_user.user_type.value != 'student':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    try:
        data = request.get_json()
        course_id = data.get('course_id')
        
        if not course_id:
            return jsonify({'error': 'ID de curso requerido'}), 400
        
        student = current_user.student_profile
        if not student:
            return jsonify({'error': 'Perfil de estudiante no encontrado'}), 404
        
        # Verificar que el estudiante esté matriculado
        enrollment = next((e for e in student.enrollments if e.course_id == course_id), None)
        if not enrollment:
            return jsonify({'error': 'No estás matriculado en este curso'}), 403
        
        # Generar ruta de aprendizaje
        generator = LearningPathGenerator()
        learning_path = generator.generate_path(student.id, course_id)
        
        if learning_path:
            return jsonify({
                'message': 'Ruta de aprendizaje generada exitosamente',
                'path_id': learning_path.id,
                'total_steps': learning_path.total_steps
            })
        else:
            return jsonify({'error': 'No se pudo generar la ruta de aprendizaje'}), 500
            
    except Exception as e:
        current_app.logger.error(f"Error generando ruta de aprendizaje: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@bp.route('/progress/update', methods=['POST'])
@login_required
def update_progress():
    """Actualizar progreso del estudiante"""
    if current_user.user_type.value != 'student':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    try:
        data = request.get_json()
        activity_type = data.get('activity_type')
        activity_id = data.get('activity_id')
        score = data.get('score')
        max_score = data.get('max_score')
        time_spent = data.get('time_spent')
        
        if not all([activity_type, activity_id, score is not None]):
            return jsonify({'error': 'Datos requeridos faltantes'}), 400
        
        student = current_user.student_profile
        if not student:
            return jsonify({'error': 'Perfil de estudiante no encontrado'}), 404
        
        # Crear registro de progreso
        progress = Progress(
            student_id=student.id,
            course_id=data.get('course_id'),
            enrollment_id=data.get('enrollment_id'),
            activity_type=activity_type,
            activity_id=activity_id,
            score=score,
            max_score=max_score,
            time_spent=time_spent
        )
        
        progress.calculate_percentage()
        db.session.add(progress)
        db.session.commit()
        
        return jsonify({
            'message': 'Progreso actualizado exitosamente',
            'progress_id': progress.id,
            'percentage': progress.percentage
        })
        
    except Exception as e:
        current_app.logger.error(f"Error actualizando progreso: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@bp.route('/vark/analyze', methods=['POST'])
@login_required
def analyze_vark_responses():
    """Analizar respuestas del cuestionario VARK"""
    if current_user.user_type.value != 'student':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    try:
        data = request.get_json()
        responses = data.get('responses')
        
        if not responses:
            return jsonify({'error': 'Respuestas VARK requeridas'}), 400
        
        from app.ai.vark_analyzer import VARKAnalyzer
        analyzer = VARKAnalyzer()
        vark_scores = analyzer.analyze_responses(responses)
        
        return jsonify({
            'message': 'Análisis VARK completado',
            'scores': vark_scores,
            'dominant_style': max(vark_scores, key=vark_scores.get)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error analizando VARK: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@bp.route('/recommendations/<int:student_id>')
@login_required
def get_recommendations(student_id):
    """Obtener recomendaciones personalizadas para un estudiante"""
    if current_user.user_type.value not in ['student', 'teacher']:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    try:
        # Verificar acceso
        if current_user.user_type.value == 'student' and current_user.student_profile.id != student_id:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        from app.ai.recommendation_engine import RecommendationEngine
        engine = RecommendationEngine()
        recommendations = engine.get_recommendations(student_id)
        
        return jsonify({
            'recommendations': recommendations
        })
        
    except Exception as e:
        current_app.logger.error(f"Error obteniendo recomendaciones: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@bp.route('/analytics/course/<int:course_id>')
@login_required
def get_course_analytics(course_id):
    """Obtener analíticas de un curso"""
    if current_user.user_type.value != 'teacher':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    try:
        teacher = current_user.teacher_profile
        course = Course.query.get_or_404(course_id)
        
        # Verificar que el curso pertenece al docente
        if course.teacher_id != teacher.id:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        # Obtener analíticas
        from app.ai.analytics_engine import AnalyticsEngine
        analytics_engine = AnalyticsEngine()
        analytics = analytics_engine.get_course_analytics(course_id)
        
        return jsonify(analytics)
        
    except Exception as e:
        current_app.logger.error(f"Error obteniendo analíticas: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
