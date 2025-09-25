#!/usr/bin/env python3
"""
Test rapide des fonctionnalités de base
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_calculations():
    """Test des calculs nutritionnels"""
    print("=== Test des calculs nutritionnels ===")

    from nutrition_generator.core.data_models import ClientData, NutritionParams
    from nutrition_generator.core.calculations import NutritionCalculator

    # Données de test
    client = ClientData(
        nom="Dupont",
        prenom="Marie",
        age=28,
        taille_cm=165,
        poids_kg=60.0,
        sexe="female"
    )

    params = NutritionParams(
        formule_metabolisme="mifflin_st_jeor",
        facteur_activite=1.55,
        deficit_surplus_kcal=-300,
        proteines_g_par_kg=1.8,
        lipides_g_par_kg=1.0
    )

    calculator = NutritionCalculator()
    results = calculator.calculate_complete_nutrition(client, params)

    print(f"Client: {client.prenom} {client.nom}")
    print(f"BMR: {results.bmr} kcal/jour")
    print(f"TDEE: {results.tdee} kcal/jour")
    print(f"Calories objectif: {results.calories_objectif} kcal/jour")
    print(f"Protéines: {results.proteines_g}g ({results.proteines_kcal} kcal)")
    print(f"Lipides: {results.lipides_g}g ({results.lipides_kcal} kcal)")
    print(f"Glucides: {results.glucides_g}g ({results.glucides_kcal} kcal)")
    print(f"Hydratation: {results.hydratation_ml} ml/jour")
    print("Calculs OK")

def test_pdf_generation():
    """Test de génération PDF"""
    print("\n=== Test de génération PDF ===")

    from nutrition_generator.core.data_models import ClientData, NutritionParams
    from nutrition_generator.core.calculations import NutritionCalculator
    from nutrition_generator.core.pdf_generator import PDFGenerator

    # Données de test
    client = ClientData(
        nom="Dupont",
        prenom="Marie",
        age=28,
        taille_cm=165,
        poids_kg=60.0,
        sexe="female"
    )

    params = NutritionParams(
        formule_metabolisme="mifflin_st_jeor",
        facteur_activite=1.55,
        deficit_surplus_kcal=-300,
        proteines_g_par_kg=1.8,
        lipides_g_par_kg=1.0
    )

    calculator = NutritionCalculator()
    results = calculator.calculate_complete_nutrition(client, params)

    # Génération PDF
    pdf_generator = PDFGenerator()
    output_path = "output/fiches/test_fiche.pdf"

    # Créer le dossier de sortie
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Paramètres pour le PDF
    params_dict = {
        'formule_metabolisme': params.formule_metabolisme,
        'facteur_activite': params.facteur_activite,
        'deficit_surplus_kcal': params.deficit_surplus_kcal,
        'proteines_g_par_kg': params.proteines_g_par_kg,
        'lipides_g_par_kg': params.lipides_g_par_kg
    }

    # Conseils
    objectif_type = calculator.get_objectif_description(params.deficit_surplus_kcal)
    conseils = calculator.get_conseils_nutritionnels(client, results, objectif_type)

    try:
        pdf_path = pdf_generator.generate_premium_pdf(client, results, params_dict, output_path, conseils)
        print(f"PDF Premium généré: {pdf_path}")
        print("Génération PDF Premium OK")
    except Exception as e:
        print(f"Erreur PDF: {e}")
        import traceback
        traceback.print_exc()

def test_gui_imports():
    """Test des imports GUI"""
    print("\n=== Test des imports GUI ===")

    try:
        import customtkinter as ctk
        print("CustomTkinter importé")

        from nutrition_generator.gui.components.client_form import ClientForm
        print("ClientForm importé")

        from nutrition_generator.gui.components.calculations_panel import CalculationsPanel
        print("CalculationsPanel importé")

        from nutrition_generator.gui.components.pdf_preview import PDFPreview
        print("PDFPreview importé")

        from nutrition_generator.gui.main_window import MainWindow
        print("MainWindow importé")

        print("Tous les imports GUI OK")

    except Exception as e:
        print(f"Erreur import GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Test de l'application Générateur de Fiches Nutritionnelles")
    print("=" * 60)

    try:
        test_calculations()
        test_pdf_generation()
        test_gui_imports()

        print("\nTous les tests sont réussis!")
        print("\nPour lancer l'application complète:")
        print("  python main.py")

    except Exception as e:
        print(f"\nErreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)