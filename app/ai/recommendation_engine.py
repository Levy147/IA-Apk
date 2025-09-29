"""
Motor de recomendaciones para el STI
"""

from app.models import Student, LearningPath, Resource, Progress, LearningRecommendation
from app import db
from app.ai.vark_analyzer import VARKAnalyzer
from datetime import datetime, timedelta
import random

class RecommendationEngine:
    """Motor de recomendaciones basado en IA"""
    
    def __init__(self):
        self.vark_analyzer = VARKAnalyzer()
    
    def get_recommendations(self, student_id, limit=5):
        """
        Obtener recomendaciones personalizadas para un estudiante
        
        Args:
            student_id (int): ID del estudiante
            limit (int): Número máximo de recomendaciones
            
        Returns:
            list: Lista de recomendaciones
        """
        try:
            student = Student.query.get(student_id)
            if not student:
                return []
            
            recommendations = []
            
            # 1. Recomendaciones basadas en estilo de aprendizaje
            vark_recommendations = self._get_vark_based_recommendations(student_id)
            recommendations.extend(vark_recommendations)
            
            # 2. Recomendaciones basadas en progreso
            progress_recommendations = self._get_progress_based_recommendations(student_id)
            recommendations.extend(progress_recommendations)
            
            # 3. Recomendaciones basadas en dificultades
            difficulty_recommendations = self._get_difficulty_based_recommendations(student_id)
            recommendations.extend(difficulty_recommendations)
            
            # 4. Recomendaciones de recursos similares
            similar_recommendations = self._get_similar_resource_recommendations(student_id)
            recommendations.extend(similar_recommendations)
            
            # Ordenar por relevancia y prioridad
            recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # Limitar número de recomendaciones
            return recommendations[:limit]
            
        except Exception as e:
            print(f"Error obteniendo recomendaciones: {e}")
            return []
    
    def _get_vark_based_recommendations(self, student_id):
        """Obtener recomendaciones basadas en el estilo de aprendizaje VARK"""
        try:
            student = Student.query.get(student_id)
            if not student or not student.dominant_learning_style:
                return []
            
            vark_profile = student.get_vark_profile()
            dominant_style = student.dominant_learning_style
            
            recommendations = []
            
            # Buscar recursos que coincidan con el estilo dominante
            resources = Resource.query.filter_by(is_active=True).all()
            
            for resource in resources:
                compatibility = self.vark_analyzer.get_learning_style_compatibility(
                    student_id, 
                    resource.resource_type.value
                )
                
                if compatibility >= 0.7:  # Alta compatibilidad
                    recommendation = {
                        'type': 'resource',
                        'target_id': resource.id,
                        'title': f"Recurso recomendado: {resource.title}",
                        'description': f"Este recurso es ideal para tu estilo de aprendizaje {dominant_style}",
                        'reasoning': f"Compatibilidad del {compatibility*100:.0f}% con tu estilo de aprendizaje",
                        'confidence_score': compatibility,
                        'relevance_score': compatibility * 0.8,
                        'priority': 3
                    }
                    recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            print(f"Error obteniendo recomendaciones VARK: {e}")
            return []
    
    def _get_progress_based_recommendations(self, student_id):
        """Obtener recomendaciones basadas en el progreso del estudiante"""
        try:
            student = Student.query.get(student_id)
            if not student:
                return []
            
            recommendations = []
            
            # Obtener rutas de aprendizaje activas
            active_paths = LearningPath.query.filter_by(
                student_id=student_id,
                is_active=True
            ).all()
            
            for path in active_paths:
                # Si el progreso es bajo, recomendar recursos de refuerzo
                if path.completion_percentage < 30:
                    recommendation = {
                        'type': 'learning_path',
                        'target_id': path.id,
                        'title': "Refuerza tu aprendizaje",
                        'description': f"Tu progreso en {path.title} es del {path.completion_percentage:.0f}%. Te recomendamos recursos adicionales.",
                        'reasoning': "Progreso bajo detectado",
                        'confidence_score': 0.8,
                        'relevance_score': 0.9,
                        'priority': 4
                    }
                    recommendations.append(recommendation)
                
                # Si el progreso es alto, recomendar desafíos adicionales
                elif path.completion_percentage > 80:
                    recommendation = {
                        'type': 'challenge',
                        'target_id': path.id,
                        'title': "Desafío adicional",
                        'description': f"¡Excelente progreso en {path.title}! Te recomendamos desafíos adicionales.",
                        'reasoning': "Alto rendimiento detectado",
                        'confidence_score': 0.7,
                        'relevance_score': 0.6,
                        'priority': 2
                    }
                    recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            print(f"Error obteniendo recomendaciones de progreso: {e}")
            return []
    
    def _get_difficulty_based_recommendations(self, student_id):
        """Obtener recomendaciones basadas en dificultades detectadas"""
        try:
            student = Student.query.get(student_id)
            if not student:
                return []
            
            recommendations = []
            
            # Buscar registros de progreso con puntajes bajos
            low_performance = Progress.query.filter(
                Progress.student_id == student_id,
                Progress.percentage < 50
            ).order_by(Progress.created_at.desc()).limit(5).all()
            
            for progress in low_performance:
                if progress.competency_id:
                    competency = progress.competency
                    recommendation = {
                        'type': 'competency_support',
                        'target_id': competency.id,
                        'title': f"Refuerza {competency.name}",
                        'description': f"Detectamos dificultades en {competency.name}. Te recomendamos recursos adicionales.",
                        'reasoning': f"Puntaje bajo ({progress.percentage:.0f}%) en evaluación reciente",
                        'confidence_score': 0.9,
                        'relevance_score': 0.95,
                        'priority': 5
                    }
                    recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            print(f"Error obteniendo recomendaciones de dificultad: {e}")
            return []
    
    def _get_similar_resource_recommendations(self, student_id):
        """Obtener recomendaciones de recursos similares a los que le gustaron al estudiante"""
        try:
            student = Student.query.get(student_id)
            if not student:
                return []
            
            recommendations = []
            
            # Buscar recursos que el estudiante ha completado exitosamente
            successful_progress = Progress.query.filter(
                Progress.student_id == student_id,
                Progress.percentage >= 80,
                Progress.activity_type == 'learning'
            ).order_by(Progress.created_at.desc()).limit(3).all()
            
            for progress in successful_progress:
                # Buscar recursos similares
                similar_resources = self._find_similar_resources(progress.activity_id)
                
                for resource in similar_resources:
                    recommendation = {
                        'type': 'similar_resource',
                        'target_id': resource.id,
                        'title': f"Recurso similar: {resource.title}",
                        'description': f"Basado en tu éxito con recursos similares, te recomendamos este contenido.",
                        'reasoning': "Basado en recursos exitosos previos",
                        'confidence_score': 0.6,
                        'relevance_score': 0.7,
                        'priority': 2
                    }
                    recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            print(f"Error obteniendo recomendaciones similares: {e}")
            return []
    
    def _find_similar_resources(self, resource_id):
        """Encontrar recursos similares a uno dado"""
        try:
            # Implementación simple: buscar recursos de la misma competencia
            resource = Resource.query.get(resource_id)
            if not resource or not resource.competency_id:
                return []
            
            similar_resources = Resource.query.filter(
                Resource.competency_id == resource.competency_id,
                Resource.id != resource_id,
                Resource.is_active == True
            ).limit(3).all()
            
            return similar_resources
            
        except Exception as e:
            print(f"Error encontrando recursos similares: {e}")
            return []
    
    def save_recommendation(self, student_id, recommendation_data):
        """
        Guardar recomendación en la base de datos
        
        Args:
            student_id (int): ID del estudiante
            recommendation_data (dict): Datos de la recomendación
            
        Returns:
            LearningRecommendation: Recomendación guardada
        """
        try:
            recommendation = LearningRecommendation(
                student_id=student_id,
                course_id=recommendation_data.get('course_id'),
                recommendation_type=recommendation_data.get('type'),
                target_id=recommendation_data.get('target_id'),
                title=recommendation_data.get('title'),
                description=recommendation_data.get('description'),
                reasoning=recommendation_data.get('reasoning'),
                confidence_score=recommendation_data.get('confidence_score'),
                relevance_score=recommendation_data.get('relevance_score'),
                priority=recommendation_data.get('priority')
            )
            
            db.session.add(recommendation)
            db.session.commit()
            
            return recommendation
            
        except Exception as e:
            print(f"Error guardando recomendación: {e}")
            db.session.rollback()
            return None
    
    def update_recommendation_feedback(self, recommendation_id, feedback_score):
        """
        Actualizar retroalimentación de una recomendación
        
        Args:
            recommendation_id (int): ID de la recomendación
            feedback_score (int): Puntuación de retroalimentación (1-5)
            
        Returns:
            bool: True si la actualización fue exitosa
        """
        try:
            recommendation = LearningRecommendation.query.get(recommendation_id)
            if not recommendation:
                return False
            
            recommendation.provide_feedback(feedback_score)
            return True
            
        except Exception as e:
            print(f"Error actualizando retroalimentación: {e}")
            return False
