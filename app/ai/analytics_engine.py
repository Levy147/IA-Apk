"""
Motor de analíticas para el STI
"""

from app.models import Student, Course, Progress, LearningPath, DiagnosticExam
from app import db
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import json

class AnalyticsEngine:
    """Motor de analíticas y reportes para el STI"""
    
    def __init__(self):
        pass
    
    def get_course_analytics(self, course_id):
        """
        Obtener analíticas completas de un curso
        
        Args:
            course_id (int): ID del curso
            
        Returns:
            dict: Analíticas del curso
        """
        try:
            course = Course.query.get(course_id)
            if not course:
                return {}
            
            analytics = {
                'course_info': {
                    'id': course.id,
                    'name': course.name,
                    'code': course.code,
                    'subject': course.subject
                },
                'enrollment_stats': self._get_enrollment_stats(course_id),
                'diagnostic_stats': self._get_diagnostic_stats(course_id),
                'learning_path_stats': self._get_learning_path_stats(course_id),
                'progress_analytics': self._get_progress_analytics(course_id),
                'learning_style_distribution': self._get_learning_style_distribution(course_id),
                'performance_trends': self._get_performance_trends(course_id),
                'engagement_metrics': self._get_engagement_metrics(course_id)
            }
            
            return analytics
            
        except Exception as e:
            print(f"Error obteniendo analíticas del curso: {e}")
            return {}
    
    def _get_enrollment_stats(self, course_id):
        """Obtener estadísticas de matrícula"""
        try:
            from app.models import CourseEnrollment
            
            total_enrollments = CourseEnrollment.query.filter_by(course_id=course_id).count()
            active_enrollments = CourseEnrollment.query.filter_by(
                course_id=course_id, 
                is_active=True
            ).count()
            completed_enrollments = CourseEnrollment.query.filter(
                CourseEnrollment.course_id == course_id,
                CourseEnrollment.completion_date.isnot(None)
            ).count()
            
            return {
                'total': total_enrollments,
                'active': active_enrollments,
                'completed': completed_enrollments,
                'completion_rate': (completed_enrollments / total_enrollments * 100) if total_enrollments > 0 else 0
            }
            
        except Exception as e:
            print(f"Error obteniendo estadísticas de matrícula: {e}")
            return {}
    
    def _get_diagnostic_stats(self, course_id):
        """Obtener estadísticas del examen diagnóstico"""
        try:
            total_diagnostics = DiagnosticExam.query.filter_by(course_id=course_id).count()
            completed_diagnostics = DiagnosticExam.query.filter_by(
                course_id=course_id,
                is_completed=True
            ).count()
            
            # Estadísticas de puntajes
            if completed_diagnostics > 0:
                avg_score = db.session.query(func.avg(DiagnosticExam.percentage)).filter(
                    DiagnosticExam.course_id == course_id,
                    DiagnosticExam.is_completed == True
                ).scalar() or 0
                
                min_score = db.session.query(func.min(DiagnosticExam.percentage)).filter(
                    DiagnosticExam.course_id == course_id,
                    DiagnosticExam.is_completed == True
                ).scalar() or 0
                
                max_score = db.session.query(func.max(DiagnosticExam.percentage)).filter(
                    DiagnosticExam.course_id == course_id,
                    DiagnosticExam.is_completed == True
                ).scalar() or 0
            else:
                avg_score = min_score = max_score = 0
            
            return {
                'total': total_diagnostics,
                'completed': completed_diagnostics,
                'completion_rate': (completed_diagnostics / total_diagnostics * 100) if total_diagnostics > 0 else 0,
                'avg_score': round(avg_score, 2),
                'min_score': round(min_score, 2),
                'max_score': round(max_score, 2)
            }
            
        except Exception as e:
            print(f"Error obteniendo estadísticas de diagnóstico: {e}")
            return {}
    
    def _get_learning_path_stats(self, course_id):
        """Obtener estadísticas de rutas de aprendizaje"""
        try:
            total_paths = LearningPath.query.filter_by(course_id=course_id).count()
            active_paths = LearningPath.query.filter_by(
                course_id=course_id,
                is_active=True
            ).count()
            completed_paths = LearningPath.query.filter_by(
                course_id=course_id,
                is_completed=True
            ).count()
            
            # Progreso promedio
            if active_paths > 0:
                avg_progress = db.session.query(func.avg(LearningPath.completion_percentage)).filter(
                    LearningPath.course_id == course_id,
                    LearningPath.is_active == True
                ).scalar() or 0
            else:
                avg_progress = 0
            
            return {
                'total': total_paths,
                'active': active_paths,
                'completed': completed_paths,
                'completion_rate': (completed_paths / total_paths * 100) if total_paths > 0 else 0,
                'avg_progress': round(avg_progress, 2)
            }
            
        except Exception as e:
            print(f"Error obteniendo estadísticas de rutas de aprendizaje: {e}")
            return {}
    
    def _get_progress_analytics(self, course_id):
        """Obtener analíticas de progreso"""
        try:
            # Obtener registros de progreso del curso
            progress_records = Progress.query.join(Progress.enrollment).filter(
                CourseEnrollment.course_id == course_id
            ).all()
            
            if not progress_records:
                return {}
            
            # Calcular estadísticas
            total_activities = len(progress_records)
            avg_percentage = sum(p.percentage for p in progress_records) / total_activities
            
            # Distribución por tipo de actividad
            activity_types = {}
            for record in progress_records:
                activity_type = record.activity_type
                if activity_type not in activity_types:
                    activity_types[activity_type] = {'count': 0, 'avg_score': 0}
                activity_types[activity_type]['count'] += 1
                activity_types[activity_type]['avg_score'] += record.percentage
            
            # Calcular promedios
            for activity_type in activity_types:
                count = activity_types[activity_type]['count']
                activity_types[activity_type]['avg_score'] = round(
                    activity_types[activity_type]['avg_score'] / count, 2
                )
            
            return {
                'total_activities': total_activities,
                'avg_percentage': round(avg_percentage, 2),
                'activity_distribution': activity_types
            }
            
        except Exception as e:
            print(f"Error obteniendo analíticas de progreso: {e}")
            return {}
    
    def _get_learning_style_distribution(self, course_id):
        """Obtener distribución de estilos de aprendizaje"""
        try:
            from app.models import CourseEnrollment
            
            # Obtener estudiantes del curso
            enrollments = CourseEnrollment.query.filter_by(
                course_id=course_id,
                is_active=True
            ).all()
            
            style_distribution = {'V': 0, 'A': 0, 'R': 0, 'K': 0, 'Unknown': 0}
            
            for enrollment in enrollments:
                student = enrollment.student
                if student.dominant_learning_style:
                    style_distribution[student.dominant_learning_style] += 1
                else:
                    style_distribution['Unknown'] += 1
            
            total_students = len(enrollments)
            if total_students > 0:
                for style in style_distribution:
                    style_distribution[style] = round(
                        (style_distribution[style] / total_students) * 100, 2
                    )
            
            return style_distribution
            
        except Exception as e:
            print(f"Error obteniendo distribución de estilos: {e}")
            return {}
    
    def _get_performance_trends(self, course_id):
        """Obtener tendencias de rendimiento"""
        try:
            # Obtener progreso de los últimos 30 días
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            progress_records = Progress.query.join(Progress.enrollment).filter(
                CourseEnrollment.course_id == course_id,
                Progress.created_at >= thirty_days_ago
            ).order_by(Progress.created_at).all()
            
            # Agrupar por día
            daily_performance = {}
            for record in progress_records:
                date_key = record.created_at.date().isoformat()
                if date_key not in daily_performance:
                    daily_performance[date_key] = []
                daily_performance[date_key].append(record.percentage)
            
            # Calcular promedio diario
            trends = []
            for date, percentages in daily_performance.items():
                avg_percentage = sum(percentages) / len(percentages)
                trends.append({
                    'date': date,
                    'avg_percentage': round(avg_percentage, 2),
                    'activity_count': len(percentages)
                })
            
            return trends
            
        except Exception as e:
            print(f"Error obteniendo tendencias de rendimiento: {e}")
            return []
    
    def _get_engagement_metrics(self, course_id):
        """Obtener métricas de engagement"""
        try:
            from app.models import CourseEnrollment
            
            # Obtener estudiantes activos
            active_enrollments = CourseEnrollment.query.filter_by(
                course_id=course_id,
                is_active=True
            ).all()
            
            if not active_enrollments:
                return {}
            
            engagement_data = []
            for enrollment in active_enrollments:
                student = enrollment.student
                
                # Obtener analíticas del estudiante
                analytics = LearningAnalytics.query.filter_by(
                    student_id=student.id
                ).order_by(desc(LearningAnalytics.created_at)).first()
                
                if analytics:
                    engagement_data.append({
                        'student_id': student.id,
                        'student_name': student.user.get_full_name(),
                        'engagement_score': analytics.engagement_score,
                        'session_duration': analytics.session_duration,
                        'questions_attempted': analytics.questions_attempted,
                        'accuracy_rate': analytics.accuracy_rate
                    })
            
            # Calcular métricas agregadas
            if engagement_data:
                avg_engagement = sum(d['engagement_score'] for d in engagement_data) / len(engagement_data)
                avg_session_duration = sum(d['session_duration'] for d in engagement_data if d['session_duration']) / len(engagement_data)
                avg_accuracy = sum(d['accuracy_rate'] for d in engagement_data if d['accuracy_rate']) / len(engagement_data)
            else:
                avg_engagement = avg_session_duration = avg_accuracy = 0
            
            return {
                'avg_engagement_score': round(avg_engagement, 2),
                'avg_session_duration': round(avg_session_duration, 2),
                'avg_accuracy_rate': round(avg_accuracy, 2),
                'student_engagement': engagement_data
            }
            
        except Exception as e:
            print(f"Error obteniendo métricas de engagement: {e}")
            return {}
    
    def get_student_analytics(self, student_id):
        """
        Obtener analíticas de un estudiante específico
        
        Args:
            student_id (int): ID del estudiante
            
        Returns:
            dict: Analíticas del estudiante
        """
        try:
            student = Student.query.get(student_id)
            if not student:
                return {}
            
            analytics = {
                'student_info': {
                    'id': student.id,
                    'name': student.user.get_full_name(),
                    'student_id': student.student_id,
                    'grade_level': student.grade_level
                },
                'vark_profile': student.get_vark_profile(),
                'diagnostic_summary': self._get_student_diagnostic_summary(student_id),
                'learning_paths': self._get_student_learning_paths(student_id),
                'progress_summary': self._get_student_progress_summary(student_id),
                'performance_trends': self._get_student_performance_trends(student_id),
                'engagement_metrics': self._get_student_engagement_metrics(student_id)
            }
            
            return analytics
            
        except Exception as e:
            print(f"Error obteniendo analíticas del estudiante: {e}")
            return {}
    
    def _get_student_diagnostic_summary(self, student_id):
        """Obtener resumen de diagnósticos del estudiante"""
        try:
            diagnostics = DiagnosticExam.query.filter_by(
                student_id=student_id,
                is_completed=True
            ).all()
            
            if not diagnostics:
                return {}
            
            avg_score = sum(d.percentage for d in diagnostics) / len(diagnostics)
            
            return {
                'total_diagnostics': len(diagnostics),
                'avg_score': round(avg_score, 2),
                'latest_score': round(diagnostics[-1].percentage, 2) if diagnostics else 0
            }
            
        except Exception as e:
            print(f"Error obteniendo resumen de diagnósticos: {e}")
            return {}
    
    def _get_student_learning_paths(self, student_id):
        """Obtener rutas de aprendizaje del estudiante"""
        try:
            paths = LearningPath.query.filter_by(student_id=student_id).all()
            
            return {
                'total_paths': len(paths),
                'active_paths': len([p for p in paths if p.is_active]),
                'completed_paths': len([p for p in paths if p.is_completed]),
                'avg_progress': round(sum(p.completion_percentage for p in paths) / len(paths), 2) if paths else 0
            }
            
        except Exception as e:
            print(f"Error obteniendo rutas de aprendizaje: {e}")
            return {}
    
    def _get_student_progress_summary(self, student_id):
        """Obtener resumen de progreso del estudiante"""
        try:
            progress_records = Progress.query.filter_by(student_id=student_id).all()
            
            if not progress_records:
                return {}
            
            avg_percentage = sum(p.percentage for p in progress_records) / len(progress_records)
            
            return {
                'total_activities': len(progress_records),
                'avg_percentage': round(avg_percentage, 2),
                'latest_activity': progress_records[-1].created_at.isoformat() if progress_records else None
            }
            
        except Exception as e:
            print(f"Error obteniendo resumen de progreso: {e}")
            return {}
    
    def _get_student_performance_trends(self, student_id):
        """Obtener tendencias de rendimiento del estudiante"""
        try:
            # Similar a _get_performance_trends pero para un estudiante específico
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            progress_records = Progress.query.filter(
                Progress.student_id == student_id,
                Progress.created_at >= thirty_days_ago
            ).order_by(Progress.created_at).all()
            
            # Implementación similar a _get_performance_trends
            daily_performance = {}
            for record in progress_records:
                date_key = record.created_at.date().isoformat()
                if date_key not in daily_performance:
                    daily_performance[date_key] = []
                daily_performance[date_key].append(record.percentage)
            
            trends = []
            for date, percentages in daily_performance.items():
                avg_percentage = sum(percentages) / len(percentages)
                trends.append({
                    'date': date,
                    'avg_percentage': round(avg_percentage, 2),
                    'activity_count': len(percentages)
                })
            
            return trends
            
        except Exception as e:
            print(f"Error obteniendo tendencias de rendimiento: {e}")
            return []
    
    def _get_student_engagement_metrics(self, student_id):
        """Obtener métricas de engagement del estudiante"""
        try:
            analytics = LearningAnalytics.query.filter_by(
                student_id=student_id
            ).order_by(desc(LearningAnalytics.created_at)).first()
            
            if not analytics:
                return {}
            
            return {
                'engagement_score': analytics.engagement_score,
                'session_duration': analytics.session_duration,
                'questions_attempted': analytics.questions_attempted,
                'accuracy_rate': analytics.accuracy_rate,
                'preferred_time': analytics.preferred_time_of_day,
                'preferred_difficulty': analytics.preferred_difficulty
            }
            
        except Exception as e:
            print(f"Error obteniendo métricas de engagement: {e}")
            return {}
