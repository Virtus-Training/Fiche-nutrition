"""
Modèles de données pour les informations clients et nutritionnelles
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
import json


@dataclass
class ClientData:
    """Données personnelles du client"""
    nom: str
    prenom: str
    age: int
    taille_cm: int
    poids_kg: float
    sexe: str = 'male'  # 'male' ou 'female'
    pourcentage_graisse: Optional[float] = None

    def __post_init__(self):
        """Validation des données après initialisation"""
        if self.age < 10 or self.age > 100:
            raise ValueError("L'âge doit être entre 10 et 100 ans")
        if self.taille_cm < 100 or self.taille_cm > 250:
            raise ValueError("La taille doit être entre 100 et 250 cm")
        if self.poids_kg < 30 or self.poids_kg > 300:
            raise ValueError("Le poids doit être entre 30 et 300 kg")
        if self.sexe not in ['male', 'female']:
            raise ValueError("Le sexe doit être 'male' ou 'female'")


@dataclass
class NutritionParams:
    """Paramètres nutritionnels et objectifs"""
    formule_metabolisme: str  # 'harris_benedict', 'mifflin_st_jeor', 'katch_mcardle'
    facteur_activite: float  # 1.2 à 2.0
    deficit_surplus_kcal: int  # -500 à +500
    proteines_g_par_kg: float
    lipides_g_par_kg: float

    def __post_init__(self):
        """Validation des paramètres nutritionnels"""
        if self.facteur_activite < 1.0 or self.facteur_activite > 2.5:
            raise ValueError("Le facteur d'activité doit être entre 1.0 et 2.5")
        if self.deficit_surplus_kcal < -1000 or self.deficit_surplus_kcal > 1000:
            raise ValueError("Le déficit/surplus doit être entre -1000 et +1000 kcal")
        if self.proteines_g_par_kg < 0.5 or self.proteines_g_par_kg > 4.0:
            raise ValueError("Les protéines doivent être entre 0.5 et 4.0 g/kg")
        if self.lipides_g_par_kg < 0.3 or self.lipides_g_par_kg > 2.0:
            raise ValueError("Les lipides doivent être entre 0.3 et 2.0 g/kg")


@dataclass
class NutritionResults:
    """Résultats des calculs nutritionnels"""
    bmr: float  # Métabolisme de base
    tdee: float  # Dépense énergétique totale
    calories_maintenance: float
    calories_objectif: float
    proteines_g: float
    proteines_kcal: float
    lipides_g: float
    lipides_kcal: float
    glucides_g: float
    glucides_kcal: float
    hydratation_ml: float

    @property
    def macros_pourcentages(self) -> Dict[str, float]:
        """Pourcentages des macronutriments"""
        total_kcal = self.proteines_kcal + self.lipides_kcal + self.glucides_kcal
        if total_kcal == 0:
            return {"proteines": 0, "lipides": 0, "glucides": 0}

        return {
            "proteines": round((self.proteines_kcal / total_kcal) * 100, 1),
            "lipides": round((self.lipides_kcal / total_kcal) * 100, 1),
            "glucides": round((self.glucides_kcal / total_kcal) * 100, 1)
        }

    def to_dict(self) -> Dict[str, Any]:
        """Conversion en dictionnaire pour sauvegarde"""
        return {
            "bmr": self.bmr,
            "tdee": self.tdee,
            "calories_maintenance": self.calories_maintenance,
            "calories_objectif": self.calories_objectif,
            "proteines_g": self.proteines_g,
            "proteines_kcal": self.proteines_kcal,
            "lipides_g": self.lipides_g,
            "lipides_kcal": self.lipides_kcal,
            "glucides_g": self.glucides_g,
            "glucides_kcal": self.glucides_kcal,
            "hydratation_ml": self.hydratation_ml,
            "macros_pourcentages": self.macros_pourcentages
        }


@dataclass
class FicheMetadata:
    """Métadonnées d'une fiche générée"""
    nom_fichier: str
    client_nom: str
    client_prenom: str
    date_creation: datetime
    calories_objectif: float
    objectif_type: str  # 'perte', 'maintenance', 'prise'

    def to_dict(self) -> Dict[str, Any]:
        """Conversion en dictionnaire pour sauvegarde"""
        return {
            "nom_fichier": self.nom_fichier,
            "client_nom": self.client_nom,
            "client_prenom": self.client_prenom,
            "date_creation": self.date_creation.isoformat(),
            "calories_objectif": self.calories_objectif,
            "objectif_type": self.objectif_type
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FicheMetadata':
        """Création depuis un dictionnaire"""
        return cls(
            nom_fichier=data["nom_fichier"],
            client_nom=data["client_nom"],
            client_prenom=data["client_prenom"],
            date_creation=datetime.fromisoformat(data["date_creation"]),
            calories_objectif=data["calories_objectif"],
            objectif_type=data["objectif_type"]
        )


# Constantes pour les formules et niveaux d'activité
FORMULES_METABOLISME = {
    "harris_benedict": "Harris-Benedict - Formule classique, convient à la plupart des cas",
    "mifflin_st_jeor": "Mifflin-St Jeor - Plus précise pour surpoids/obésité",
    "katch_mcardle": "Katch-McArdle - Pour composition corporelle connue"
}

NIVEAUX_ACTIVITE = {
    1.2: "Sédentaire (bureau, pas d'exercice)",
    1.375: "Légèrement actif (1-3x/semaine)",
    1.55: "Modérément actif (3-5x/semaine)",
    1.725: "Très actif (6-7x/semaine)",
    1.9: "Extrêmement actif (quotidien + physique)"
}