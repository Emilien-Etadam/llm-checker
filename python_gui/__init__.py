"""
LLM Checker GUI - Standalone Windows Application
Détecte le hardware et recommande les meilleurs modèles Ollama LLM
"""

__version__ = "1.0.0"
__author__ = "Based on llm-checker by Pavelevich"
__description__ = "Standalone GUI for LLM model recommendations based on hardware detection"

from .hardware_detector import HardwareDetector
from .model_scorer import ModelScorer
from .model_database import get_popular_models

__all__ = [
    'HardwareDetector',
    'ModelScorer',
    'get_popular_models'
]
