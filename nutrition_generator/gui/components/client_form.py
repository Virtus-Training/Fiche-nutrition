"""
Composant de formulaire client pour la saisie des données personnelles
"""

import customtkinter as ctk
from typing import Dict, Callable, Optional
from ...core.data_models import ClientData


class ClientForm(ctk.CTkFrame):
    """Formulaire de saisie des données client"""

    def __init__(self, parent, on_data_change: Optional[Callable] = None, **kwargs):
        """
        Initialise le formulaire client

        Args:
            parent: Widget parent
            on_data_change: Callback appelé lors du changement de données
        """
        super().__init__(parent, **kwargs)

        self.on_data_change = on_data_change
        self._setup_ui()
        self._bind_events()

    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        # Titre de la section
        self.title_label = ctk.CTkLabel(
            self,
            text="INFORMATIONS CLIENT",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#2c3e50"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="w")

        # Nom (obligatoire)
        self.nom_label = ctk.CTkLabel(
            self,
            text="Nom *",
            font=ctk.CTkFont(size=12)
        )
        self.nom_label.grid(row=1, column=0, sticky="w", pady=(0, 5))

        self.nom_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nom de famille",
            fg_color="white",
            border_color="#bdc3c7"
        )
        self.nom_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        # Prénom (obligatoire)
        self.prenom_label = ctk.CTkLabel(
            self,
            text="Prénom *",
            font=ctk.CTkFont(size=12)
        )
        self.prenom_label.grid(row=3, column=0, sticky="w", pady=(0, 5))

        self.prenom_entry = ctk.CTkEntry(
            self,
            placeholder_text="Prénom",
            fg_color="white",
            border_color="#bdc3c7"
        )
        self.prenom_entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        # Âge
        self.age_label = ctk.CTkLabel(
            self,
            text="Âge (années)",
            font=ctk.CTkFont(size=12)
        )
        self.age_label.grid(row=5, column=0, sticky="w", pady=(0, 5))

        self.age_entry = ctk.CTkEntry(
            self,
            placeholder_text="25",
            fg_color="white",
            border_color="#bdc3c7"
        )
        self.age_entry.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        # Sexe
        self.sexe_label = ctk.CTkLabel(
            self,
            text="Sexe",
            font=ctk.CTkFont(size=12)
        )
        self.sexe_label.grid(row=7, column=0, sticky="w", pady=(0, 5))

        self.sexe_var = ctk.StringVar(value="male")
        self.sexe_frame = ctk.CTkFrame(
            self,
            fg_color="#f8f9fa",
            border_color="#bdc3c7",
            border_width=1
        )
        self.sexe_frame.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        self.sexe_male = ctk.CTkRadioButton(
            self.sexe_frame,
            text="Homme",
            variable=self.sexe_var,
            value="male",
            fg_color="#3498db"
        )
        self.sexe_male.pack(side="left", padx=12, pady=8)

        self.sexe_female = ctk.CTkRadioButton(
            self.sexe_frame,
            text="Femme",
            variable=self.sexe_var,
            value="female",
            fg_color="#3498db"
        )
        self.sexe_female.pack(side="left", padx=12, pady=8)

        # Taille
        self.taille_label = ctk.CTkLabel(
            self,
            text="Taille (cm)",
            font=ctk.CTkFont(size=12)
        )
        self.taille_label.grid(row=9, column=0, sticky="w", pady=(0, 5))

        self.taille_entry = ctk.CTkEntry(
            self,
            placeholder_text="175",
            fg_color="white",
            border_color="#bdc3c7"
        )
        self.taille_entry.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        # Poids
        self.poids_label = ctk.CTkLabel(
            self,
            text="Poids (kg)",
            font=ctk.CTkFont(size=12)
        )
        self.poids_label.grid(row=11, column=0, sticky="w", pady=(0, 5))

        self.poids_entry = ctk.CTkEntry(
            self,
            placeholder_text="70.5",
            fg_color="white",
            border_color="#bdc3c7"
        )
        self.poids_entry.grid(row=12, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        # Pourcentage de graisse (optionnel)
        self.graisse_label = ctk.CTkLabel(
            self,
            text="% Graisse corporelle (optionnel)",
            font=ctk.CTkFont(size=12)
        )
        self.graisse_label.grid(row=13, column=0, sticky="w", pady=(0, 5))

        self.graisse_entry = ctk.CTkEntry(
            self,
            placeholder_text="15.0",
            fg_color="white",
            border_color="#bdc3c7"
        )
        self.graisse_entry.grid(row=14, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Message de validation
        self.validation_label = ctk.CTkLabel(
            self,
            text="",
            text_color="red",
            font=ctk.CTkFont(size=10)
        )
        self.validation_label.grid(row=15, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Configuration des colonnes
        self.grid_columnconfigure(1, weight=1)

    def _bind_events(self):
        """Lie les événements de validation"""
        entries = [
            self.nom_entry, self.prenom_entry, self.age_entry,
            self.taille_entry, self.poids_entry, self.graisse_entry
        ]

        for entry in entries:
            entry.bind("<KeyRelease>", self._on_entry_change)

        self.sexe_var.trace("w", self._on_sexe_change)

    def _on_entry_change(self, event=None):
        """Gestionnaire de changement dans les champs de saisie"""
        self._validate_and_notify()

    def _on_sexe_change(self, *args):
        """Gestionnaire de changement du sexe"""
        self._validate_and_notify()

    def _validate_and_notify(self):
        """Valide les données et notifie les changements"""
        validation_errors = self._validate_data()

        if validation_errors:
            self.validation_label.configure(text=validation_errors[0])
        else:
            self.validation_label.configure(text="")

        # Notifier le parent du changement
        if self.on_data_change:
            self.on_data_change()

    def _validate_data(self) -> list:
        """
        Valide les données saisies

        Returns:
            Liste des erreurs de validation
        """
        errors = []

        # Vérification des champs obligatoires
        if not self.nom_entry.get().strip():
            errors.append("Le nom est obligatoire")
            return errors

        if not self.prenom_entry.get().strip():
            errors.append("Le prénom est obligatoire")
            return errors

        # Validation de l'âge
        try:
            age = int(self.age_entry.get())
            if age < 10 or age > 100:
                errors.append("L'âge doit être entre 10 et 100 ans")
        except ValueError:
            if self.age_entry.get().strip():
                errors.append("L'âge doit être un nombre entier")

        # Validation de la taille
        try:
            taille = int(self.taille_entry.get())
            if taille < 100 or taille > 250:
                errors.append("La taille doit être entre 100 et 250 cm")
        except ValueError:
            if self.taille_entry.get().strip():
                errors.append("La taille doit être un nombre entier")

        # Validation du poids
        try:
            poids = float(self.poids_entry.get())
            if poids < 30 or poids > 300:
                errors.append("Le poids doit être entre 30 et 300 kg")
        except ValueError:
            if self.poids_entry.get().strip():
                errors.append("Le poids doit être un nombre")

        # Validation du pourcentage de graisse (optionnel)
        if self.graisse_entry.get().strip():
            try:
                graisse = float(self.graisse_entry.get())
                if graisse < 3 or graisse > 50:
                    errors.append("Le % de graisse doit être entre 3 et 50%")
            except ValueError:
                errors.append("Le % de graisse doit être un nombre")

        return errors

    def get_client_data(self) -> Optional[ClientData]:
        """
        Récupère les données client du formulaire

        Returns:
            ClientData si valide, None sinon
        """
        validation_errors = self._validate_data()
        if validation_errors:
            return None

        try:
            # Récupération du pourcentage de graisse (optionnel)
            pourcentage_graisse = None
            if self.graisse_entry.get().strip():
                pourcentage_graisse = float(self.graisse_entry.get())

            return ClientData(
                nom=self.nom_entry.get().strip(),
                prenom=self.prenom_entry.get().strip(),
                age=int(self.age_entry.get()),
                taille_cm=int(self.taille_entry.get()),
                poids_kg=float(self.poids_entry.get()),
                sexe=self.sexe_var.get(),
                pourcentage_graisse=pourcentage_graisse
            )
        except (ValueError, TypeError):
            return None

    def is_valid(self) -> bool:
        """
        Vérifie si les données du formulaire sont valides

        Returns:
            True si valide, False sinon
        """
        return len(self._validate_data()) == 0

    def clear_form(self):
        """Efface tous les champs du formulaire"""
        self.nom_entry.delete(0, "end")
        self.prenom_entry.delete(0, "end")
        self.age_entry.delete(0, "end")
        self.taille_entry.delete(0, "end")
        self.poids_entry.delete(0, "end")
        self.graisse_entry.delete(0, "end")
        self.sexe_var.set("male")
        self.validation_label.configure(text="")

    def load_example_data(self):
        """Charge des données d'exemple pour les tests"""
        self.nom_entry.delete(0, "end")
        self.nom_entry.insert(0, "Dupont")

        self.prenom_entry.delete(0, "end")
        self.prenom_entry.insert(0, "Marie")

        self.age_entry.delete(0, "end")
        self.age_entry.insert(0, "28")

        self.taille_entry.delete(0, "end")
        self.taille_entry.insert(0, "165")

        self.poids_entry.delete(0, "end")
        self.poids_entry.insert(0, "60.0")

        self.sexe_var.set("female")

        self._validate_and_notify()