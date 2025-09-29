"""
Módulos de Inteligencia Artificial para el STI
"""

from .google_forms_integration import GoogleFormsIntegration
from .vark_analyzer import VARKAnalyzer
from .learning_path_generator import LearningPathGenerator
from .recommendation_engine import RecommendationEngine
from .analytics_engine import AnalyticsEngine

__all__ = [
    'GoogleFormsIntegration',
    'VARKAnalyzer', 
    'LearningPathGenerator',
    'RecommendationEngine',
    'AnalyticsEngine'
]
