"""
Modelos para el motor de IA del STI
"""

from datetime import datetime
import enum
import json
from app import db

class AIModelType(enum.Enum):
    """Tipos de modelos de IA"""
    LEARNING_PATH_GENERATOR = "learning_path_generator"
    RESOURCE_RECOMMENDER = "resource_recommender"
    DIFFICULTY_ADJUSTER = "difficulty_adjuster"
    PERFORMANCE_PREDICTOR = "performance_predictor"

class AIModel(db.Model):
    """Modelos de IA utilizados en el sistema"""
    __tablename__ = 'ai_models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model_type = db.Column(db.Enum(AIModelType), nullable=False)
    version = db.Column(db.String(20), default="1.0")
    
    # Configuración del modelo
    model_path = db.Column(db.String(500))  # Ruta al archivo del modelo
    parameters = db.Column(db.JSON)  # Parámetros del modelo
    training_data_size = db.Column(db.Integer)
    
    # Métricas de rendimiento
    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    
    # Estado
    is_active = db.Column(db.Boolean, default=True)
    is_trained = db.Column(db.Boolean, default=False)
    
    # Fechas
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    trained_at = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    recommendations = db.relationship('LearningRecommendation', backref='ai_model', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<AIModel {self.name} v{self.version}>'
    
    def update_metrics(self, accuracy, precision, recall, f1_score):
        """Actualizar métricas del modelo"""
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.f1_score = f1_score
        self.trained_at = datetime.utcnow()
        self.is_trained = True
        db.session.commit()

class LearningRecommendation(db.Model):
    """Recomendaciones generadas por IA"""
    __tablename__ = 'learning_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    ai_model_id = db.Column(db.Integer, db.ForeignKey('ai_models.id'), nullable=False)
    
    # Tipo de recomendación
    recommendation_type = db.Column(db.String(50), nullable=False)  # 'resource', 'path', 'difficulty'
    target_id = db.Column(db.Integer)  # ID del recurso, ruta, etc.
    
    # Información de la recomendación
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    reasoning = db.Column(db.Text)  # Explicación de por qué se recomienda
    
    # Puntuación de la recomendación
    confidence_score = db.Column(db.Float)  # 0.0 a 1.0
    relevance_score = db.Column(db.Float)  # 0.0 a 1.0
    priority = db.Column(db.Integer, default=1)  # 1-5, mayor número = mayor prioridad
    
    # Estado
    is_accepted = db.Column(db.Boolean, default=False)
    is_implemented = db.Column(db.Boolean, default=False)
    feedback_score = db.Column(db.Integer)  # 1-5, calificación del estudiante
    
    # Fechas
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime)
    implemented_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<LearningRecommendation {self.id}: {self.title}>'
    
    def accept_recommendation(self):
        """Aceptar recomendación"""
        self.is_accepted = True
        self.accepted_at = datetime.utcnow()
        db.session.commit()
    
    def implement_recommendation(self):
        """Marcar recomendación como implementada"""
        self.is_implemented = True
        self.implemented_at = datetime.utcnow()
        db.session.commit()
    
    def provide_feedback(self, score):
        """Proporcionar retroalimentación sobre la recomendación"""
        self.feedback_score = score
        db.session.commit()

class LearningAnalytics(db.Model):
    """Analíticas de aprendizaje para mejorar el sistema"""
    __tablename__ = 'learning_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    # Métricas de comportamiento
    session_duration = db.Column(db.Integer)  # Duración de la sesión en segundos
    questions_attempted = db.Column(db.Integer, default=0)
    questions_correct = db.Column(db.Integer, default=0)
    hints_used = db.Column(db.Integer, default=0)
    resources_accessed = db.Column(db.Integer, default=0)
    
    # Métricas de rendimiento
    average_response_time = db.Column(db.Float)
    accuracy_rate = db.Column(db.Float)
    engagement_score = db.Column(db.Float)  # 0.0 a 1.0
    
    # Patrones de aprendizaje
    preferred_time_of_day = db.Column(db.String(20))  # 'morning', 'afternoon', 'evening'
    preferred_difficulty = db.Column(db.String(20))  # 'easy', 'medium', 'hard'
    learning_style_accuracy = db.Column(db.Float)  # Qué tan bien funciona el estilo detectado
    
    # Fechas
    session_date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LearningAnalytics {self.id} for {self.student.student_id}>'
    
    def calculate_engagement_score(self):
        """Calcular puntaje de engagement"""
        # Fórmula simple para engagement basada en actividad
        if self.questions_attempted > 0:
            accuracy_factor = self.questions_correct / self.questions_attempted
            activity_factor = min(1.0, self.questions_attempted / 20)  # Normalizar a 20 preguntas
            self.engagement_score = (accuracy_factor * 0.6) + (activity_factor * 0.4)
        else:
            self.engagement_score = 0.0
        
        db.session.commit()
        return self.engagement_score
