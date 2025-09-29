"""
Modelos de evaluación y diagnóstico
"""

from datetime import datetime
import enum
from app import db

class QuestionType(enum.Enum):
    """Tipos de preguntas"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"
    SHORT_ANSWER = "short_answer"

class DifficultyLevel(enum.Enum):
    """Niveles de dificultad"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Question(db.Model):
    """Modelo de pregunta"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    competency_id = db.Column(db.Integer, db.ForeignKey('competencies.id'))
    
    # Contenido de la pregunta
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.Enum(QuestionType), nullable=False)
    difficulty = db.Column(db.Enum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    
    # Opciones para preguntas de opción múltiple
    option_a = db.Column(db.String(500))
    option_b = db.Column(db.String(500))
    option_c = db.Column(db.String(500))
    option_d = db.Column(db.String(500))
    
    # Respuesta correcta
    correct_answer = db.Column(db.String(500), nullable=False)
    explanation = db.Column(db.Text)  # Explicación de la respuesta
    
    # Metadatos
    points = db.Column(db.Integer, default=1)
    time_limit = db.Column(db.Integer)  # Tiempo límite en segundos
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    exam_responses = db.relationship('ExamResponse', backref='question', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:50]}...>'
    
    def get_options(self):
        """Obtener opciones de la pregunta"""
        if self.question_type == QuestionType.MULTIPLE_CHOICE:
            return {
                'A': self.option_a,
                'B': self.option_b,
                'C': self.option_c,
                'D': self.option_d
            }
        return {}

class DiagnosticExam(db.Model):
    """Examen diagnóstico"""
    __tablename__ = 'diagnostic_exams'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    
    # Configuración del examen
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    total_questions = db.Column(db.Integer, default=25)
    time_limit = db.Column(db.Integer)  # Tiempo límite en minutos
    
    # Estado del examen
    is_completed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Resultados
    total_score = db.Column(db.Float)
    percentage = db.Column(db.Float)
    competency_scores = db.Column(db.JSON)  # Puntajes por competencia
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    responses = db.relationship('ExamResponse', backref='exam', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<DiagnosticExam {self.id} for {self.student.student_id}>'
    
    def calculate_score(self):
        """Calcular puntaje del examen"""
        if not self.responses:
            return 0.0
        
        correct_answers = sum(1 for response in self.responses if response.is_correct)
        total_questions = len(self.responses)
        
        self.total_score = correct_answers
        self.percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Actualizar perfil del estudiante
        self.student.diagnostic_completed = True
        self.student.diagnostic_score = self.percentage
        self.student.diagnostic_date = datetime.utcnow()
        
        db.session.commit()
        return self.percentage

class ExamResponse(db.Model):
    """Respuesta del estudiante a una pregunta del examen"""
    __tablename__ = 'exam_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('diagnostic_exams.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    
    # Respuesta del estudiante
    student_answer = db.Column(db.String(500), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    points_earned = db.Column(db.Float, default=0.0)
    
    # Metadatos
    time_spent = db.Column(db.Integer)  # Tiempo en segundos
    attempts = db.Column(db.Integer, default=1)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExamResponse {self.id}: {"✓" if self.is_correct else "✗"}>'

# Modelos para el cuestionario VARK
class VARKQuestion(db.Model):
    """Preguntas del cuestionario VARK"""
    __tablename__ = 'vark_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    
    # Opciones VARK
    option_v = db.Column(db.String(500))  # Visual
    option_a = db.Column(db.String(500))  # Auditory
    option_r = db.Column(db.String(500))  # Reading/Writing
    option_k = db.Column(db.String(500))  # Kinesthetic
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    responses = db.relationship('VARKResponse', backref='vark_question', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<VARKQuestion {self.question_number}>'

class VARKResponse(db.Model):
    """Respuestas del estudiante al cuestionario VARK"""
    __tablename__ = 'vark_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('vark_questions.id'), nullable=False)
    
    # Respuesta seleccionada (V, A, R, K)
    selected_option = db.Column(db.String(1), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<VARKResponse {self.id}: {self.selected_option}>'
