"""
Composant de prévisualisation et gestion des fichiers PDF générés
"""

import os
import subprocess
import platform
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
import customtkinter as ctk
from ...core.data_models import FicheMetadata


class PDFPreview(ctk.CTkFrame):
    """Composant pour afficher les résultats et gérer les PDFs générés"""

    def __init__(self, parent, on_generate_pdf: Optional[Callable] = None, **kwargs):
        """
        Initialise le composant de prévisualisation

        Args:
            parent: Widget parent
            on_generate_pdf: Callback pour générer un PDF
        """
        super().__init__(parent, **kwargs)

        self.on_generate_pdf = on_generate_pdf
        self.output_directory = "output/fiches"
        self.current_results = None
        self.current_params = None

        self._setup_ui()
        self._load_existing_pdfs()

    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        # Section résultats
        self.results_label = ctk.CTkLabel(
            self,
            text="RÉSUMÉ DES CALCULS",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#2c3e50"
        )
        self.results_label.grid(row=0, column=0, columnspan=2, pady=(10, 12), sticky="w")

        # Zone de texte pour les résultats
        self.results_text = ctk.CTkTextbox(
            self,
            height=200,
            wrap="word",
            font=ctk.CTkFont(size=11),
            fg_color="white",
            border_color="#bdc3c7",
            border_width=1
        )
        self.results_text.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        # Bouton de génération PDF
        self.generate_button = ctk.CTkButton(
            self,
            text="Générer PDF",
            command=self._on_generate_pdf,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            corner_radius=6
        )
        self.generate_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Section fiches créées
        self.fiches_label = ctk.CTkLabel(
            self,
            text="FICHES CRÉÉES",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2c3e50"
        )
        self.fiches_label.grid(row=3, column=0, columnspan=2, pady=(0, 8), sticky="w")

        # Zone scrollable pour les fiches
        self.fiches_frame = ctk.CTkScrollableFrame(
            self,
            height=180,
            label_text="Historique des fiches générées",
            fg_color="white",
            border_color="#bdc3c7",
            border_width=1
        )
        self.fiches_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.fiches_frame.grid_columnconfigure(0, weight=1)

        # Boutons de gestion
        self.management_frame = ctk.CTkFrame(self)
        self.management_frame.grid(row=5, column=0, columnspan=2, sticky="ew")
        self.management_frame.grid_columnconfigure((0, 1), weight=1)

        self.open_folder_button = ctk.CTkButton(
            self.management_frame,
            text="Ouvrir dossier",
            command=self._open_output_folder,
            fg_color="#3498db",
            hover_color="#2980b9",
            corner_radius=4,
            height=32
        )
        self.open_folder_button.grid(row=0, column=0, padx=(0, 5), pady=8, sticky="ew")

        self.refresh_button = ctk.CTkButton(
            self.management_frame,
            text="Actualiser",
            command=self._refresh_pdf_list,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            corner_radius=4,
            height=32
        )
        self.refresh_button.grid(row=0, column=1, padx=(5, 0), pady=8, sticky="ew")

        # Configuration des colonnes
        self.grid_columnconfigure(1, weight=1)

        # Initialisation
        self._update_results_display()

    def _update_results_display(self):
        """Met à jour l'affichage des résultats"""
        self.results_text.delete("1.0", "end")

        if not self.current_results:
            self.results_text.insert("1.0", "Aucun calcul effectué.\n\nVeuillez remplir les informations client et cliquer sur 'Calculer'.")
            self.generate_button.configure(state="disabled")
            return

        # Formatage des résultats
        results_text = self._format_results()
        self.results_text.insert("1.0", results_text)
        self.generate_button.configure(state="normal")

    def _format_results(self) -> str:
        """
        Formate les résultats pour l'affichage

        Returns:
            Texte formaté des résultats
        """
        if not self.current_results:
            return ""

        r = self.current_results
        deficit_surplus = 0
        if self.current_params:
            deficit_surplus = self.current_params.deficit_surplus_kcal

        # Détermination de l'objectif
        if deficit_surplus < -100:
            objectif = "Perte de poids"
            emoji = "🔥"
        elif deficit_surplus > 100:
            objectif = "Prise de masse"
            emoji = "💪"
        else:
            objectif = "Recomposition corporelle"
            emoji = "⚖️"

        text = f"""{emoji} OBJECTIF: {objectif}

📊 BESOINS ÉNERGÉTIQUES:
• Métabolisme de base: {int(r.bmr)} kcal/jour
• Dépense totale (TDEE): {int(r.tdee)} kcal/jour
• Calories objectif: {int(r.calories_objectif)} kcal/jour
• Déficit/Surplus: {deficit_surplus:+d} kcal/jour

🥩 MACRONUTRIMENTS:
• Protéines: {r.proteines_g:.1f}g ({int(r.proteines_kcal)} kcal) - {r.macros_pourcentages['proteines']}%
• Lipides: {r.lipides_g:.1f}g ({int(r.lipides_kcal)} kcal) - {r.macros_pourcentages['lipides']}%
• Glucides: {r.glucides_g:.1f}g ({int(r.glucides_kcal)} kcal) - {r.macros_pourcentages['glucides']}%

💧 HYDRATATION:
• Besoin quotidien: {int(r.hydratation_ml)} ml/jour
• Équivalent: {int(r.hydratation_ml/250)} verres de 250ml

✅ Prêt pour la génération PDF!"""

        return text

    def _on_generate_pdf(self):
        """Gestionnaire de génération PDF"""
        if self.on_generate_pdf and self.current_results:
            success = self.on_generate_pdf()
            if success:
                self._refresh_pdf_list()

    def _load_existing_pdfs(self):
        """Charge la liste des PDFs existants"""
        # Créer le dossier de sortie s'il n'existe pas
        os.makedirs(self.output_directory, exist_ok=True)
        self._refresh_pdf_list()

    def _refresh_pdf_list(self):
        """Actualise la liste des PDFs"""
        # Effacer les anciens widgets
        for widget in self.fiches_frame.winfo_children():
            widget.destroy()

        # Lister les fichiers PDF
        try:
            pdf_files = [f for f in os.listdir(self.output_directory) if f.endswith('.pdf')]
            pdf_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.output_directory, x)), reverse=True)

            if not pdf_files:
                no_files_label = ctk.CTkLabel(
                    self.fiches_frame,
                    text="Aucune fiche générée",
                    text_color="gray"
                )
                no_files_label.grid(row=0, column=0, pady=20)
                return

            # Afficher chaque fichier
            for i, filename in enumerate(pdf_files):
                self._create_pdf_item(filename, i)

        except FileNotFoundError:
            os.makedirs(self.output_directory, exist_ok=True)

    def _create_pdf_item(self, filename: str, row: int):
        """
        Crée un élément d'affichage pour un fichier PDF

        Args:
            filename: Nom du fichier
            row: Ligne dans la grille
        """
        # Frame pour l'élément
        item_frame = ctk.CTkFrame(self.fiches_frame)
        item_frame.grid(row=row, column=0, sticky="ew", pady=2, padx=5)
        item_frame.grid_columnconfigure(0, weight=1)

        # Informations du fichier
        filepath = os.path.join(self.output_directory, filename)
        file_stats = os.stat(filepath)
        modification_time = datetime.fromtimestamp(file_stats.st_mtime)

        # Extraction des informations du nom de fichier
        try:
            # Format: Fiche_Prénom_Nom_AAAAMMJJ.pdf
            parts = filename.replace('.pdf', '').split('_')
            if len(parts) >= 4:
                prenom = parts[1]
                nom = parts[2]
                date_str = parts[3]
                client_name = f"{prenom} {nom}"
            else:
                client_name = filename.replace('.pdf', '')
        except:
            client_name = filename.replace('.pdf', '')

        # Label d'information
        info_text = f"📄 {client_name}\n📅 {modification_time.strftime('%d/%m/%Y %H:%M')}"
        info_label = ctk.CTkLabel(
            item_frame,
            text=info_text,
            font=ctk.CTkFont(size=10),
            justify="left"
        )
        info_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Boutons d'action
        buttons_frame = ctk.CTkFrame(item_frame)
        buttons_frame.grid(row=0, column=1, padx=10, pady=5)

        open_button = ctk.CTkButton(
            buttons_frame,
            text="Ouvrir",
            width=60,
            height=25,
            font=ctk.CTkFont(size=10),
            command=lambda f=filename: self._open_pdf(f)
        )
        open_button.pack(side="left", padx=2)

        delete_button = ctk.CTkButton(
            buttons_frame,
            text="Suppr",
            width=50,
            height=25,
            font=ctk.CTkFont(size=10),
            fg_color="red",
            hover_color="darkred",
            command=lambda f=filename: self._delete_pdf(f)
        )
        delete_button.pack(side="left", padx=2)

    def _open_pdf(self, filename: str):
        """
        Ouvre un fichier PDF avec l'application par défaut

        Args:
            filename: Nom du fichier à ouvrir
        """
        filepath = os.path.join(self.output_directory, filename)
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', filepath])
            elif platform.system() == 'Windows':  # Windows
                os.startfile(filepath)
            else:  # Linux
                subprocess.call(['xdg-open', filepath])
        except Exception as e:
            print(f"Erreur lors de l'ouverture du PDF: {e}")

    def _delete_pdf(self, filename: str):
        """
        Supprime un fichier PDF après confirmation

        Args:
            filename: Nom du fichier à supprimer
        """
        # Boîte de dialogue de confirmation
        result = ctk.CTkInputDialog(
            text=f"Voulez-vous vraiment supprimer '{filename}'?\nTapez 'OUI' pour confirmer:",
            title="Confirmation de suppression"
        )

        if result.get_input() == "OUI":
            try:
                filepath = os.path.join(self.output_directory, filename)
                os.remove(filepath)
                self._refresh_pdf_list()
            except Exception as e:
                print(f"Erreur lors de la suppression: {e}")

    def _open_output_folder(self):
        """Ouvre le dossier de sortie des PDFs"""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', self.output_directory])
            elif platform.system() == 'Windows':  # Windows
                os.startfile(self.output_directory)
            else:  # Linux
                subprocess.call(['xdg-open', self.output_directory])
        except Exception as e:
            print(f"Erreur lors de l'ouverture du dossier: {e}")

    def update_results(self, results: Optional[Any], params: Optional[Any]):
        """
        Met à jour les résultats affichés

        Args:
            results: Résultats des calculs nutritionnels
            params: Paramètres utilisés pour les calculs
        """
        self.current_results = results
        self.current_params = params
        self._update_results_display()

    def clear_results(self):
        """Efface les résultats affichés"""
        self.current_results = None
        self.current_params = None
        self._update_results_display()