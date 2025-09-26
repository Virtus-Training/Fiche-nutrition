"""
Panneau de calculs nutritionnels avec paramètres et résultats
"""

import customtkinter as ctk
from typing import Dict, Callable, Optional
from core.data_models import (
    ClientData, NutritionParams, NutritionResults,
    FORMULES_METABOLISME, NIVEAUX_ACTIVITE
)
from core.calculations import NutritionCalculator


class CalculationsPanel(ctk.CTkFrame):
    """Panneau pour les paramètres nutritionnels et calculs"""

    def __init__(self, parent, on_calculation_update: Optional[Callable] = None, **kwargs):
        """
        Initialise le panneau de calculs

        Args:
            parent: Widget parent
            on_calculation_update: Callback appelé lors de mise à jour des calculs
        """
        super().__init__(parent, **kwargs)

        self.on_calculation_update = on_calculation_update
        self.calculator = NutritionCalculator()
        self.current_results: Optional[NutritionResults] = None

        self._setup_ui()
        self._setup_defaults()
        self._bind_events()

    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        # Configuration du scrollable frame principal
        self.main_scroll = ctk.CTkScrollableFrame(self)
        self.main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        self.main_scroll.grid_columnconfigure(0, weight=1)

        # Titre de la section
        self.title_label = ctk.CTkLabel(
            self.main_scroll,
            text="PARAMÈTRES NUTRITIONNELS",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#2c3e50"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="w")

        # Formule de métabolisme
        self.formule_label = ctk.CTkLabel(
            self.main_scroll,
            text="Formule de métabolisme",
            font=ctk.CTkFont(size=12)
        )
        self.formule_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 5))

        formule_options = list(FORMULES_METABOLISME.values())
        self.formule_combo = ctk.CTkComboBox(
            self.main_scroll,
            values=formule_options,
            state="readonly",
            fg_color="white",
            border_color="#bdc3c7",
            button_color="#3498db"
        )
        self.formule_combo.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        # Niveau d'activité
        self.activite_label = ctk.CTkLabel(
            self.main_scroll,
            text="Niveau d'activité",
            font=ctk.CTkFont(size=12)
        )
        self.activite_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 5))

        self.activite_frame = ctk.CTkFrame(
            self.main_scroll,
            fg_color="#f8f9fa",
            border_color="#bdc3c7",
            border_width=1
        )
        self.activite_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.activite_frame.grid_columnconfigure(0, weight=1)

        # Slider pour le niveau d'activité
        self.activite_slider = ctk.CTkSlider(
            self.activite_frame,
            from_=1.2,
            to=2.0,
            number_of_steps=4,
            progress_color="#3498db",
            button_color="#2980b9"
        )
        self.activite_slider.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 5))

        # Label dynamique pour le niveau d'activité
        self.activite_desc_label = ctk.CTkLabel(
            self.activite_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="#2c3e50"
        )
        self.activite_desc_label.grid(row=1, column=0, padx=10, pady=(0, 8))

        # Objectif (déficit/surplus)
        self.objectif_label = ctk.CTkLabel(
            self.main_scroll,
            text="Objectif calorique",
            font=ctk.CTkFont(size=12)
        )
        self.objectif_label.grid(row=5, column=0, columnspan=2, sticky="w", pady=(0, 5))

        self.objectif_frame = ctk.CTkFrame(
            self.main_scroll,
            fg_color="#f8f9fa",
            border_color="#bdc3c7",
            border_width=1
        )
        self.objectif_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.objectif_frame.grid_columnconfigure(0, weight=1)

        # Slider pour l'objectif
        self.objectif_slider = ctk.CTkSlider(
            self.objectif_frame,
            from_=-500,
            to=500,
            number_of_steps=20,
            progress_color="#95a5a6",
            button_color="#7f8c8d"
        )
        self.objectif_slider.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 5))

        # Label dynamique pour l'objectif
        self.objectif_desc_label = ctk.CTkLabel(
            self.objectif_frame,
            text="",
            font=ctk.CTkFont(size=10)
        )
        self.objectif_desc_label.grid(row=1, column=0, padx=10, pady=(0, 8))

        # Macronutriments
        self.macros_label = ctk.CTkLabel(
            self.main_scroll,
            text="MACRONUTRIMENTS",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2c3e50"
        )
        self.macros_label.grid(row=7, column=0, columnspan=2, pady=(15, 10), sticky="w")

        # Protéines
        self.proteines_label = ctk.CTkLabel(
            self.main_scroll,
            text="Protéines (g/kg)",
            font=ctk.CTkFont(size=12)
        )
        self.proteines_label.grid(row=8, column=0, sticky="w", pady=(0, 5))

        self.proteines_entry = ctk.CTkEntry(
            self.main_scroll,
            placeholder_text="1.8",
            fg_color="white",
            border_color="#bdc3c7"
        )
        self.proteines_entry.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Lipides
        self.lipides_label = ctk.CTkLabel(
            self.main_scroll,
            text="Lipides (g/kg)",
            font=ctk.CTkFont(size=12)
        )
        self.lipides_label.grid(row=10, column=0, sticky="w", pady=(0, 5))

        self.lipides_entry = ctk.CTkEntry(
            self.main_scroll,
            placeholder_text="1.0",
            fg_color="white",
            border_color="#bdc3c7"
        )
        self.lipides_entry.grid(row=11, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Boutons d'action
        self.buttons_frame = ctk.CTkFrame(
            self.main_scroll,
            fg_color="transparent"
        )
        self.buttons_frame.grid(row=12, column=0, columnspan=2, sticky="ew", pady=(20, 10))
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)

        self.calculate_button = ctk.CTkButton(
            self.buttons_frame,
            text="Calculer",
            command=self._calculate_nutrition,
            font=ctk.CTkFont(weight="bold", size=13),
            height=36,
            fg_color="#3498db",
            hover_color="#2980b9",
            corner_radius=6
        )
        self.calculate_button.grid(row=0, column=0, padx=(0, 8), pady=8, sticky="ew")

        self.reset_button = ctk.CTkButton(
            self.buttons_frame,
            text="Réinitialiser",
            command=self._reset_values,
            font=ctk.CTkFont(weight="bold", size=13),
            height=36,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            corner_radius=6
        )
        self.reset_button.grid(row=0, column=1, padx=(8, 0), pady=8, sticky="ew")

        # Configuration des colonnes du scroll frame
        self.main_scroll.grid_columnconfigure(0, weight=1)
        self.main_scroll.grid_columnconfigure(1, weight=1)

    def _setup_defaults(self):
        """Configure les valeurs par défaut"""
        # Formule par défaut (Mifflin-St Jeor)
        self.formule_combo.set(FORMULES_METABOLISME["mifflin_st_jeor"])

        # Activité par défaut (modérément actif)
        self.activite_slider.set(1.55)

        # Objectif par défaut (maintenance)
        self.objectif_slider.set(0)

        # Macros par défaut
        self.proteines_entry.insert(0, "1.8")
        self.lipides_entry.insert(0, "1.0")

        # Mise à jour des labels
        self._update_activite_description()
        self._update_objectif_description()

    def _bind_events(self):
        """Lie les événements"""
        self.activite_slider.configure(command=self._on_activite_change)
        self.objectif_slider.configure(command=self._on_objectif_change)

        # Événements des entries
        self.proteines_entry.bind("<KeyRelease>", self._on_entry_change)
        self.lipides_entry.bind("<KeyRelease>", self._on_entry_change)

    def _on_activite_change(self, value):
        """Gestionnaire de changement du niveau d'activité"""
        self._update_activite_description()

    def _on_objectif_change(self, value):
        """Gestionnaire de changement de l'objectif"""
        self._update_objectif_description()

    def _on_entry_change(self, event=None):
        """Gestionnaire de changement dans les entries"""
        pass  # Validation en temps réel si nécessaire

    def _update_activite_description(self):
        """Met à jour la description du niveau d'activité"""
        value = self.activite_slider.get()

        # Trouver la description correspondante
        for factor, description in NIVEAUX_ACTIVITE.items():
            if abs(value - factor) < 0.1:
                self.activite_desc_label.configure(
                    text=f"{factor} - {description}"
                )
                return

        # Valeur intermédiaire
        self.activite_desc_label.configure(
            text=f"{value:.2f} - Niveau intermédiaire"
        )

    def _update_objectif_description(self):
        """Met à jour la description de l'objectif"""
        value = int(self.objectif_slider.get())

        if value < -100:
            color = "red"
            description = f"Perte de poids ({value:+d} kcal/jour)"
        elif value > 100:
            color = "green"
            description = f"Prise de masse ({value:+d} kcal/jour)"
        else:
            color = "gray"
            description = f"Recomposition ({value:+d} kcal/jour)"

        self.objectif_desc_label.configure(
            text=description,
            text_color=color
        )

    def _get_formule_key(self) -> str:
        """Récupère la clé de la formule sélectionnée"""
        selected_value = self.formule_combo.get()
        for key, value in FORMULES_METABOLISME.items():
            if value == selected_value:
                return key
        return "mifflin_st_jeor"  # Par défaut

    def _validate_macros(self) -> tuple:
        """
        Valide les valeurs des macronutriments

        Returns:
            Tuple (proteines, lipides, errors)
        """
        errors = []

        try:
            proteines = float(self.proteines_entry.get())
            if proteines < 0.5 or proteines > 4.0:
                errors.append("Protéines: 0.5-4.0 g/kg")
        except ValueError:
            errors.append("Protéines: valeur invalide")
            proteines = 1.8

        try:
            lipides = float(self.lipides_entry.get())
            if lipides < 0.3 or lipides > 2.0:
                errors.append("Lipides: 0.3-2.0 g/kg")
        except ValueError:
            errors.append("Lipides: valeur invalide")
            lipides = 1.0

        return proteines, lipides, errors

    def _calculate_nutrition(self, client_data: ClientData = None):
        """Calcule les besoins nutritionnels"""
        if not hasattr(self, '_current_client') or self._current_client is None:
            return

        # Validation des macros
        proteines, lipides, errors = self._validate_macros()
        if errors:
            # Afficher les erreurs
            return

        try:
            # Création des paramètres nutritionnels
            params = NutritionParams(
                formule_metabolisme=self._get_formule_key(),
                facteur_activite=self.activite_slider.get(),
                deficit_surplus_kcal=int(self.objectif_slider.get()),
                proteines_g_par_kg=proteines,
                lipides_g_par_kg=lipides
            )

            # Calcul des résultats
            self.current_results = self.calculator.calculate_complete_nutrition(
                self._current_client, params
            )

            # Notifier le parent
            if self.on_calculation_update:
                self.on_calculation_update(self.current_results, params)

        except Exception as e:
            print(f"Erreur de calcul: {e}")

    def _reset_values(self):
        """Remet les valeurs par défaut"""
        self._setup_defaults()
        self.current_results = None

        if self.on_calculation_update:
            self.on_calculation_update(None, None)

    def set_client_data(self, client_data: ClientData):
        """
        Met à jour les données client pour les calculs

        Args:
            client_data: Données du client
        """
        self._current_client = client_data

        # Suggestions automatiques basées sur l'objectif
        self._update_macro_suggestions()

    def _update_macro_suggestions(self):
        """Met à jour les suggestions de macronutriments"""
        if not hasattr(self, '_current_client') or self._current_client is None:
            return

        objectif_value = int(self.objectif_slider.get())

        # Suggestions selon l'objectif
        if objectif_value < -200:  # Perte de poids
            proteines_suggestion = 2.2
            lipides_suggestion = 0.8
        elif objectif_value > 200:  # Prise de masse
            proteines_suggestion = 1.6
            lipides_suggestion = 1.2
        else:  # Maintenance/recomposition
            proteines_suggestion = 1.8
            lipides_suggestion = 1.0

        # Mise à jour des placeholders
        self.proteines_entry.configure(placeholder_text=f"{proteines_suggestion}")
        self.lipides_entry.configure(placeholder_text=f"{lipides_suggestion}")

    def get_current_params(self) -> Optional[NutritionParams]:
        """
        Récupère les paramètres nutritionnels actuels

        Returns:
            NutritionParams si valide, None sinon
        """
        proteines, lipides, errors = self._validate_macros()
        if errors:
            return None

        try:
            return NutritionParams(
                formule_metabolisme=self._get_formule_key(),
                facteur_activite=self.activite_slider.get(),
                deficit_surplus_kcal=int(self.objectif_slider.get()),
                proteines_g_par_kg=proteines,
                lipides_g_par_kg=lipides
            )
        except Exception:
            return None

    def auto_calculate_if_ready(self):
        """Calcule automatiquement si les données sont prêtes"""
        if hasattr(self, '_current_client') and self._current_client is not None:
            self._calculate_nutrition()