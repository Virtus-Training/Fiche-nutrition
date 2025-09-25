"""
Calculs nutritionnels et métaboliques
Contient les formules pour BMR, TDEE et répartition des macronutriments
"""

import math
from typing import Tuple, Dict, Any
from .data_models import ClientData, NutritionParams, NutritionResults


class MetabolismCalculator:
    """Calculateur pour différentes formules de métabolisme de base"""

    @staticmethod
    def harris_benedict(weight: float, height: float, age: int, gender: str = 'male') -> float:
        """
        Formule Harris-Benedict pour le métabolisme de base

        Args:
            weight: Poids en kg
            height: Taille en cm
            age: Âge en années
            gender: 'male' ou 'female'

        Returns:
            BMR en kcal/jour
        """
        if gender == 'male':
            return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    @staticmethod
    def mifflin_st_jeor(weight: float, height: float, age: int, gender: str = 'male') -> float:
        """
        Formule Mifflin-St Jeor pour le métabolisme de base
        Plus précise pour les personnes en surpoids/obésité

        Args:
            weight: Poids en kg
            height: Taille en cm
            age: Âge en années
            gender: 'male' ou 'female'

        Returns:
            BMR en kcal/jour
        """
        base = (10 * weight) + (6.25 * height) - (5 * age)
        if gender == 'male':
            return base + 5
        else:
            return base - 161

    @staticmethod
    def katch_mcardle(weight: float, body_fat_percentage: float) -> float:
        """
        Formule Katch-McArdle basée sur la masse maigre

        Args:
            weight: Poids en kg
            body_fat_percentage: Pourcentage de graisse corporelle (0-100)

        Returns:
            BMR en kcal/jour
        """
        lean_mass = weight * (1 - body_fat_percentage / 100)
        return 370 + (21.6 * lean_mass)


class NutritionCalculator:
    """Calculateur principal pour toutes les valeurs nutritionnelles"""

    def __init__(self):
        self.metabolism_calc = MetabolismCalculator()

    def calculate_bmr(self, client: ClientData, formule: str) -> float:
        """
        Calcule le métabolisme de base selon la formule choisie

        Args:
            client: Données du client
            formule: Type de formule ('harris_benedict', 'mifflin_st_jeor', 'katch_mcardle')

        Returns:
            BMR en kcal/jour
        """
        if formule == 'harris_benedict':
            return self.metabolism_calc.harris_benedict(
                client.poids_kg, client.taille_cm, client.age, client.sexe
            )
        elif formule == 'mifflin_st_jeor':
            return self.metabolism_calc.mifflin_st_jeor(
                client.poids_kg, client.taille_cm, client.age, client.sexe
            )
        elif formule == 'katch_mcardle':
            if client.pourcentage_graisse is None:
                raise ValueError("Le pourcentage de graisse corporelle est requis pour Katch-McArdle")
            return self.metabolism_calc.katch_mcardle(
                client.poids_kg, client.pourcentage_graisse
            )
        else:
            raise ValueError(f"Formule inconnue: {formule}")

    def calculate_tdee(self, bmr: float, facteur_activite: float) -> float:
        """
        Calcule la dépense énergétique totale quotidienne

        Args:
            bmr: Métabolisme de base
            facteur_activite: Facteur d'activité (1.2 - 2.0)

        Returns:
            TDEE en kcal/jour
        """
        return bmr * facteur_activite

    def calculate_macros(self, client: ClientData, params: NutritionParams,
                        calories_objectif: float) -> Tuple[float, float, float]:
        """
        Calcule la répartition des macronutriments

        Args:
            client: Données du client
            params: Paramètres nutritionnels
            calories_objectif: Calories cibles quotidiennes

        Returns:
            Tuple (protéines_g, lipides_g, glucides_g)
        """
        # Calcul des protéines et lipides
        proteines_g = params.proteines_g_par_kg * client.poids_kg
        lipides_g = params.lipides_g_par_kg * client.poids_kg

        # Calories des protéines et lipides
        proteines_kcal = proteines_g * 4
        lipides_kcal = lipides_g * 9

        # Calories restantes pour les glucides
        glucides_kcal = calories_objectif - proteines_kcal - lipides_kcal
        glucides_g = max(0, glucides_kcal / 4)  # Minimum 0g

        return proteines_g, lipides_g, glucides_g

    def calculate_hydration(self, client: ClientData, facteur_activite: float) -> float:
        """
        Calcule les besoins en hydratation

        Args:
            client: Données du client
            facteur_activite: Facteur d'activité

        Returns:
            Hydratation recommandée en ml/jour
        """
        # Base: 35ml/kg
        base_hydration = client.poids_kg * 35

        # Ajustement selon l'activité
        activity_bonus = 0
        if facteur_activite >= 1.55:  # Modérément actif ou plus
            activity_bonus = 500
        elif facteur_activite >= 1.375:  # Légèrement actif
            activity_bonus = 250

        return base_hydration + activity_bonus

    def get_objectif_description(self, deficit_surplus: int) -> str:
        """
        Retourne la description de l'objectif basé sur le déficit/surplus

        Args:
            deficit_surplus: Déficit (-) ou surplus (+) en kcal

        Returns:
            Description de l'objectif
        """
        if deficit_surplus < -100:
            return "perte"
        elif deficit_surplus > 100:
            return "prise"
        else:
            return "maintenance"

    def get_conseils_nutritionnels(self, client: ClientData, results: NutritionResults,
                                  objectif_type: str) -> list:
        """
        Génère des conseils nutritionnels personnalisés

        Args:
            client: Données du client
            results: Résultats des calculs
            objectif_type: Type d'objectif ('perte', 'maintenance', 'prise')

        Returns:
            Liste de conseils nutritionnels
        """
        conseils = []

        # Conseils généraux
        conseils.append("• Répartissez vos repas sur 3-5 prises alimentaires dans la journée")
        conseils.append(f"• Hydratez-vous avec au moins {int(results.hydratation_ml)}ml d'eau par jour")

        # Conseils selon l'objectif
        if objectif_type == "perte":
            conseils.extend([
                "• Privilégiez les légumes à chaque repas pour la satiété",
                "• Consommez vos glucides principalement autour de l'entraînement",
                "• Maintenez un déficit modéré pour préserver la masse musculaire"
            ])
        elif objectif_type == "prise":
            conseils.extend([
                "• Augmentez progressivement vos portions sur 2-3 semaines",
                "• Ajoutez des collations riches en calories saines",
                "• Priorisez les glucides complexes et les bonnes graisses"
            ])
        else:  # maintenance
            conseils.extend([
                "• Maintenez un équilibre alimentaire régulier",
                "• Ajustez légèrement selon votre évolution physique",
                "• Focalisez-vous sur la qualité des aliments"
            ])

        # Conseils sur les protéines
        if results.proteines_g / client.poids_kg >= 2.0:
            conseils.append("• Répartissez vos protéines sur tous les repas (20-30g par prise)")
        else:
            conseils.append("• Assurez-vous d'avoir une source de protéines à chaque repas")

        return conseils

    def calculate_complete_nutrition(self, client: ClientData,
                                   params: NutritionParams) -> NutritionResults:
        """
        Calcule tous les besoins nutritionnels du client

        Args:
            client: Données du client
            params: Paramètres nutritionnels

        Returns:
            Résultats complets des calculs nutritionnels
        """
        # Calcul du métabolisme de base
        bmr = self.calculate_bmr(client, params.formule_metabolisme)

        # Calcul de la dépense énergétique totale
        tdee = self.calculate_tdee(bmr, params.facteur_activite)

        # Calories de maintenance et objectif
        calories_maintenance = tdee
        calories_objectif = tdee + params.deficit_surplus_kcal

        # Calcul des macronutriments
        proteines_g, lipides_g, glucides_g = self.calculate_macros(
            client, params, calories_objectif
        )

        # Conversion en calories
        proteines_kcal = proteines_g * 4
        lipides_kcal = lipides_g * 9
        glucides_kcal = glucides_g * 4

        # Calcul de l'hydratation
        hydratation_ml = self.calculate_hydration(client, params.facteur_activite)

        return NutritionResults(
            bmr=round(bmr, 0),
            tdee=round(tdee, 0),
            calories_maintenance=round(calories_maintenance, 0),
            calories_objectif=round(calories_objectif, 0),
            proteines_g=round(proteines_g, 1),
            proteines_kcal=round(proteines_kcal, 0),
            lipides_g=round(lipides_g, 1),
            lipides_kcal=round(lipides_kcal, 0),
            glucides_g=round(glucides_g, 1),
            glucides_kcal=round(glucides_kcal, 0),
            hydratation_ml=round(hydratation_ml, 0)
        )