"""
Modelos de progreso y competencias
"""

from datetime import datetime
import enum
from app import db

class CompetencyLevel(enum.Enum):
    """Niveles de dominio de competencias"""
    NOVICE = "novice"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class Competency(db.Model):
    """Competencias curriculares"""
    __tablename__ = 'competencies'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    # Información de la competencia
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    code = db.Column(db.String(50), unique=True, nullable=False)
    
    # Configuración
    level = db.Column(db.Enum(CompetencyLevel), default=CompetencyLevel.BEGINNER)
    is_core = db.Column(db.Boolean, default=True)  # Competencia fundamental
    prerequisites = db.Column(db.JSON)  # IDs de competencias prerequisito
    
    # Metadatos
    weight = db.Column(db.Float, default=1.0)  # Peso en la evaluación
    estimated_hours = db.Column(db.Integer)  # Horas estimadas para dominar
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    questions = db.relationship('Question', backref='competency', cascade='all, delete-orphan')
    resources = db.relationship('Resource', backref='competency', cascade='all, delete-orphan')
    learning_steps = db.relationship('LearningPathStep', backref='competency', cascade='all, delete-orphan')
    mastery_records = db.relationship('CompetencyMastery', backref='competency', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Competency {self.code}: {self.name}>'

class CompetencyMastery(db.Model):
    """Dominio de competencias por estudiante"""
    __tablename__ = 'competency_mastery'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    competency_id = db.Column(db.Integer, db.ForeignKey('competencies.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    # Nivel de dominio
    mastery_level = db.Column(db.Float, default=0.0)  # 0.0 a 1.0
    confidence_level = db.Column(db.Float, default=0.0)  # 0.0 a 1.0
    
    # Estado
    is_mastered = db.Column(db.Boolean, default=False)
    mastery_threshold = db.Column(db.Float, default=0.7)  # Umbral para considerar dominio
    
    # Fechas
    first_attempt = db.Column(db.DateTime)
    last_attempt = db.Column(db.DateTime)
    mastered_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CompetencyMastery {self.student.student_id} - {self.competency.code}>'
    
    def update_mastery(self, new_level, confidence=None):
        """Actualizar nivel de dominio"""
        self.mastery_level = min(1.0, max(0.0, new_level))
        if confidence is not None:
            self.confidence_level = min(1.0, max(0.0, confidence))
        
        self.last_attempt = datetime.utcnow()
        
        # Verificar si se alcanzó el dominio
        if self.mastery_level >= self.mastery_threshold and not self.is_mastered:
            self.is_mastered = True
            self.mastered_at = datetime.utcnow()
        
        db.session.commit()
    
    def get_mastery_status(self):
        """Obtener estado de dominio"""
        if self.mastery_level >= self.mastery_threshold:
            return "mastered"
        elif self.mastery_level >= 0.5:
            return "developing"
        else:
            return "beginning"

class Progress(db.Model):
    """Registro de progreso del estudiante"""
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('course_enrollments.id'), nullable=False)
    
    # Información del progreso
    activity_type = db.Column(db.String(50), nullable=False)  # 'diagnostic', 'learning', 'assessment'
    activity_id = db.Column(db.Integer)  # ID de la actividad específica
    competency_id = db.Column(db.Integer, db.ForeignKey('competencies.id'))
    
    # Resultados
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    percentage = db.Column(db.Float)
    time_spent = db.Column(db.Integer)  # Tiempo en segundos
    
    # Metadatos
    notes = db.Column(db.Text)
    feedback = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    competency = db.relationship('Competency', backref='progress_records')
    
    def __repr__(self):
        return f'<Progress {self.id}: {self.activity_type} - {self.percentage}%>'
    
    def calculate_percentage(self):
        """Calcular porcentaje de la actividad"""
        if self.max_score and self.max_score > 0:
            self.percentage = (self.score / self.max_score) * 100
        else:
            self.percentage = 0.0
        db.session.commit()
        return self.percentage
