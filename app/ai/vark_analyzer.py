"""
Analizador de estilos de aprendizaje VARK
"""

from app.models import VARKQuestion, VARKResponse, Student
from app import db
import numpy as np

class VARKAnalyzer:
    """Analizador para el cuestionario VARK (Visual, Auditory, Reading/Writing, Kinesthetic)"""
    
    def __init__(self):
        self.vark_weights = {
            'V': {'visual': 1.0, 'auditory': 0.0, 'reading': 0.0, 'kinesthetic': 0.0},
            'A': {'visual': 0.0, 'auditory': 1.0, 'reading': 0.0, 'kinesthetic': 0.0},
            'R': {'visual': 0.0, 'auditory': 0.0, 'reading': 1.0, 'kinesthetic': 0.0},
            'K': {'visual': 0.0, 'auditory': 0.0, 'reading': 0.0, 'kinesthetic': 1.0}
        }
    
    def analyze_responses(self, responses):
        """
        Analizar respuestas del cuestionario VARK
        
        Args:
            responses (dict): Diccionario con question_id como clave y respuesta como valor
            
        Returns:
            dict: Puntajes VARK normalizados
        """
        try:
            # Inicializar contadores
            vark_scores = {'visual': 0.0, 'auditory': 0.0, 'reading': 0.0, 'kinesthetic': 0.0}
            total_questions = len(responses)
            
            if total_questions == 0:
                return vark_scores
            
            # Procesar cada respuesta
            for question_id, response in responses.items():
                if response in self.vark_weights:
                    weights = self.vark_weights[response]
                    for style, weight in weights.items():
                        vark_scores[style] += weight
            
            # Normalizar puntajes (convertir a porcentajes)
            for style in vark_scores:
                vark_scores[style] = (vark_scores[style] / total_questions) * 100
            
            return vark_scores
            
        except Exception as e:
            print(f"Error analizando respuestas VARK: {e}")
            return {'visual': 25.0, 'auditory': 25.0, 'reading': 25.0, 'kinesthetic': 25.0}
    
    def get_dominant_style(self, vark_scores):
        """
        Determinar el estilo de aprendizaje dominante
        
        Args:
            vark_scores (dict): Puntajes VARK
            
        Returns:
            str: Estilo dominante (V, A, R, K)
        """
        if not vark_scores:
            return 'V'  # Default a Visual
        
        # Mapear nombres a letras
        style_mapping = {
            'visual': 'V',
            'auditory': 'A', 
            'reading': 'R',
            'kinesthetic': 'K'
        }
        
        dominant_style = max(vark_scores, key=vark_scores.get)
        return style_mapping.get(dominant_style, 'V')
    
    def get_learning_style_profile(self, student_id):
        """
        Obtener perfil completo de estilo de aprendizaje de un estudiante
        
        Args:
            student_id (int): ID del estudiante
            
        Returns:
            dict: Perfil completo VARK
        """
        try:
            student = Student.query.get(student_id)
            if not student:
                return None
            
            # Obtener respuestas VARK del estudiante
            vark_responses = VARKResponse.query.filter_by(student_id=student_id).all()
            
            if not vark_responses:
                return None
            
            # Convertir respuestas a formato para análisis
            responses = {}
            for response in vark_responses:
                responses[response.question_id] = response.selected_option
            
            # Analizar respuestas
            vark_scores = self.analyze_responses(responses)
            dominant_style = self.get_dominant_style(vark_scores)
            
            # Calcular fortalezas y debilidades
            strengths = self._identify_strengths(vark_scores)
            weaknesses = self._identify_weaknesses(vark_scores)
            
            return {
                'scores': vark_scores,
                'dominant_style': dominant_style,
                'strengths': strengths,
                'weaknesses': weaknesses,
                'learning_preferences': self._get_learning_preferences(dominant_style),
                'recommended_resources': self._get_recommended_resource_types(dominant_style)
            }
            
        except Exception as e:
            print(f"Error obteniendo perfil VARK: {e}")
            return None
    
    def _identify_strengths(self, vark_scores):
        """Identificar fortalezas del estudiante"""
        strengths = []
        for style, score in vark_scores.items():
            if score >= 30:  # Umbral para considerar fortaleza
                strengths.append(style)
        return strengths
    
    def _identify_weaknesses(self, vark_scores):
        """Identificar debilidades del estudiante"""
        weaknesses = []
        for style, score in vark_scores.items():
            if score <= 20:  # Umbral para considerar debilidad
                weaknesses.append(style)
        return weaknesses
    
    def _get_learning_preferences(self, dominant_style):
        """Obtener preferencias de aprendizaje basadas en el estilo dominante"""
        preferences = {
            'V': {
                'description': 'Aprendizaje Visual',
                'preferences': [
                    'Diagramas y gráficos',
                    'Videos educativos',
                    'Mapas conceptuales',
                    'Presentaciones visuales',
                    'Infografías'
                ],
                'study_tips': [
                    'Usa colores para organizar información',
                    'Crea mapas mentales',
                    'Visualiza conceptos abstractos',
                    'Usa diagramas de flujo'
                ]
            },
            'A': {
                'description': 'Aprendizaje Auditivo',
                'preferences': [
                    'Lecturas en voz alta',
                    'Discusiones grupales',
                    'Podcasts educativos',
                    'Música de fondo',
                    'Explicaciones verbales'
                ],
                'study_tips': [
                    'Lee en voz alta',
                    'Participa en discusiones',
                    'Usa grabaciones de audio',
                    'Explica conceptos a otros'
                ]
            },
            'R': {
                'description': 'Aprendizaje por Lectura/Escritura',
                'preferences': [
                    'Textos y lecturas',
                    'Tomar notas detalladas',
                    'Listas y esquemas',
                    'Ejercicios escritos',
                    'Resúmenes'
                ],
                'study_tips': [
                    'Toma notas detalladas',
                    'Haz resúmenes',
                    'Usa listas y esquemas',
                    'Escribe explicaciones propias'
                ]
            },
            'K': {
                'description': 'Aprendizaje Kinestésico',
                'preferences': [
                    'Actividades prácticas',
                    'Simulaciones',
                    'Experimentos',
                    'Juegos educativos',
                    'Manipulación de objetos'
                ],
                'study_tips': [
                    'Haz actividades prácticas',
                    'Usa simulaciones',
                    'Toma descansos frecuentes',
                    'Aprende haciendo'
                ]
            }
        }
        
        return preferences.get(dominant_style, preferences['V'])
    
    def _get_recommended_resource_types(self, dominant_style):
        """Obtener tipos de recursos recomendados"""
        resource_mapping = {
            'V': ['video', 'simulation', 'game'],
            'A': ['video', 'reading'],
            'R': ['reading', 'exercise'],
            'K': ['simulation', 'game', 'exercise']
        }
        
        return resource_mapping.get(dominant_style, ['reading', 'video'])
    
    def update_student_vark_profile(self, student_id, vark_scores):
        """
        Actualizar perfil VARK del estudiante en la base de datos
        
        Args:
            student_id (int): ID del estudiante
            vark_scores (dict): Puntajes VARK
        """
        try:
            student = Student.query.get(student_id)
            if not student:
                return False
            
            # Actualizar puntajes VARK
            student.vark_visual = vark_scores.get('visual', 0.0)
            student.vark_auditory = vark_scores.get('auditory', 0.0)
            student.vark_reading = vark_scores.get('reading', 0.0)
            student.vark_kinesthetic = vark_scores.get('kinesthetic', 0.0)
            
            # Determinar estilo dominante
            student.dominant_learning_style = self.get_dominant_style(vark_scores)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error actualizando perfil VARK: {e}")
            db.session.rollback()
            return False
    
    def get_learning_style_compatibility(self, student_id, resource_type):
        """
        Calcular compatibilidad entre el estilo de aprendizaje del estudiante y un tipo de recurso
        
        Args:
            student_id (int): ID del estudiante
            resource_type (str): Tipo de recurso
            
        Returns:
            float: Puntuación de compatibilidad (0.0 a 1.0)
        """
        try:
            student = Student.query.get(student_id)
            if not student:
                return 0.5  # Compatibilidad neutral
            
            # Mapeo de tipos de recursos a estilos de aprendizaje
            resource_style_mapping = {
                'video': {'visual': 0.8, 'auditory': 0.7, 'reading': 0.3, 'kinesthetic': 0.4},
                'reading': {'visual': 0.4, 'auditory': 0.2, 'reading': 0.9, 'kinesthetic': 0.3},
                'exercise': {'visual': 0.5, 'auditory': 0.3, 'reading': 0.6, 'kinesthetic': 0.8},
                'simulation': {'visual': 0.7, 'auditory': 0.4, 'reading': 0.4, 'kinesthetic': 0.9},
                'game': {'visual': 0.6, 'auditory': 0.5, 'reading': 0.3, 'kinesthetic': 0.8}
            }
            
            # Obtener puntajes VARK del estudiante
            student_vark = {
                'visual': student.vark_visual / 100.0,
                'auditory': student.vark_auditory / 100.0,
                'reading': student.vark_reading / 100.0,
                'kinesthetic': student.vark_kinesthetic / 100.0
            }
            
            # Obtener compatibilidad del tipo de recurso
            resource_compatibility = resource_style_mapping.get(resource_type, {
                'visual': 0.5, 'auditory': 0.5, 'reading': 0.5, 'kinesthetic': 0.5
            })
            
            # Calcular compatibilidad ponderada
            compatibility = 0.0
            for style in ['visual', 'auditory', 'reading', 'kinesthetic']:
                compatibility += student_vark[style] * resource_compatibility[style]
            
            return min(1.0, max(0.0, compatibility))
            
        except Exception as e:
            print(f"Error calculando compatibilidad: {e}")
            return 0.5
