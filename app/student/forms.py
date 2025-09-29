"""
Formularios para estudiantes
"""

from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class VARKForm(FlaskForm):
    """Formulario para el cuestionario VARK"""
    submit = SubmitField('Completar Cuestionario')

class DiagnosticResponseForm(FlaskForm):
    """Formulario para respuestas del examen diagnóstico"""
    question_id = HiddenField('Question ID', validators=[DataRequired()])
    answer = RadioField('Respuesta', choices=[], validators=[DataRequired()])
    submit = SubmitField('Siguiente Pregunta')
