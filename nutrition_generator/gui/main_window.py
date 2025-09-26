"""
Fenêtre principale de l'application de génération de fiches nutritionnelles
"""

import os
import json
import threading
from datetime import datetime
from typing import Optional, Dict, Any
import customtkinter as ctk

from gui.components.client_form import ClientForm
from gui.components.calculations_panel import CalculationsPanel
from gui.components.pdf_preview import PDFPreview
from core.data_models import ClientData, NutritionResults, NutritionParams
from core.calculations import NutritionCalculator
from core.pdf_generator import PDFGenerator


class MainWindow(ctk.CTk):
    """Fenêtre principale de l'application"""

    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.title("Générateur de Fiches Nutritionnelles - Coach Pro")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Configuration du thème
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Configuration des couleurs personnalisées
        self.configure(fg_color="#f8f9fa")

        # Variables d'état
        self.current_client: Optional[ClientData] = None
        self.current_results: Optional[NutritionResults] = None
        self.current_params: Optional[NutritionParams] = None

        # Initialisation des composants métier
        self.calculator = NutritionCalculator()
        self.pdf_generator = PDFGenerator(self._get_config_path())

        # Configuration de l'interface
        self._setup_ui()
        self._setup_layout()

        # Chargement de la configuration
        self._load_config()

    def _get_config_path(self) -> str:
        """Retourne le chemin vers le fichier de configuration"""
        return os.path.join("nutrition_generator", "config", "settings.json")

    def _load_config(self):
        """Charge la configuration de l'application"""
        config_path = self._get_config_path()
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement de la configuration: {e}")
                self.config = self._get_default_config()
        else:
            self.config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Retourne la configuration par défaut"""
        return {
            "coach_info": {
                "name": "Coach Pro",
                "instagram": "@coach_pro",
                "phone": "+33 6 XX XX XX XX",
                "email": "contact@coach-pro.fr"
            },
            "default_values": {
                "activity_factor": 1.55,
                "protein_ratio": 1.8,
                "fat_ratio": 1.0
            }
        }

    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        # En-tête de l'application
        self.header_frame = ctk.CTkFrame(
            self,
            height=70,
            fg_color="#2c3e50",
            corner_radius=10
        )
        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.header_frame.pack_propagate(False)

        # Titre principal
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🍽️ Générateur de Fiches Nutritionnelles - Coach Pro",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.title_label.pack(pady=18)

        # Conteneur principal
        self.main_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.main_container.pack(fill="both", expand=True, padx=15, pady=10)

        # Configuration de la grille principale (3 colonnes)
        self.main_container.grid_columnconfigure(0, weight=2, minsize=300)  # Client
        self.main_container.grid_columnconfigure(1, weight=3, minsize=380)  # Calculs
        self.main_container.grid_columnconfigure(2, weight=2, minsize=320)  # Résultats
        self.main_container.grid_rowconfigure(0, weight=1)

    def _setup_layout(self):
        """Configure la disposition des composants"""
        # Panneau gauche : Formulaire client
        self.client_form = ClientForm(
            self.main_container,
            on_data_change=self._on_client_data_change,
            fg_color="white",
            border_color="#bdc3c7",
            border_width=1,
            corner_radius=8
        )
        self.client_form.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)

        # Panneau central : Paramètres et calculs
        self.calculations_panel = CalculationsPanel(
            self.main_container,
            on_calculation_update=self._on_calculation_update,
            fg_color="white",
            border_color="#bdc3c7",
            border_width=1,
            corner_radius=8
        )
        self.calculations_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Panneau droit : Résultats et PDF
        self.pdf_preview = PDFPreview(
            self.main_container,
            on_generate_pdf=self._generate_pdf,
            fg_color="white",
            border_color="#bdc3c7",
            border_width=1,
            corner_radius=8
        )
        self.pdf_preview.grid(row=0, column=2, sticky="nsew", padx=(5, 0), pady=5)

        # Barre de statut
        self.status_frame = ctk.CTkFrame(
            self,
            height=30,
            fg_color="#ecf0f1",
            corner_radius=5
        )
        self.status_frame.pack(fill="x", padx=10, pady=(5, 10))
        self.status_frame.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Prêt - Remplissez les informations client pour commencer",
            font=ctk.CTkFont(size=10),
            text_color="#2c3e50"
        )
        self.status_label.pack(pady=6)

        # Menu et raccourcis
        self._setup_menu()

    def _setup_menu(self):
        """Configure le menu de l'application"""
        # Raccourcis clavier
        self.bind("<Control-r>", lambda e: self._reset_all())
        self.bind("<Control-s>", lambda e: self._save_as_template())
        self.bind("<F1>", lambda e: self._show_help())
        self.bind("<F5>", lambda e: self._load_example_data())

    def _on_client_data_change(self):
        """Gestionnaire de changement des données client"""
        # Récupérer les nouvelles données client
        client_data = self.client_form.get_client_data()

        if client_data:
            self.current_client = client_data
            # Transmettre au panneau de calculs
            self.calculations_panel.set_client_data(client_data)
            # Auto-calcul si possible
            self.calculations_panel.auto_calculate_if_ready()
            self._update_status("Données client mises à jour")
        else:
            self.current_client = None
            self._update_status("Données client incomplètes")

    def _on_calculation_update(self, results: Optional[NutritionResults],
                              params: Optional[NutritionParams]):
        """
        Gestionnaire de mise à jour des calculs

        Args:
            results: Résultats des calculs nutritionnels
            params: Paramètres utilisés pour les calculs
        """
        self.current_results = results
        self.current_params = params

        # Mettre à jour l'affichage des résultats
        self.pdf_preview.update_results(results, params)

        if results:
            self._update_status(
                f"Calculs terminés - {int(results.calories_objectif)} kcal/jour"
            )
        else:
            self._update_status("Calculs effacés")

    def _generate_pdf(self) -> bool:
        """
        Génère le PDF de la fiche nutritionnelle

        Returns:
            True si succès, False sinon
        """
        if not self.current_client or not self.current_results or not self.current_params:
            self._show_error("Données incomplètes pour générer le PDF")
            return False

        try:
            self._update_status("Génération du PDF en cours...")

            # Génération du nom de fichier
            filename = self.pdf_generator.generate_filename(self.current_client)
            output_path = os.path.join("output", "fiches", filename)

            # Créer le dossier de sortie
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Génération des conseils personnalisés
            objectif_type = self.calculator.get_objectif_description(
                self.current_params.deficit_surplus_kcal
            )
            conseils = self.calculator.get_conseils_nutritionnels(
                self.current_client,
                self.current_results,
                objectif_type
            )

            # Paramètres pour le PDF
            params_dict = {
                'formule_metabolisme': self.current_params.formule_metabolisme,
                'facteur_activite': self.current_params.facteur_activite,
                'deficit_surplus_kcal': self.current_params.deficit_surplus_kcal,
                'proteines_g_par_kg': self.current_params.proteines_g_par_kg,
                'lipides_g_par_kg': self.current_params.lipides_g_par_kg
            }

            # Génération en thread pour ne pas bloquer l'interface
            def generate_in_thread():
                try:
                    self.pdf_generator.generate_premium_pdf(
                        self.current_client,
                        self.current_results,
                        params_dict,
                        output_path,
                        conseils
                    )

                    # Mise à jour de l'interface dans le thread principal
                    self.after(0, lambda: self._on_pdf_generated_success(filename))

                except Exception as e:
                    error_msg = str(e)
                    self.after(0, lambda: self._on_pdf_generated_error(error_msg))

            thread = threading.Thread(target=generate_in_thread)
            thread.daemon = True
            thread.start()

            return True

        except Exception as e:
            self._show_error(f"Erreur lors de la génération: {str(e)}")
            return False

    def _on_pdf_generated_success(self, filename: str):
        """Gestionnaire de succès de génération PDF"""
        self._update_status(f"PDF généré avec succès: {filename}")
        self._show_info(f"Fiche générée avec succès!\n\nFichier: {filename}")

    def _on_pdf_generated_error(self, error_message: str):
        """Gestionnaire d'erreur de génération PDF"""
        self._update_status("Erreur lors de la génération du PDF")
        self._show_error(f"Erreur lors de la génération du PDF:\n{error_message}")

    def _reset_all(self):
        """Remet à zéro tous les formulaires"""
        self.client_form.clear_form()
        self.calculations_panel._reset_values()
        self.pdf_preview.clear_results()
        self.current_client = None
        self.current_results = None
        self.current_params = None
        self._update_status("Formulaires réinitialisés")

    def _load_example_data(self):
        """Charge des données d'exemple pour les tests"""
        self.client_form.load_example_data()
        self._update_status("Données d'exemple chargées - Appuyez sur F5 pour recharger")

    def _save_as_template(self):
        """Sauvegarde les paramètres actuels comme modèle"""
        # Fonctionnalité future
        self._update_status("Fonctionnalité de sauvegarde à venir")

    def _show_help(self):
        """Affiche l'aide de l'application"""
        help_text = """🏋️ AIDE - Générateur de Fiches Nutritionnelles

📋 UTILISATION:
1. Remplissez les informations client (nom, âge, taille, poids)
2. Ajustez les paramètres nutritionnels selon les objectifs
3. Cliquez sur 'Calculer' pour voir les résultats
4. Cliquez sur 'Générer PDF' pour créer la fiche

⌨️ RACCOURCIS:
• Ctrl+R : Réinitialiser tous les formulaires
• F1 : Afficher cette aide
• F5 : Charger des données d'exemple

💡 CONSEILS:
• Les champs marqués * sont obligatoires
• Les macronutriments s'ajustent automatiquement selon l'objectif
• Les PDFs sont sauvegardés dans le dossier 'output/fiches'
"""
        self._show_info(help_text)

    def _update_status(self, message: str):
        """Met à jour la barre de statut"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_label.configure(text=f"[{timestamp}] {message}")

    def _show_error(self, message: str):
        """Affiche un message d'erreur"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Erreur")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()

        label = ctk.CTkLabel(dialog, text=message, wraplength=350)
        label.pack(pady=20, padx=20)

        button = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
        button.pack(pady=10)

        # Centrer la fenêtre
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

    def _show_info(self, message: str):
        """Affiche un message d'information"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Information")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()

        # Zone de texte scrollable pour long texte
        textbox = ctk.CTkTextbox(dialog, wrap="word")
        textbox.pack(fill="both", expand=True, padx=20, pady=20)
        textbox.insert("1.0", message)
        textbox.configure(state="disabled")

        button = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
        button.pack(pady=10)

        # Centrer la fenêtre
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

    def run(self):
        """Lance l'application"""
        self._update_status("Application démarrée - Prête à l'emploi")
        self.mainloop()