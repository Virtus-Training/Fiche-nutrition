#!/usr/bin/env python3
"""
Test de l'interface avec données pré-remplies pour visualiser les améliorations
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_interface_with_data():
    """Lance l'app et charge automatiquement des données de test"""

    from nutrition_generator.gui.main_window import MainWindow

    # Créer l'application
    app = MainWindow()

    # Attendre que l'interface soit prête
    app.after(500, lambda: app.client_form.load_example_data())

    # Auto-calculer après le chargement des données
    app.after(1000, lambda: app.calculations_panel.auto_calculate_if_ready())

    # Lancer l'application
    app.run()

if __name__ == "__main__":
    print("Test de l'interface améliorée avec données pré-chargées")
    print("=" * 60)
    print("✨ Nouvelles fonctionnalités:")
    print("   🎨 Interface colorée avec icônes")
    print("   📱 Panneau de calculs avec scrolling")
    print("   🔘 Boutons plus grands et colorés")
    print("   🖼️ Bordures colorées par section")
    print("   📊 Meilleure séparation visuelle")
    print("\n🚀 Lancement de l'interface...")

    test_interface_with_data()