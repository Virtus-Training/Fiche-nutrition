#!/usr/bin/env python3
"""
Point d'entrée principal pour le Générateur de Fiches Nutritionnelles
Lanceur de l'application CustomTkinter
"""

import sys
import os

# Ajouter le répertoire du projet au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from nutrition_generator.main import main
    main()