# Cahier des charges - Générateur de fiches nutritionnelles professionnelles

## 1. Vue d'ensemble du projet

### Objectif
Développer un logiciel Python avec interface graphique CTK pour générer des fiches nutritionnelles professionnelles au format PDF, personnalisées pour chaque client.

### Utilisateur cible
Coach sportif/nutritionniste professionnel (utilisateur unique)

### Technologie
- Python avec CustomTkinter (CTK) pour l'interface
- Génération PDF avec reportlab ou matplotlib
- Stockage local uniquement

## 2. Fonctionnalités principales

### 2.1 Interface utilisateur (CTK)
- Design inspiré du thème coach.pro (theme.json du GitHub)
- Interface moderne et professionnelle
- Formulaire de saisie des données client
- Visualisation des fiches PDF générées
- Navigation simple et intuitive

### 2.2 Saisie des données client
#### Informations personnelles
- Nom (obligatoire)
- Prénom (obligatoire)
- Âge (obligatoire)
- Taille en cm (obligatoire)
- Poids en kg (obligatoire)

#### Paramètres nutritionnels
- **Formule métabolisme de base** (sélection avec descriptions) :
  - Harris-Benedict : "Formule classique, convient à la plupart des cas"
  - Mifflin-St Jeor : "Plus précise pour les personnes en surpoids/obésité"
  - Katch-McArdle : "Pour les personnes avec composition corporelle connue"

- **Niveau d'activité** (coefficient ajustable 1.0 - 2.0) :
  - 1.2 : "Sédentaire (travail de bureau, pas d'exercice)"
  - 1.375 : "Légèrement actif (exercice léger 1-3x/semaine)"
  - 1.55 : "Modérément actif (exercice modéré 3-5x/semaine)"
  - 1.725 : "Très actif (exercice intense 6-7x/semaine)"
  - 1.9 : "Extrêmement actif (travail physique + exercice quotidien)"

- **Objectif** (déficit/surplus -500 à +500 kcal) :
  - Perte de poids : -200 à -500 kcal
  - Recomposition corporelle : -100 à +100 kcal
  - Prise de masse : +200 à +500 kcal

#### Répartition des macronutriments (ajustable)
- **Protéines** : 1.6-2.2 g/kg (pré-rempli selon objectif)
- **Lipides** : 0.8-1.2 g/kg (pré-rempli selon objectif)
- **Glucides** : Calculés automatiquement (reste calorique)

### 2.3 Calculs automatiques
- Métabolisme de base selon formule choisie
- Dépense énergétique totale (MB × coefficient activité)
- Calories objectif (maintenance ± déficit/surplus)
- Répartition macro en grammes et calories
- Conseils nutritionnels personnalisés

## 3. Génération du PDF

### 3.1 Structure de la fiche (format A4)
#### En-tête
- Logo coach (PNG fourni)
- Titre "FICHE NUTRITIONNELLE PERSONNALISÉE"
- Informations de contact : Instagram, téléphone, email

#### Section 1 : Profil client
- Nom, Prénom, Âge, Taille, Poids
- Niveau d'activité (texte explicatif)
- Objectif défini

#### Section 2 : Besoins caloriques
- Métabolisme de base (formule utilisée mentionnée)
- Dépense énergétique totale
- Calories de maintenance
- Calories objectif
- Déficit/Surplus appliqué (avec couleur : rouge pour déficit, vert pour surplus)

#### Section 3 : Répartition des macronutriments
- Tableau détaillé : Protéines, Lipides, Glucides (en g et kcal)
- Pie chart des macronutriments (en grammes)
- Pourcentages de répartition

#### Section 4 : Graphiques
- Courbe de poids estimée sur 12 semaines
- Graphiques additionnels pertinents (barres comparatives, etc.)

#### Section 5 : Conseils nutritionnels
- Apport hydrique recommandé (35ml/kg + ajustement activité)
- Conseils timing des repas
- Recommandations spécifiques à l'objectif
- Conseils généraux de nutrition

#### Pied de page
- Date de création
- "Fiche établie par [Nom du coach]"
- Rappel des contacts

### 3.2 Design graphique
- Charte graphique coach.pro (theme.json)
- Séparateurs visuels entre sections
- Icônes appropriées (nutrition, sport, santé)
- Mise en page professionnelle et aérée
- Couleurs cohérentes avec la marque

## 4. Fonctionnalités techniques

### 4.1 Gestion des fichiers
- **Stockage** : Dossier local "Fiches_Nutrition/"
- **Nomenclature** : "Fiche_Prénom_Nom_AAAAMMJJ.pdf"
- **Visualisation** : Liste des fiches créées dans l'interface
- **Aperçu** : Possibilité d'ouvrir les PDF depuis l'application

### 4.2 Validation des données
- Contrôle de saisie (âge > 0, poids > 0, taille > 0)
- Messages d'erreur explicites
- Sauvegarde des paramètres par défaut

### 4.3 Configuration
- Fichier de configuration pour les informations coach
- Paramètres par défaut modifiables
- Import du logo

## 5. Architecture technique

### 5.1 Structure des fichiers
```
nutrition_generator/
├── main.py                 # Point d'entrée
├── gui/
│   ├── __init__.py
│   ├── main_window.py     # Interface principale
│   ├── components/        # Composants CTK
│   └── theme.json         # Thème coach.pro
├── core/
│   ├── __init__.py
│   ├── calculations.py    # Calculs nutritionnels
│   ├── pdf_generator.py   # Génération PDF
│   └── data_models.py     # Modèles de données
├── assets/
│   ├── logo.png
│   └── icons/
├── config/
│   └── settings.json      # Configuration
└── output/
    └── fiches/            # PDFs générés
```

### 5.2 Dépendances requises
- customtkinter
- reportlab ou matplotlib (PDF)
- PIL (gestion images)
- datetime
- json
- os

## 6. Spécifications d'interface

### 6.1 Fenêtre principale
- Dimensions : 1000x700 pixels
- Titre : "Générateur de Fiches Nutritionnelles - Coach Pro"
- Layout responsive avec CTK

### 6.2 Sections interface
1. **Panneau de saisie** (gauche) : Formulaire client
2. **Panneau de paramètres** (centre) : Calculs et répartitions
3. **Panneau d'aperçu** (droite) : Résumé et génération
4. **Panneau inférieur** : Liste des fiches créées

### 6.3 Boutons principaux
- "Calculer" : Mise à jour des calculs
- "Générer PDF" : Création de la fiche
- "Réinitialiser" : Vider le formulaire
- "Ouvrir dossier" : Accès aux fiches créées

## 7. Livrables attendus

1. **Application complète** avec interface CTK
2. **Documentation** d'utilisation
3. **Fichier de configuration** exemple
4. **Template de thème** coach.pro intégré
5. **Exemples de fiches** PDF générées

## 8. Contraintes et exigences

### 8.1 Performance
- Génération PDF < 5 secondes
- Interface fluide et responsive
- Gestion d'erreur robuste

### 8.2 Compatibilité
- Python 3.8+
- Windows/Mac/Linux
- Polices système standard

### 8.3 Qualité
- Code documenté et structuré
- Respect des bonnes pratiques Python
- Interface intuitive sans formation préalable