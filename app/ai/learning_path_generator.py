"""
Generador de rutas de aprendizaje personalizadas
"""

from app.models import Student, Course, LearningPath, LearningPathStep, Resource, Competency, CompetencyMastery
from app import db
from app.ai.vark_analyzer import VARKAnalyzer
from datetime import datetime
import random

class LearningPathGenerator:
    """Generador de rutas de aprendizaje personalizadas basado en IA"""
    
    def __init__(self):
        self.vark_analyzer = VARKAnalyzer()
    
    def generate_path(self, student_id, course_id):
        """
        Generar ruta de aprendizaje personalizada para un estudiante
        
        Args:
            student_id (int): ID del estudiante
            course_id (int): ID del curso
            
        Returns:
            LearningPath: Ruta de aprendizaje generada
        """
        try:
            student = Student.query.get(student_id)
            course = Course.query.get(course_id)
            
            if not student or not course:
                return None
            
            # Verificar si ya existe una ruta activa
            existing_path = LearningPath.query.filter_by(
                student_id=student_id,
                course_id=course_id,
                is_active=True
            ).first()
            
            if existing_path:
                return existing_path
            
            # Obtener perfil del estudiante
            vark_profile = student.get_vark_profile()
            diagnostic_scores = self._get_diagnostic_scores(student_id, course_id)
            
            # Generar secuencia de competencias
            competency_sequence = self._generate_competency_sequence(course_id, diagnostic_scores)
            
            # Crear ruta de aprendizaje
            learning_path = LearningPath(
                student_id=student_id,
                course_id=course_id,
                title=f"Ruta Personalizada - {course.name}",
                description=f"Ruta de aprendizaje adaptada para {student.user.get_full_name()}",
                learning_style=student.dominant_learning_style,
                total_steps=0,
                current_step=0
            )
            
            db.session.add(learning_path)
            db.session.flush()  # Para obtener el ID
            
            # Generar pasos de la ruta
            steps = self._generate_learning_steps(
                learning_path.id, 
                competency_sequence, 
                vark_profile
            )
            
            learning_path.total_steps = len(steps)
            learning_path.started_at = datetime.utcnow()
            
            db.session.commit()
            
            return learning_path
            
        except Exception as e:
            print(f"Error generando ruta de aprendizaje: {e}")
            db.session.rollback()
            return None
    
    def _get_diagnostic_scores(self, student_id, course_id):
        """Obtener puntajes del examen diagnóstico por competencia"""
        try:
            from app.models import DiagnosticExam
            
            diagnostic = DiagnosticExam.query.filter_by(
                student_id=student_id,
                course_id=course_id,
                is_completed=True
            ).first()
            
            if diagnostic and diagnostic.competency_scores:
                return diagnostic.competency_scores
            else:
                # Si no hay diagnóstico, asumir puntajes bajos
                competencies = Competency.query.filter_by(course_id=course_id).all()
                return {comp.id: {'percentage': 20.0} for comp in competencies}
                
        except Exception as e:
            print(f"Error obteniendo puntajes diagnósticos: {e}")
            return {}
    
    def _generate_competency_sequence(self, course_id, diagnostic_scores):
        """Generar secuencia de competencias basada en puntajes diagnósticos"""
        try:
            competencies = Competency.query.filter_by(course_id=course_id).all()
            
            if not competencies:
                return []
            
            # Ordenar competencias por puntaje diagnóstico (menor a mayor)
            competency_scores = []
            for comp in competencies:
                score = diagnostic_scores.get(comp.id, {}).get('percentage', 0.0)
                competency_scores.append((comp, score))
            
            # Ordenar por puntaje (las que necesitan más trabajo primero)
            competency_scores.sort(key=lambda x: x[1])
            
            # Aplicar lógica de prerequisitos
            ordered_competencies = self._apply_prerequisites(competency_scores)
            
            return ordered_competencies
            
        except Exception as e:
            print(f"Error generando secuencia de competencias: {e}")
            return []
    
    def _apply_prerequisites(self, competency_scores):
        """Aplicar lógica de prerequisitos a la secuencia de competencias"""
        try:
            ordered = []
            remaining = competency_scores.copy()
            
            while remaining:
                # Buscar competencias sin prerequisitos o con prerequisitos ya incluidos
                for comp, score in remaining[:]:
                    if self._can_add_competency(comp, ordered):
                        ordered.append((comp, score))
                        remaining.remove((comp, score))
                        break
                else:
                    # Si no se puede agregar ninguna, agregar la primera restante
                    if remaining:
                        comp, score = remaining.pop(0)
                        ordered.append((comp, score))
            
            return ordered
            
        except Exception as e:
            print(f"Error aplicando prerequisitos: {e}")
            return competency_scores
    
    def _can_add_competency(self, competency, ordered_list):
        """Verificar si una competencia puede ser agregada a la secuencia"""
        if not competency.prerequisites:
            return True
        
        ordered_ids = [comp.id for comp, _ in ordered_list]
        return all(prereq_id in ordered_ids for prereq_id in competency.prerequisites)
    
    def _generate_learning_steps(self, learning_path_id, competency_sequence, vark_profile):
        """Generar pasos de aprendizaje para cada competencia"""
        try:
            steps = []
            step_order = 1
            
            for competency, diagnostic_score in competency_sequence:
                # Determinar número de pasos basado en el puntaje diagnóstico
                num_steps = self._calculate_steps_needed(diagnostic_score)
                
                # Obtener recursos apropiados para la competencia
                resources = self._get_appropriate_resources(
                    competency.id, 
                    vark_profile,
                    num_steps
                )
                
                # Crear pasos para cada recurso
                for i, resource in enumerate(resources):
                    step = LearningPathStep(
                        learning_path_id=learning_path_id,
                        resource_id=resource.id,
                        competency_id=competency.id,
                        step_order=step_order,
                        title=f"{competency.name} - Paso {i+1}",
                        description=f"Aprende {competency.name} usando {resource.title}",
                        estimated_time=resource.duration or 30,
                        points=resource.points or 1
                    )
                    
                    db.session.add(step)
                    steps.append(step)
                    step_order += 1
            
            return steps
            
        except Exception as e:
            print(f"Error generando pasos de aprendizaje: {e}")
            return []
    
    def _calculate_steps_needed(self, diagnostic_score):
        """Calcular número de pasos necesarios basado en el puntaje diagnóstico"""
        if diagnostic_score >= 80:
            return 1  # Solo repaso
        elif diagnostic_score >= 60:
            return 2  # Repaso y práctica
        elif diagnostic_score >= 40:
            return 3  # Aprendizaje básico
        else:
            return 4  # Aprendizaje completo
    
    def _get_appropriate_resources(self, competency_id, vark_profile, num_steps):
        """Obtener recursos apropiados para una competencia y estilo de aprendizaje"""
        try:
            # Obtener todos los recursos de la competencia
            all_resources = Resource.query.filter_by(
                competency_id=competency_id,
                is_active=True
            ).all()
            
            if not all_resources:
                return []
            
            # Calcular compatibilidad con el estilo de aprendizaje
            resource_scores = []
            for resource in all_resources:
                compatibility = self._calculate_resource_compatibility(
                    resource, 
                    vark_profile
                )
                resource_scores.append((resource, compatibility))
            
            # Ordenar por compatibilidad
            resource_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Seleccionar los mejores recursos
            selected_resources = []
            for resource, score in resource_scores[:num_steps]:
                selected_resources.append(resource)
            
            # Si no hay suficientes recursos, agregar recursos adicionales
            if len(selected_resources) < num_steps:
                remaining_resources = [r for r, _ in resource_scores[len(selected_resources):]]
                selected_resources.extend(remaining_resources[:num_steps - len(selected_resources)])
            
            return selected_resources
            
        except Exception as e:
            print(f"Error obteniendo recursos apropiados: {e}")
            return []
    
    def _calculate_resource_compatibility(self, resource, vark_profile):
        """Calcular compatibilidad entre un recurso y el perfil VARK del estudiante"""
        try:
            if not vark_profile or not resource:
                return 0.5
            
            # Obtener puntajes VARK del estudiante
            student_vark = {
                'visual': vark_profile.get('visual', 25.0) / 100.0,
                'auditory': vark_profile.get('auditory', 25.0) / 100.0,
                'reading': vark_profile.get('reading', 25.0) / 100.0,
                'kinesthetic': vark_profile.get('kinesthetic', 25.0) / 100.0
            }
            
            # Obtener puntajes del recurso
            resource_scores = resource.get_learning_style_scores()
            
            # Calcular compatibilidad ponderada
            compatibility = 0.0
            for style in ['visual', 'auditory', 'reading', 'kinesthetic']:
                compatibility += student_vark[style] * resource_scores[style]
            
            return min(1.0, max(0.0, compatibility))
            
        except Exception as e:
            print(f"Error calculando compatibilidad de recurso: {e}")
            return 0.5
    
    def adapt_path(self, learning_path_id, performance_data):
        """
        Adaptar ruta de aprendizaje basada en el rendimiento del estudiante
        
        Args:
            learning_path_id (int): ID de la ruta de aprendizaje
            performance_data (dict): Datos de rendimiento del estudiante
            
        Returns:
            bool: True si la adaptación fue exitosa
        """
        try:
            learning_path = LearningPath.query.get(learning_path_id)
            if not learning_path:
                return False
            
            # Analizar rendimiento
            if performance_data.get('struggling', False):
                # Si el estudiante está teniendo dificultades, agregar pasos de refuerzo
                self._add_reinforcement_steps(learning_path)
            elif performance_data.get('excelling', False):
                # Si el estudiante está sobresaliendo, agregar pasos de desafío
                self._add_challenge_steps(learning_path)
            
            # Actualizar progreso
            learning_path.update_progress()
            
            return True
            
        except Exception as e:
            print(f"Error adaptando ruta de aprendizaje: {e}")
            return False
    
    def _add_reinforcement_steps(self, learning_path):
        """Agregar pasos de refuerzo a la ruta de aprendizaje"""
        # Implementar lógica para agregar pasos de refuerzo
        pass
    
    def _add_challenge_steps(self, learning_path):
        """Agregar pasos de desafío a la ruta de aprendizaje"""
        # Implementar lógica para agregar pasos de desafío
        pass
