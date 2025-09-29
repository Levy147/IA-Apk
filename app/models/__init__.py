"""
Modelos de la base de datos para el Sistema de Tutoría Inteligente (STI)
"""

# Importar modelos en el orden correcto para evitar problemas de relaciones
from .user import User, Student, Teacher
from .course import Course, CourseEnrollment
from .assessment import Question, DiagnosticExam, ExamResponse, VARKQuestion, VARKResponse
from .learning import LearningPath, LearningPathStep, Resource, ResourceType
from .progress import Progress, Competency, CompetencyMastery
from .ai import AIModel, LearningRecommendation

__all__ = [
    'User', 'Student', 'Teacher',
    'Course', 'CourseEnrollment', 
    'Question', 'DiagnosticExam', 'ExamResponse', 'VARKQuestion', 'VARKResponse',
    'LearningPath', 'LearningPathStep', 'Resource', 'ResourceType',
    'Progress', 'Competency', 'CompetencyMastery',
    'AIModel', 'LearningRecommendation'
]
