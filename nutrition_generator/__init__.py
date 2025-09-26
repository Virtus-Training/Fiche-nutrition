"""
Générateur de fiches nutritionnelles professionnelles
"""

__version__ = "1.0.0"
__author__ = "Virtus Training"

# Imports principaux pour faciliter l'utilisation
from .core.calculations import NutritionCalculator
from .core.pdf_generator import PDFGenerator
from .gui.main_window import MainWindow