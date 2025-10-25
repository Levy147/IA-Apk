"""
Integración específica con el formulario VARK de Google Forms
"""

import requests
import json
from datetime import datetime
from app.models import Student, VARKResponse, VARKQuestion
from app import db
from config import Config
from app.ai.vark_analyzer import VARKAnalyzer

class VARKFormsIntegration:
    """Clase para integrar con el formulario VARK específico de Google Forms"""
    
    def __init__(self):
        self.form_id = Config.VARK_FORM_ID
        self.form_url = Config.VARK_FORM_URL
        self.api_key = Config.GOOGLE_FORMS_API_KEY
        self.base_url = "https://forms.googleapis.com/v1/forms"
        self.analyzer = VARKAnalyzer()
    
    def get_vark_form_url(self):
        """Obtener URL del formulario VARK"""
        return self.form_url
    
    def process_vark_responses_from_forms(self, student_id, responses_data):
        """
        Procesar respuestas del formulario VARK de Google Forms
        
        Args:
            student_id (int): ID del estudiante
            responses_data (dict): Datos de respuestas del formulario
            
        Returns:
            dict: Resultado del procesamiento
        """
        try:
            student = Student.query.get(student_id)
            if not student:
                return {'success': False, 'error': 'Estudiante no encontrado'}
            
            # Verificar si ya completó el cuestionario VARK
            if student.dominant_learning_style:
                return {'success': False, 'error': 'El estudiante ya completó el cuestionario VARK'}
            
            # Mapear respuestas del formulario a formato VARK
            vark_responses = self._map_forms_responses_to_vark(responses_data)
            
            if not vark_responses:
                return {'success': False, 'error': 'No se pudieron procesar las respuestas'}
            
            # Analizar respuestas VARK
            vark_scores = self.analyzer.analyze_responses(vark_responses)
            
            # Guardar respuestas en la base de datos
            for question_id, response in vark_responses.items():
                vark_response = VARKResponse(
                    student_id=student_id,
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
            
            return {
                'success': True,
                'vark_scores': vark_scores,
                'dominant_style': self.analyzer.get_dominant_style(vark_scores),
                'learning_preferences': self.analyzer._get_learning_preferences(
                    self.analyzer.get_dominant_style(vark_scores)
                )
            }
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def _map_forms_responses_to_vark(self, forms_data):
        """
        Mapear respuestas del formulario de Google Forms al formato VARK
        
        El formulario VARK tiene 16 preguntas con opciones:
        - V: Visual (diagramas, gráficos, imágenes)
        - A: Auditivo (explicaciones orales, audio)
        - R: Lectura/Escritura (textos, apuntes)
        - K: Kinestésico (práctica, ejercicios)
        """
        try:
            # Mapeo de las preguntas del formulario a respuestas VARK
            # Basado en el contenido del formulario proporcionado
            question_mapping = {
                # Pregunta 1: "Cuando me explican un tema de matemáticas, prefiero:"
                'entry.1': {
                    'Ver diagramas o ejemplos gráficos.': 'V',
                    'Escuchar la explicación del profesor.': 'A',
                    'Leer la teoría en el libro o apuntes.': 'R',
                    'Resolver ejercicios prácticos.': 'K'
                },
                # Pregunta 2: "Si me piden aprender a simplificar fracciones, prefiero:"
                'entry.2': {
                    'Ver un esquema paso a paso en imágenes.': 'V',
                    'Escuchar a alguien explicarlo en voz alta.': 'A',
                    'Leer la explicación en el cuaderno o guía.': 'R',
                    'Intentar resolver ejemplos por mi cuenta.': 'K'
                },
                # Pregunta 3: "Para aprender fórmulas, me ayuda más:"
                'entry.3': {
                    'Ver la fórmula en un gráfico o esquema.': 'V',
                    'Escuchar cómo se explica con ejemplos orales.': 'A',
                    'Leer y escribir varias veces la fórmula.': 'R',
                    'Usar la fórmula en muchos ejercicios prácticos.': 'K'
                },
                # Pregunta 4: "Cuando estudio operaciones básicas, prefiero:"
                'entry.4': {
                    'Usar colores o subrayar para diferenciar pasos.': 'V',
                    'Escuchar grabaciones de clases.': 'A',
                    'Hacer resúmenes y escribir las reglas.': 'R',
                    'Resolver problemas de aplicación.': 'K'
                },
                # Pregunta 5: "Para recordar definiciones, prefiero:"
                'entry.5': {
                    'Asociarlas con una imagen o gráfico.': 'V',
                    'Repetirlas en voz alta.': 'A',
                    'Leer y escribirlas varias veces.': 'R',
                    'Usarlas al resolver ejercicios.': 'K'
                },
                # Pregunta 6: "Si no entiendo un problema, busco:"
                'entry.6': {
                    'Ver la solución resuelta con dibujos.': 'V',
                    'Que alguien me lo explique verbalmente.': 'A',
                    'Leer el procedimiento en un texto.': 'R',
                    'Resolverlo manipulando números y probando.': 'K'
                },
                # Pregunta 7: "Para aprender geometría, prefiero:"
                'entry.7': {
                    'Ver figuras y esquemas.': 'V',
                    'Escuchar la explicación del maestro.': 'A',
                    'Leer las propiedades en el libro.': 'R',
                    'Usar instrumentos (regla, compás) para practicar.': 'K'
                },
                # Pregunta 8: "Cuando reviso álgebra, me sirve más:"
                'entry.8': {
                    'Mirar ejemplos con gráficos o diagramas.': 'V',
                    'Escuchar un audio con la explicación.': 'A',
                    'Leer paso a paso el procedimiento.': 'R',
                    'Resolver ejercicios prácticos en hojas.': 'K'
                },
                # Pregunta 9: "En un examen me siento más seguro si:"
                'entry.9': {
                    'Recuerdo los gráficos o colores usados al estudiar.': 'V',
                    'Recuerdo lo que el profesor explicó en clase.': 'A',
                    'Recuerdo lo que escribí en mis apuntes.': 'R',
                    'Recuerdo los ejercicios que practiqué.': 'K'
                },
                # Pregunta 10: "Para aprender porcentajes, prefiero:"
                'entry.10': {
                    'Ver diagramas circulares o barras.': 'V',
                    'Escuchar ejemplos prácticos explicados.': 'A',
                    'Leer la fórmula y ejemplos en el cuaderno.': 'R',
                    'Aplicar porcentajes en compras o descuentos.': 'K'
                },
                # Pregunta 11: "Cuando tengo que repasar, prefiero:"
                'entry.11': {
                    'Hacer mapas conceptuales o esquemas.': 'V',
                    'Explicarle en voz alta a un compañero.': 'A',
                    'Reescribir mis notas y resúmenes.': 'R',
                    'Hacer ejercicios prácticos.': 'K'
                },
                # Pregunta 12: "Para aprender a resolver ecuaciones, prefiero:"
                'entry.12': {
                    'Ver un procedimiento visual paso a paso.': 'V',
                    'Escuchar cómo alguien lo resuelve en voz alta.': 'A',
                    'Leer ejemplos resueltos en el libro.': 'R',
                    'Resolver varias ecuaciones yo mismo.': 'K'
                },
                # Pregunta 13: "Cuando me enseñan un tema nuevo, lo entiendo mejor si:"
                'entry.13': {
                    'Veo imágenes o gráficos del tema.': 'V',
                    'Escucho la explicación oralmente.': 'A',
                    'Leo el procedimiento escrito.': 'R',
                    'Lo practico con ejemplos.': 'K'
                },
                # Pregunta 14: "Para aprender probabilidad, prefiero:"
                'entry.14': {
                    'Ver tablas y gráficos de resultados.': 'V',
                    'Escuchar la explicación de ejemplos cotidianos.': 'A',
                    'Leer la definición y fórmulas.': 'R',
                    'Realizar experimentos como lanzar dados o monedas.': 'K'
                },
                # Pregunta 15: "Cuando estudio, me resulta más fácil:"
                'entry.15': {
                    'Recordar imágenes, colores o diagramas.': 'V',
                    'Recordar lo que escuché en clase.': 'A',
                    'Recordar lo que escribí o leí.': 'R',
                    'Recordar lo que hice en ejercicios prácticos.': 'K'
                }
            }
            
            vark_responses = {}
            
            # Procesar cada respuesta del formulario
            for entry_key, response_text in forms_data.items():
                if entry_key in question_mapping:
                    question_number = int(entry_key.split('.')[1])
                    vark_option = question_mapping[entry_key].get(response_text)
                    
                    if vark_option:
                        vark_responses[question_number] = vark_option
            
            return vark_responses
            
        except Exception as e:
            print(f"Error mapeando respuestas VARK: {e}")
            return {}
    
    def get_vark_form_embed_url(self):
        """Obtener URL para embeber el formulario VARK"""
        return f"{self.form_url}?embedded=true"
    
    def create_vark_completion_webhook(self, student_id):
        """
        Crear webhook para notificar cuando se complete el formulario VARK
        Esto requeriría configuración adicional en Google Forms
        """
        webhook_data = {
            'student_id': student_id,
            'form_id': self.form_id,
            'callback_url': f"/api/vark-completed/{student_id}",
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return webhook_data
    
    def sync_vark_questions_to_database(self):
        """
        Sincronizar las preguntas del formulario VARK con la base de datos
        """
        try:
            # Verificar si ya existen las preguntas VARK
            existing_questions = VARKQuestion.query.count()
            if existing_questions >= 15:  # El formulario tiene 15 preguntas
                return {'success': True, 'message': 'Las preguntas VARK ya están sincronizadas'}
            
            # Crear preguntas VARK basadas en el formulario
            vark_questions = [
                {
                    'question_number': 1,
                    'question_text': 'Cuando me explican un tema de matemáticas, prefiero:',
                    'options': {
                        'V': 'Ver diagramas o ejemplos gráficos.',
                        'A': 'Escuchar la explicación del profesor.',
                        'R': 'Leer la teoría en el libro o apuntes.',
                        'K': 'Resolver ejercicios prácticos.'
                    }
                },
                {
                    'question_number': 2,
                    'question_text': 'Si me piden aprender a simplificar fracciones, prefiero:',
                    'options': {
                        'V': 'Ver un esquema paso a paso en imágenes.',
                        'A': 'Escuchar a alguien explicarlo en voz alta.',
                        'R': 'Leer la explicación en el cuaderno o guía.',
                        'K': 'Intentar resolver ejemplos por mi cuenta.'
                    }
                },
                {
                    'question_number': 3,
                    'question_text': 'Para aprender fórmulas, me ayuda más:',
                    'options': {
                        'V': 'Ver la fórmula en un gráfico o esquema.',
                        'A': 'Escuchar cómo se explica con ejemplos orales.',
                        'R': 'Leer y escribir varias veces la fórmula.',
                        'K': 'Usar la fórmula en muchos ejercicios prácticos.'
                    }
                },
                {
                    'question_number': 4,
                    'question_text': 'Cuando estudio operaciones básicas, prefiero:',
                    'options': {
                        'V': 'Usar colores o subrayar para diferenciar pasos.',
                        'A': 'Escuchar grabaciones de clases.',
                        'R': 'Hacer resúmenes y escribir las reglas.',
                        'K': 'Resolver problemas de aplicación.'
                    }
                },
                {
                    'question_number': 5,
                    'question_text': 'Para recordar definiciones, prefiero:',
                    'options': {
                        'V': 'Asociarlas con una imagen o gráfico.',
                        'A': 'Repetirlas en voz alta.',
                        'R': 'Leer y escribirlas varias veces.',
                        'K': 'Usarlas al resolver ejercicios.'
                    }
                },
                {
                    'question_number': 6,
                    'question_text': 'Si no entiendo un problema, busco:',
                    'options': {
                        'V': 'Ver la solución resuelta con dibujos.',
                        'A': 'Que alguien me lo explique verbalmente.',
                        'R': 'Leer el procedimiento en un texto.',
                        'K': 'Resolverlo manipulando números y probando.'
                    }
                },
                {
                    'question_number': 7,
                    'question_text': 'Para aprender geometría, prefiero:',
                    'options': {
                        'V': 'Ver figuras y esquemas.',
                        'A': 'Escuchar la explicación del maestro.',
                        'R': 'Leer las propiedades en el libro.',
                        'K': 'Usar instrumentos (regla, compás) para practicar.'
                    }
                },
                {
                    'question_number': 8,
                    'question_text': 'Cuando reviso álgebra, me sirve más:',
                    'options': {
                        'V': 'Mirar ejemplos con gráficos o diagramas.',
                        'A': 'Escuchar un audio con la explicación.',
                        'R': 'Leer paso a paso el procedimiento.',
                        'K': 'Resolver ejercicios prácticos en hojas.'
                    }
                },
                {
                    'question_number': 9,
                    'question_text': 'En un examen me siento más seguro si:',
                    'options': {
                        'V': 'Recuerdo los gráficos o colores usados al estudiar.',
                        'A': 'Recuerdo lo que el profesor explicó en clase.',
                        'R': 'Recuerdo lo que escribí en mis apuntes.',
                        'K': 'Recuerdo los ejercicios que practiqué.'
                    }
                },
                {
                    'question_number': 10,
                    'question_text': 'Para aprender porcentajes, prefiero:',
                    'options': {
                        'V': 'Ver diagramas circulares o barras.',
                        'A': 'Escuchar ejemplos prácticos explicados.',
                        'R': 'Leer la fórmula y ejemplos en el cuaderno.',
                        'K': 'Aplicar porcentajes en compras o descuentos.'
                    }
                },
                {
                    'question_number': 11,
                    'question_text': 'Cuando tengo que repasar, prefiero:',
                    'options': {
                        'V': 'Hacer mapas conceptuales o esquemas.',
                        'A': 'Explicarle en voz alta a un compañero.',
                        'R': 'Reescribir mis notas y resúmenes.',
                        'K': 'Hacer ejercicios prácticos.'
                    }
                },
                {
                    'question_number': 12,
                    'question_text': 'Para aprender a resolver ecuaciones, prefiero:',
                    'options': {
                        'V': 'Ver un procedimiento visual paso a paso.',
                        'A': 'Escuchar cómo alguien lo resuelve en voz alta.',
                        'R': 'Leer ejemplos resueltos en el libro.',
                        'K': 'Resolver varias ecuaciones yo mismo.'
                    }
                },
                {
                    'question_number': 13,
                    'question_text': 'Cuando me enseñan un tema nuevo, lo entiendo mejor si:',
                    'options': {
                        'V': 'Veo imágenes o gráficos del tema.',
                        'A': 'Escucho la explicación oralmente.',
                        'R': 'Leo el procedimiento escrito.',
                        'K': 'Lo practico con ejemplos.'
                    }
                },
                {
                    'question_number': 14,
                    'question_text': 'Para aprender probabilidad, prefiero:',
                    'options': {
                        'V': 'Ver tablas y gráficos de resultados.',
                        'A': 'Escuchar la explicación de ejemplos cotidianos.',
                        'R': 'Leer la definición y fórmulas.',
                        'K': 'Realizar experimentos como lanzar dados o monedas.'
                    }
                },
                {
                    'question_number': 15,
                    'question_text': 'Cuando estudio, me resulta más fácil:',
                    'options': {
                        'V': 'Recordar imágenes, colores o diagramas.',
                        'A': 'Recordar lo que escuché en clase.',
                        'R': 'Recordar lo que escribí o leí.',
                        'K': 'Recordar lo que hice en ejercicios prácticos.'
                    }
                }
            ]
            
            # Crear preguntas en la base de datos
            for question_data in vark_questions:
                existing_question = VARKQuestion.query.filter_by(
                    question_number=question_data['question_number']
                ).first()
                
                if not existing_question:
                    vark_question = VARKQuestion(
                        question_number=question_data['question_number'],
                        question_text=question_data['question_text'],
                        option_v=question_data['options'].get('V', ''),
                        option_a=question_data['options'].get('A', ''),
                        option_r=question_data['options'].get('R', ''),
                        option_k=question_data['options'].get('K', '')
                    )
                    db.session.add(vark_question)
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f'Se sincronizaron {len(vark_questions)} preguntas VARK',
                'questions_created': len(vark_questions)
            }
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}

