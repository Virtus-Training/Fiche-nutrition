"""
Point d'entrée principal pour le Générateur de Fiches Nutritionnelles
Application complète avec interface CustomTkinter pour coaches sportifs
"""

import os
import sys
import logging
from datetime import datetime

# Configuration du logging
def setup_logging():
    """Configure le système de logging"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = f"nutrition_app_{datetime.now().strftime('%Y%m%d')}.log"
    log_path = os.path.join(log_dir, log_filename)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    required_packages = [
        'customtkinter',
        'reportlab',
        'matplotlib',
        'PIL'  # Pillow
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("ERREUR: Dépendances manquantes:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstallation requise:")
        print("   pip install -r requirements.txt")
        return False

    return True

def check_directories():
    """Vérifie et crée les répertoires nécessaires"""
    required_dirs = [
        "output",
        "output/fiches",
        "logs",
        "assets",
        "assets/icons"
    ]

    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Dossier créé: {directory}")

def create_placeholder_assets():
    """Crée des assets de démonstration si nécessaires"""
    # Créer un logo placeholder si il n'existe pas
    logo_path = "assets/logo.png"
    if not os.path.exists(logo_path):
        try:
            from PIL import Image, ImageDraw, ImageFont

            # Créer une image de logo simple
            img = Image.new('RGB', (200, 80), color='#1f538d')
            draw = ImageDraw.Draw(img)

            # Texte du logo
            try:
                # Essayer d'utiliser une police système
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()

            text = "COACH PRO"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            x = (200 - text_width) // 2
            y = (80 - text_height) // 2

            draw.text((x, y), text, fill='white', font=font)
            img.save(logo_path)
            print(f"Logo placeholder créé: {logo_path}")

        except Exception as e:
            print(f"ATTENTION: Impossible de créer le logo: {e}")

def main():
    """Fonction principale de l'application"""
    print("Générateur de Fiches Nutritionnelles - Coach Pro")
    print("=" * 50)

    # Configuration du logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Vérifications préliminaires
        print("Vérification des dépendances...")
        if not check_dependencies():
            sys.exit(1)

        print("Toutes les dépendances sont installées")

        # Vérification et création des dossiers
        print("Vérification des dossiers...")
        check_directories()

        # Création des assets de démonstration
        print("Préparation des assets...")
        create_placeholder_assets()

        # Import et lancement de l'application
        print("Lancement de l'application...")
        logger.info("Démarrage de l'application")

        from .gui.main_window import MainWindow

        # Lancer l'application
        app = MainWindow()
        app.run()

        logger.info("Application fermée normalement")
        print("Au revoir!")

    except KeyboardInterrupt:
        print("\nApplication interrompue par l'utilisateur")
        logger.info("Application interrompue par l'utilisateur")

    except Exception as e:
        error_msg = f"Erreur fatale: {str(e)}"
        print(f"ERREUR: {error_msg}")
        logger.error(error_msg, exc_info=True)

        # En mode développement, afficher la traceback complète
        if "--debug" in sys.argv:
            raise

        sys.exit(1)

if __name__ == "__main__":
    main()