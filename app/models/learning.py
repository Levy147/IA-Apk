"""
Modelos de rutas de aprendizaje y recursos
"""

from datetime import datetime
import enum
from app import db

class ResourceType(enum.Enum):
    """Tipos de recursos de aprendizaje"""
    VIDEO = "video"
    READING = "reading"
    EXERCISE = "exercise"
    QUIZ = "quiz"
    SIMULATION = "simulation"
    GAME = "game"

class LearningStyle(enum.Enum):
    """Estilos de aprendizaje VARK"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    READING = "reading"
    KINESTHETIC = "kinesthetic"

class StepStatus(enum.Enum):
    """Estado de un paso en la ruta de aprendizaje"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"

class LearningPath(db.Model):
    """Ruta de aprendizaje personalizada"""
    __tablename__ = 'learning_paths'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('course_enrollments.id'), nullable=False)
    
    # Configuración de la ruta
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    total_steps = db.Column(db.Integer, default=0)
    current_step = db.Column(db.Integer, default=0)
    
    # Personalización basada en perfil del estudiante
    learning_style = db.Column(db.Enum(LearningStyle))
    difficulty_level = db.Column(db.String(20))
    estimated_duration = db.Column(db.Integer)  # Duración estimada en minutos
    
    # Estado de la ruta
    is_active = db.Column(db.Boolean, default=True)
    is_completed = db.Column(db.Boolean, default=False)
    completion_percentage = db.Column(db.Float, default=0.0)
    
    # Fechas
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    steps = db.relationship('LearningPathStep', backref='learning_path', cascade='all, delete-orphan', order_by='LearningPathStep.step_order')
    
    def __repr__(self):
        return f'<LearningPath {self.id} for {self.student.student_id}>'
    
    def get_next_step(self):
        """Obtener siguiente paso en la ruta"""
        return LearningPathStep.query.filter_by(
            learning_path_id=self.id,
            step_order=self.current_step + 1
        ).first()
    
    def update_progress(self):
        """Actualizar progreso de la ruta"""
        completed_steps = len([step for step in self.steps if step.status == StepStatus.COMPLETED])
        self.completion_percentage = (completed_steps / self.total_steps) * 100 if self.total_steps > 0 else 0
        
        if self.completion_percentage >= 100:
            self.is_completed = True
            self.completed_at = datetime.utcnow()
        
        db.session.commit()

class LearningPathStep(db.Model):
    """Paso individual en una ruta de aprendizaje"""
    __tablename__ = 'learning_path_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    learning_path_id = db.Column(db.Integer, db.ForeignKey('learning_paths.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    competency_id = db.Column(db.Integer, db.ForeignKey('competencies.id'))
    
    # Configuración del paso
    step_order = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Estado del paso
    status = db.Column(db.Enum(StepStatus), default=StepStatus.PENDING)
    is_required = db.Column(db.Boolean, default=True)
    
    # Metadatos
    estimated_time = db.Column(db.Integer)  # Tiempo estimado en minutos
    points = db.Column(db.Integer, default=1)
    
    # Fechas
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LearningPathStep {self.step_order}: {self.title}>'
    
    def complete_step(self):
        """Marcar paso como completado"""
        self.status = StepStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        db.session.commit()
        
        # Actualizar progreso de la ruta
        self.learning_path.update_progress()

class Resource(db.Model):
    """Recursos de aprendizaje"""
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    competency_id = db.Column(db.Integer, db.ForeignKey('competencies.id'))
    
    # Información del recurso
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    resource_type = db.Column(db.Enum(ResourceType), nullable=False)
    
    # Contenido del recurso
    content_url = db.Column(db.String(500))  # URL del recurso
    content_text = db.Column(db.Text)  # Contenido de texto
    file_path = db.Column(db.String(500))  # Ruta del archivo local
    
    # Metadatos
    difficulty_level = db.Column(db.String(20))
    duration = db.Column(db.Integer)  # Duración en minutos
    points = db.Column(db.Integer, default=1)
    
    # Compatibilidad con estilos de aprendizaje
    visual_score = db.Column(db.Float, default=0.0)  # 0.0 a 1.0
    auditory_score = db.Column(db.Float, default=0.0)
    reading_score = db.Column(db.Float, default=0.0)
    kinesthetic_score = db.Column(db.Float, default=0.0)
    
    # Estado
    is_active = db.Column(db.Boolean, default=True)
    is_required = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    learning_steps = db.relationship('LearningPathStep', backref='resource', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Resource {self.id}: {self.title}>'
    
    def get_learning_style_scores(self):
        """Obtener puntajes de compatibilidad con estilos de aprendizaje"""
        return {
            'visual': self.visual_score,
            'auditory': self.auditory_score,
            'reading': self.reading_score,
            'kinesthetic': self.kinesthetic_score
        }
    
    def is_suitable_for_style(self, learning_style, threshold=0.5):
        """Verificar si el recurso es adecuado para un estilo de aprendizaje"""
        scores = self.get_learning_style_scores()
        return scores.get(learning_style.value, 0.0) >= threshold
