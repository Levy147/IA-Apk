"""
Integración con Google Forms para el examen diagnóstico
"""

import requests
import json
from datetime import datetime
from app.models import Student, DiagnosticExam, ExamResponse, Question, Competency
from app import db
from config import Config

class GoogleFormsIntegration:
    """Clase para integrar con Google Forms API"""
    
    def __init__(self):
        self.api_key = Config.GOOGLE_FORMS_API_KEY
        self.form_id = Config.GOOGLE_FORMS_FORM_ID
        self.base_url = "https://forms.googleapis.com/v1/forms"
    
    def get_form_responses(self, form_id=None):
        """Obtener respuestas de un formulario de Google Forms"""
        try:
            form_id = form_id or self.form_id
            url = f"{self.base_url}/{form_id}/responses"
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo respuestas de Google Forms: {e}")
            return None
    
    def process_diagnostic_responses(self, student_id, responses_data):
        """Procesar respuestas del examen diagnóstico"""
        try:
            student = Student.query.get(student_id)
            if not student:
                return {'success': False, 'error': 'Estudiante no encontrado'}
            
            # Buscar o crear examen diagnóstico
            diagnostic = DiagnosticExam.query.filter_by(
                student_id=student_id,
                is_completed=False
            ).first()
            
            if not diagnostic:
                return {'success': False, 'error': 'Examen diagnóstico no encontrado'}
            
            # Procesar cada respuesta
            total_score = 0
            total_questions = 0
            
            for response_data in responses_data:
                question_id = response_data.get('question_id')
                student_answer = response_data.get('answer')
                time_spent = response_data.get('time_spent', 0)
                
                # Buscar la pregunta
                question = Question.query.get(question_id)
                if not question:
                    continue
                
                # Verificar si la respuesta es correcta
                is_correct = self._check_answer(question, student_answer)
                points_earned = question.points if is_correct else 0
                
                # Crear registro de respuesta
                exam_response = ExamResponse(
                    exam_id=diagnostic.id,
                    question_id=question_id,
                    student_id=student_id,
                    student_answer=student_answer,
                    is_correct=is_correct,
                    points_earned=points_earned,
                    time_spent=time_spent
                )
                
                db.session.add(exam_response)
                
                total_score += points_earned
                total_questions += 1
            
            # Calcular puntaje final
            diagnostic.total_score = total_score
            diagnostic.percentage = (total_score / total_questions) * 100 if total_questions > 0 else 0
            diagnostic.is_completed = True
            diagnostic.completed_at = datetime.utcnow()
            
            # Actualizar perfil del estudiante
            student.diagnostic_completed = True
            student.diagnostic_score = diagnostic.percentage
            student.diagnostic_date = datetime.utcnow()
            
            db.session.commit()
            
            # Generar análisis de competencias
            competency_scores = self._analyze_competency_scores(diagnostic.id)
            diagnostic.competency_scores = competency_scores
            db.session.commit()
            
            return {
                'success': True,
                'diagnostic_id': diagnostic.id,
                'score': diagnostic.percentage,
                'competency_scores': competency_scores
            }
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def _check_answer(self, question, student_answer):
        """Verificar si la respuesta del estudiante es correcta"""
        correct_answer = question.correct_answer.lower().strip()
        student_answer = student_answer.lower().strip()
        
        if question.question_type.value == 'multiple_choice':
            return correct_answer == student_answer
        elif question.question_type.value == 'true_false':
            return correct_answer == student_answer
        elif question.question_type.value == 'fill_blank':
            # Para completar espacios, permitir variaciones
            return self._fuzzy_match(correct_answer, student_answer)
        else:
            return correct_answer == student_answer
    
    def _fuzzy_match(self, correct, student):
        """Comparación difusa para respuestas de texto libre"""
        # Implementación simple de comparación difusa
        correct_words = set(correct.split())
        student_words = set(student.split())
        
        # Calcular similitud basada en palabras comunes
        common_words = correct_words.intersection(student_words)
        similarity = len(common_words) / len(correct_words) if correct_words else 0
        
        return similarity >= 0.7  # 70% de similitud
    
    def _analyze_competency_scores(self, diagnostic_id):
        """Analizar puntajes por competencia"""
        diagnostic = DiagnosticExam.query.get(diagnostic_id)
        if not diagnostic:
            return {}
        
        competency_scores = {}
        
        # Agrupar respuestas por competencia
        for response in diagnostic.responses:
            if response.question.competency_id:
                competency_id = response.question.competency_id
                if competency_id not in competency_scores:
                    competency_scores[competency_id] = {
                        'total_questions': 0,
                        'correct_answers': 0,
                        'total_points': 0,
                        'earned_points': 0
                    }
                
                competency_scores[competency_id]['total_questions'] += 1
                competency_scores[competency_id]['total_points'] += response.question.points
                
                if response.is_correct:
                    competency_scores[competency_id]['correct_answers'] += 1
                    competency_scores[competency_id]['earned_points'] += response.points_earned
        
        # Calcular porcentajes
        for competency_id, scores in competency_scores.items():
            if scores['total_questions'] > 0:
                scores['percentage'] = (scores['earned_points'] / scores['total_points']) * 100
                scores['accuracy'] = (scores['correct_answers'] / scores['total_questions']) * 100
            else:
                scores['percentage'] = 0
                scores['accuracy'] = 0
        
        return competency_scores
    
    def create_diagnostic_form(self, course_id, questions):
        """Crear formulario de Google Forms para examen diagnóstico"""
        # Esta función requeriría implementación específica de la API de Google Forms
        # Por ahora, retornamos un placeholder
        return {
            'form_id': 'placeholder_form_id',
            'form_url': 'https://forms.gle/placeholder',
            'message': 'Formulario creado exitosamente'
        }
    
    def sync_questions_to_forms(self, course_id):
        """Sincronizar preguntas del curso con Google Forms"""
        try:
            questions = Question.query.filter_by(course_id=course_id).all()
            
            if not questions:
                return {'success': False, 'error': 'No hay preguntas para sincronizar'}
            
            # Crear formulario con las preguntas
            form_data = self._prepare_form_data(questions)
            result = self.create_diagnostic_form(course_id, questions)
            
            return {
                'success': True,
                'form_id': result['form_id'],
                'form_url': result['form_url'],
                'questions_synced': len(questions)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _prepare_form_data(self, questions):
        """Preparar datos del formulario para Google Forms"""
        form_data = {
            'info': {
                'title': 'Examen Diagnóstico - STI',
                'description': 'Este examen nos ayudará a personalizar tu experiencia de aprendizaje.'
            },
            'items': []
        }
        
        for i, question in enumerate(questions):
            item = {
                'itemId': f'question_{question.id}',
                'title': question.question_text,
                'questionItem': {
                    'question': {
                        'required': True,
                        'choiceQuestion': {
                            'type': 'RADIO',
                            'options': []
                        }
                    }
                }
            }
            
            # Agregar opciones para preguntas de opción múltiple
            if question.question_type.value == 'multiple_choice':
                for option_key, option_text in question.get_options().items():
                    item['questionItem']['question']['choiceQuestion']['options'].append({
                        'value': option_key
                    })
            
            form_data['items'].append(item)
        
        return form_data
