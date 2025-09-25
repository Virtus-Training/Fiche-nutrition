# 🏋️ Générateur de Fiches Nutritionnelles - Coach Pro

Application complète en Python avec interface CustomTkinter pour générer des fiches nutritionnelles professionnelles destinées aux clients de coaches sportifs.

## ✨ Fonctionnalités

- **Interface moderne CustomTkinter** : Interface utilisateur intuitive et responsive
- **Calculs nutritionnels avancés** : Multiples formules de métabolisme (Harris-Benedict, Mifflin-St Jeor, Katch-McArdle)
- **Génération PDF professionnelle** : Fiches brandées avec graphiques et mise en page soignée
- **Personnalisation complète** : Adaptation aux objectifs (perte, maintenance, prise de masse)
- **Gestion des fiches** : Historique, ouverture et organisation des PDFs générés

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Lancement de l'application
```bash
python main.py
```

## 📦 Dépendances

- `customtkinter>=5.2.0` - Interface utilisateur moderne
- `reportlab>=4.0.0` - Génération de PDFs
- `matplotlib>=3.7.0` - Création de graphiques
- `Pillow>=10.0.0` - Traitement d'images

## 🎯 Utilisation

### 1. Saisie des données client
- Remplissez les informations personnelles (nom, prénom, âge, taille, poids)
- Sélectionnez le sexe et optionnellement le pourcentage de graisse corporelle

### 2. Configuration des paramètres nutritionnels
- Choisissez la formule de métabolisme adaptée
- Ajustez le niveau d'activité avec le slider
- Définissez l'objectif calorique (déficit/surplus)
- Personnalisez les ratios de macronutriments

### 3. Génération de la fiche
- Cliquez sur "Calculer" pour voir les résultats
- Vérifiez les besoins nutritionnels affichés
- Cliquez sur "Générer PDF" pour créer la fiche professionnelle

### 4. Gestion des fiches
- Visualisez l'historique des fiches générées
- Ouvrez directement les PDFs
- Accédez au dossier de sortie

## ⌨️ Raccourcis clavier

- `Ctrl+R` : Réinitialiser tous les formulaires
- `F1` : Afficher l'aide
- `F5` : Charger des données d'exemple

## 📁 Structure du projet

```
nutrition_generator/
├── main.py                    # Point d'entrée principal
├── gui/                       # Interface utilisateur
│   ├── main_window.py        # Fenêtre principale
│   ├── components/           # Composants GUI
│   │   ├── client_form.py    # Formulaire client
│   │   ├── calculations_panel.py # Panneau calculs
│   │   └── pdf_preview.py    # Aperçu et gestion PDF
│   └── theme.json           # Configuration du thème
├── core/                     # Logique métier
│   ├── calculations.py       # Calculs nutritionnels
│   ├── pdf_generator.py      # Génération PDF
│   └── data_models.py        # Modèles de données
├── config/                   # Configuration
│   └── settings.json         # Paramètres de l'application
├── assets/                   # Ressources
│   └── icons/               # Icônes de l'application
└── output/                   # Fichiers générés
    └── fiches/              # PDFs de fiches nutritionnelles
```

## ⚙️ Configuration

### Personnalisation des informations coach
Éditez le fichier `nutrition_generator/config/settings.json` :

```json
{
    "coach_info": {
        "name": "Votre Nom",
        "instagram": "@votre_instagram",
        "phone": "+33 6 XX XX XX XX",
        "email": "votre@email.fr"
    }
}
```

### Valeurs par défaut
Ajustez les valeurs par défaut dans la même configuration :

```json
{
    "default_values": {
        "activity_factor": 1.55,
        "protein_ratio": 1.8,
        "fat_ratio": 1.0
    }
}
```

## 📊 Formules disponibles

### Métabolisme de base (BMR)

1. **Harris-Benedict** (formule classique)
   - Hommes: 88.362 + (13.397 × poids) + (4.799 × taille) - (5.677 × âge)
   - Femmes: 447.593 + (9.247 × poids) + (3.098 × taille) - (4.330 × âge)

2. **Mifflin-St Jeor** (plus précise pour surpoids/obésité)
   - Hommes: (10 × poids) + (6.25 × taille) - (5 × âge) + 5
   - Femmes: (10 × poids) + (6.25 × taille) - (5 × âge) - 161

3. **Katch-McArdle** (basée sur la composition corporelle)
   - 370 + (21.6 × masse maigre)

### Niveaux d'activité

- **1.2** : Sédentaire (bureau, pas d'exercice)
- **1.375** : Légèrement actif (1-3x/semaine)
- **1.55** : Modérément actif (3-5x/semaine)
- **1.725** : Très actif (6-7x/semaine)
- **1.9** : Extrêmement actif (quotidien + physique)

## 🔧 Développement

### Tests avec données d'exemple
Appuyez sur `F5` dans l'application pour charger des données de test.

### Mode debug
```bash
python main.py --debug
```

### Logs
Les logs sont automatiquement générés dans le dossier `logs/`.

## 📝 Format des PDFs générés

Chaque fiche PDF contient :
- En-tête avec informations du coach
- Profil client avec données personnelles
- Besoins caloriques détaillés (BMR, TDEE, objectif)
- Tableau des macronutriments avec pourcentages
- Graphique en secteurs de la répartition
- Recommandations d'hydratation
- Conseils nutritionnels personnalisés
- Pied de page avec date et signature

## 🆘 Support

### Problèmes courants

**L'application ne se lance pas :**
- Vérifiez que Python 3.8+ est installé
- Installez les dépendances : `pip install -r requirements.txt`

**Erreur de génération PDF :**
- Vérifiez que le dossier `output/fiches` existe
- Assurez-vous d'avoir les droits d'écriture

**Interface déformée :**
- Augmentez la taille de la fenêtre (minimum 1000x700)
- Vérifiez la version de CustomTkinter

### Logs et debug
Consultez les fichiers de log dans `logs/` pour plus d'informations sur les erreurs.

## 📄 Licence

Ce projet est destiné à un usage professionnel pour les coaches sportifs.

## 🔄 Versions

- **v1.0.0** : Version initiale complète avec toutes les fonctionnalités