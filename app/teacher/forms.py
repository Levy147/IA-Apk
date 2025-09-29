"""
Formularios para docentes
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from app.models import Course

class CourseForm(FlaskForm):
    """Formulario para crear/editar curso"""
    name = StringField('Nombre del Curso', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Descripción', validators=[Length(max=500)])
    code = StringField('Código del Curso', validators=[DataRequired(), Length(min=3, max=20)])
    
    grade_level = SelectField('Nivel Educativo', 
        choices=[
            ('', 'Seleccionar...'),
            ('primaria', 'Primaria'),
            ('secundaria', 'Secundaria'),
            ('universidad', 'Universidad')
        ],
        validators=[DataRequired()])
    
    subject = StringField('Materia', validators=[DataRequired(), Length(max=50)])
    credits = IntegerField('Créditos', validators=[NumberRange(min=1, max=10)], default=1)
    
    # Configuración de diagnóstico
    diagnostic_required = BooleanField('Examen Diagnóstico Requerido', default=True)
    min_diagnostic_questions = IntegerField('Mínimo de Preguntas Diagnósticas', 
        validators=[NumberRange(min=10, max=50)], default=25)
    
    submit = SubmitField('Crear Curso')

class QuestionForm(FlaskForm):
    """Formulario para crear preguntas"""
    question_text = TextAreaField('Texto de la Pregunta', validators=[DataRequired()])
    question_type = SelectField('Tipo de Pregunta',
        choices=[
            ('multiple_choice', 'Opción Múltiple'),
            ('true_false', 'Verdadero/Falso'),
            ('fill_blank', 'Completar Espacios'),
            ('short_answer', 'Respuesta Corta')
        ],
        validators=[DataRequired()])
    
    difficulty = SelectField('Dificultad',
        choices=[
            ('easy', 'Fácil'),
            ('medium', 'Medio'),
            ('hard', 'Difícil')
        ],
        validators=[DataRequired()])
    
    # Opciones para opción múltiple
    option_a = StringField('Opción A', validators=[Length(max=500)])
    option_b = StringField('Opción B', validators=[Length(max=500)])
    option_c = StringField('Opción C', validators=[Length(max=500)])
    option_d = StringField('Opción D', validators=[Length(max=500)])
    
    correct_answer = StringField('Respuesta Correcta', validators=[DataRequired()])
    explanation = TextAreaField('Explicación', validators=[Length(max=1000)])
    points = IntegerField('Puntos', validators=[NumberRange(min=1, max=10)], default=1)
    
    submit = SubmitField('Crear Pregunta')
