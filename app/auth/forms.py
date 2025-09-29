"""
Formularios de autenticación
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User, Student, Teacher

class LoginForm(FlaskForm):
    """Formulario de inicio de sesión"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    """Formulario de registro"""
    # Información personal
    first_name = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[
        DataRequired(), 
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    password2 = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(), 
        EqualTo('password', message='Las contraseñas no coinciden')
    ])
    
    # Tipo de usuario
    user_type = SelectField('Tipo de Usuario', 
        choices=[('student', 'Estudiante'), ('teacher', 'Docente')],
        validators=[DataRequired()])
    
    # Campos específicos para estudiantes
    student_id = StringField('Carnet de Estudiante', validators=[Length(max=20)])
    grade_level = SelectField('Nivel Educativo', 
        choices=[
            ('', 'Seleccionar...'),
            ('primaria', 'Primaria'),
            ('secundaria', 'Secundaria'),
            ('universidad', 'Universidad')
        ])
    school = StringField('Institución Educativa', validators=[Length(max=100)])
    
    # Campos específicos para docentes
    teacher_id = StringField('Código de Docente', validators=[Length(max=20)])
    department = StringField('Departamento', validators=[Length(max=100)])
    specialization = StringField('Especialización', validators=[Length(max=100)])
    
    # Botón de envío
    submit = SubmitField('Registrarse')
    
    def validate_email(self, email):
        """Validar que el email no esté registrado"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('El email ya está registrado. Usa un email diferente.')
    
    def validate_student_id(self, student_id):
        """Validar carnet de estudiante si es estudiante"""
        if self.user_type.data == 'student':
            if not student_id.data:
                raise ValidationError('El carnet de estudiante es requerido.')
            student = Student.query.filter_by(student_id=student_id.data).first()
            if student:
                raise ValidationError('El carnet ya está registrado.')
    
    def validate_teacher_id(self, teacher_id):
        """Validar código de docente si es docente"""
        if self.user_type.data == 'teacher':
            if not teacher_id.data:
                raise ValidationError('El código de docente es requerido.')
            teacher = Teacher.query.filter_by(teacher_id=teacher_id.data).first()
            if teacher:
                raise ValidationError('El código de docente ya está registrado.')
