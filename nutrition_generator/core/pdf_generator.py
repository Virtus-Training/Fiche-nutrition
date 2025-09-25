"""
Générateur PDF Premium - Niveau Coach Celebrity
Design professionnel digne d'un coach sportif reconnu avec +100k followers
"""

import os
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch, mm
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, FrameBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from .data_models import ClientData, NutritionResults, FicheMetadata
from .calculations import NutritionCalculator


class PremiumPDFGenerator:
    """Générateur PDF niveau Coach Celebrity - Design Premium"""

    def __init__(self, config_path: str = None):
        """
        Initialise le générateur PDF premium

        Args:
            config_path: Chemin vers le fichier de configuration
        """
        self.config = self._load_config(config_path)
        self.colors = self._define_premium_colors()
        self.styles = self._create_premium_styles()

        # Configuration matplotlib pour graphiques premium
        import matplotlib
        matplotlib.use('Agg')  # Backend non-interactif pour PDF

        try:
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            try:
                plt.style.use('seaborn-whitegrid')
            except:
                plt.style.use('default')

        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Arial', 'DejaVu Sans'],
            'font.size': 10,
            'axes.linewidth': 0.5,
            'grid.alpha': 0.3,
            'figure.max_open_warning': 0
        })

    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Charge la configuration coach"""
        # Essayer de charger depuis le fichier de config du projet
        if not config_path:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            config_path = os.path.join(project_root, "nutrition_generator", "config", "settings.json")

        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # S'assurer que coach_info existe
                if 'coach_info' not in config:
                    config['coach_info'] = {
                        "name": "Virtus Training",
                        "title": "Nutrition & Performance Coach",
                        "instagram": "virtus.training_",
                        "phone": "07 69 39 43 83",
                        "email": "virtustraining.fit@gmail.com",
                        "website": "www.virtus-training.fr"
                    }
                return config

        # Configuration par défaut Virtus Training si pas de fichier
        return {
            "coach_info": {
                "name": "Virtus Training",
                "title": "Nutrition & Performance Coach",
                "instagram": "virtus.training_",
                "phone": "07 69 39 43 83",
                "email": "virtustraining.fit@gmail.com",
                "website": "www.virtus-training.fr"
            }
        }

    def _define_premium_colors(self) -> Dict[str, Color]:
        """Palette de couleurs premium"""
        return {
            # Couleurs principales
            'primary': HexColor('#2E86AB'),      # Bleu moderne premium
            'accent_loss': HexColor('#F24236'),   # Rouge coral pour déficit
            'accent_gain': HexColor('#4CAF50'),   # Vert pour surplus
            'accent_maintain': HexColor('#FF9800'), # Orange pour maintenance

            # Couleurs neutres sophistiquées
            'dark_gray': HexColor('#2C3E50'),     # Gris foncé pour textes
            'medium_gray': HexColor('#6C757D'),   # Gris moyen
            'light_gray': HexColor('#E9ECEF'),    # Gris clair
            'background': HexColor('#FAFAFA'),    # Blanc cassé
            'card_bg': HexColor('#F8F9FA'),       # Fond des cartes

            # Couleurs pour graphiques
            'chart_protein': HexColor('#2E86AB'),  # Bleu pour protéines
            'chart_fat': HexColor('#F24236'),      # Rouge pour lipides
            'chart_carbs': HexColor('#4CAF50'),    # Vert pour glucides

            'white': white,
            'black': black
        }

    def _create_premium_styles(self) -> Dict[str, ParagraphStyle]:
        """Styles de paragraphe premium"""
        styles = getSampleStyleSheet()

        return {
            'MainTitle': ParagraphStyle(
                'MainTitle',
                parent=styles['Heading1'],
                fontSize=20,
                fontName='Helvetica-Bold',
                textColor=self.colors['primary'],
                alignment=TA_CENTER,
                spaceAfter=8,
                spaceBefore=0
            ),
            'Subtitle': ParagraphStyle(
                'Subtitle',
                parent=styles['Normal'],
                fontSize=12,
                fontName='Helvetica',
                textColor=self.colors['medium_gray'],
                alignment=TA_CENTER,
                spaceAfter=20
            ),
            'SectionTitle': ParagraphStyle(
                'SectionTitle',
                parent=styles['Heading2'],
                fontSize=16,
                fontName='Helvetica-Bold',
                textColor=self.colors['dark_gray'],
                spaceAfter=15,
                spaceBefore=20
            ),
            'CardTitle': ParagraphStyle(
                'CardTitle',
                parent=styles['Heading3'],
                fontSize=14,
                fontName='Helvetica-Bold',
                textColor=self.colors['primary'],
                spaceAfter=10
            ),
            'DataValue': ParagraphStyle(
                'DataValue',
                parent=styles['Normal'],
                fontSize=18,
                fontName='Helvetica-Bold',
                textColor=self.colors['primary'],
                alignment=TA_CENTER,
                spaceAfter=5
            ),
            'DataLabel': ParagraphStyle(
                'DataLabel',
                parent=styles['Normal'],
                fontSize=10,
                fontName='Helvetica',
                textColor=self.colors['medium_gray'],
                alignment=TA_CENTER
            ),
            'BodyText': ParagraphStyle(
                'BodyText',
                parent=styles['Normal'],
                fontSize=11,
                fontName='Helvetica',
                textColor=self.colors['dark_gray'],
                spaceAfter=8
            ),
            'BulletPoint': ParagraphStyle(
                'BulletPoint',
                parent=styles['Normal'],
                fontSize=11,
                fontName='Helvetica',
                textColor=self.colors['dark_gray'],
                leftIndent=20,
                bulletIndent=10,
                spaceAfter=6
            ),
            'Footer': ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                fontName='Helvetica',
                textColor=self.colors['medium_gray'],
                alignment=TA_CENTER
            )
        }

    def _create_premium_header(self) -> List:
        """Crée un en-tête premium avec logo et design sophistiqué"""
        elements = []

        # Header avec logo intégré - Chemins relatifs au projet
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        logo_paths = [
            os.path.join(project_root, "assets", "logo.png"),
            os.path.join(project_root, "Logo.png"),
            os.path.join(project_root, "logo.png")
        ]
        logo_element = None

        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                try:
                    logo_element = Image(logo_path, width=80, height=80)
                    logo_element.hAlign = 'LEFT'
                    break
                except Exception:
                    continue

        # Approche simplifiée : Logo séparé du tableau
        if logo_element:
            # D'abord le logo seul
            elements.append(logo_element)
            elements.append(Spacer(1, 10))

        # Informations coach
        coach_info = self.config['coach_info']

        # Header compact
        header_style = ParagraphStyle(
            'HeaderStyle',
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=self.colors['white'],
            alignment=TA_CENTER,
            spaceAfter=3
        )

        contact_style = ParagraphStyle(
            'ContactHeaderStyle',
            fontSize=8,
            fontName='Helvetica',
            textColor=self.colors['white'],
            alignment=TA_CENTER,
            spaceAfter=1
        )

        # Titre principal compact
        title_text = "<b>FICHE NUTRITIONNELLE PERSONNALISEE</b>"
        title_paragraph = Paragraph(title_text, header_style)

        # Contact compact
        contact_text = f"{coach_info['name']} | @{coach_info['instagram']} | {coach_info['phone']}"
        contact_paragraph = Paragraph(contact_text, contact_style)

        # Tableau simple pour le header compact
        header_data = [[title_paragraph], [contact_paragraph]]
        header_table = Table(header_data, colWidths=[17*cm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['primary']),
        ]))
        elements.append(header_table)

        # Message si pas de logo trouvé
        if not logo_element:
            no_logo_msg = Paragraph("(Logo Virtus Training non trouvé)", self.styles['BodyText'])
            elements.append(no_logo_msg)

        elements.append(Spacer(1, 8))

        return elements

    def _create_client_profile_card(self, client: ClientData, params: Dict) -> List:
        """Crée une carte profil client moderne"""
        elements = []

        # Titre de section avec symbole
        profile_title = "● PROFIL CLIENT"
        elements.append(Paragraph(profile_title, self.styles['SectionTitle']))

        # Déterminer l'objectif et sa couleur
        deficit_surplus = params.get('deficit_surplus_kcal', 0)
        if deficit_surplus < -100:
            objectif_text = "Perte de poids"
            objectif_color = self.colors['accent_loss']
        elif deficit_surplus > 100:
            objectif_text = "Prise de masse"
            objectif_color = self.colors['accent_gain']
        else:
            objectif_text = "Recomposition corporelle"
            objectif_color = self.colors['accent_maintain']

        # Description du niveau d'activité
        activite_descriptions = {
            1.2: "Sédentaire (bureau, pas d'exercice)",
            1.375: "Légèrement actif (1-3x/semaine)",
            1.55: "Modérément actif (3-5x/semaine)",
            1.725: "Très actif (6-7x/semaine)",
            1.9: "Extrêmement actif (quotidien + physique)"
        }

        facteur_activite = params.get('facteur_activite', 1.55)
        activite_desc = activite_descriptions.get(facteur_activite, "Niveau personnalisé")

        # Données du profil en tableau moderne
        profile_data = [
            ['NOM', f"{client.nom.upper()}", 'PRÉNOM', f"{client.prenom.title()}", 'ÂGE', f"{client.age} ans"],
            ['TAILLE', f"{client.taille_cm} cm", 'POIDS', f"{client.poids_kg} kg", 'SEXE', 'Homme' if client.sexe == 'male' else 'Femme'],
            ['ACTIVITÉ', activite_desc, '', '', '', ''],
            ['OBJECTIF', objectif_text, '', '', '', '']
        ]

        # Style du tableau profil compact
        profile_table = Table(profile_data, colWidths=[2.5*cm, 3*cm, 2.5*cm, 3*cm, 2*cm, 2*cm])
        profile_table.setStyle(TableStyle([
            # Style général
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['dark_gray']),

            # Labels en gras
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (4, 0), (4, -1), 'Helvetica-Bold'),

            # Couleur spéciale pour objectif
            ('TEXTCOLOR', (1, 3), (1, 3), objectif_color),
            ('FONTNAME', (1, 3), (1, 3), 'Helvetica-Bold'),

            # Borders et background
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['card_bg']),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['light_gray']),

            # Padding réduit
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),

            # Span pour activité et objectif
            ('SPAN', (1, 2), (5, 2)),  # Activité
            ('SPAN', (1, 3), (5, 3)),  # Objectif
        ]))

        elements.append(profile_table)
        elements.append(Spacer(1, 10))

        return elements

    def _create_caloric_needs_infographic(self, results: NutritionResults,
                                         params: Dict) -> List:
        """Crée une infographie des besoins caloriques"""
        elements = []

        # Titre de section compact avec symbole
        energy_title = "▲ BESOINS ÉNERGÉTIQUES"
        elements.append(Paragraph(energy_title, self.styles['SectionTitle']))
        elements.append(Spacer(1, 8))  # Espacement réduit

        deficit_surplus = params.get('deficit_surplus_kcal', 0)

        # Données pour les 3 cartes avec symboles
        cards_data = [
            ['• MÉTABOLISME', f"{int(results.bmr)}", 'kcal/jour', 'Énergie au repos'],
            ['• MAINTENANCE', f"{int(results.tdee)}", 'kcal/jour', 'Avec activité'],
            ['• OBJECTIF', f"{int(results.calories_objectif)}", 'kcal/jour', f"{deficit_surplus:+d} kcal"]
        ]

        # Couleur pour la carte objectif
        objectif_color = self.colors['accent_loss'] if deficit_surplus < 0 else \
                        self.colors['accent_gain'] if deficit_surplus > 0 else \
                        self.colors['accent_maintain']

        # Tableau des cartes énergétiques - Optimisé pour A4
        cards_table = Table(cards_data, colWidths=[5.3*cm, 5.3*cm, 5.3*cm])
        cards_table.setStyle(TableStyle([
            # Style général
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # Titres des cartes
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('TEXTCOLOR', (0, 0), (1, 0), self.colors['primary']),
            ('TEXTCOLOR', (2, 0), (2, 0), objectif_color),

            # Valeurs principales
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, 1), 18),
            ('TEXTCOLOR', (0, 1), (1, 1), self.colors['primary']),
            ('TEXTCOLOR', (2, 1), (2, 1), objectif_color),

            # Unités
            ('FONTSIZE', (0, 2), (-1, 2), 10),
            ('TEXTCOLOR', (0, 2), (-1, 2), self.colors['medium_gray']),

            # Descriptions
            ('FONTSIZE', (0, 3), (-1, 3), 9),
            ('TEXTCOLOR', (0, 3), (-1, 3), self.colors['medium_gray']),

            # Backgrounds des cartes
            ('BACKGROUND', (0, 0), (0, -1), self.colors['card_bg']),
            ('BACKGROUND', (1, 0), (1, -1), self.colors['card_bg']),
            ('BACKGROUND', (2, 0), (2, -1), self.colors['card_bg']),

            # Bordures
            ('GRID', (0, 0), (-1, -1), 1, self.colors['light_gray']),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),

            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))

        elements.append(cards_table)
        elements.append(Spacer(1, 8))

        return elements

    def _create_macronutrient_section(self, results: NutritionResults, client, params: Dict) -> List:
        """Crée la section macronutriments avec deux tableaux distincts"""
        elements = []

        # Titre de section avec symbole
        macro_title = "♦ RÉPARTITION DES MACRONUTRIMENTS"
        elements.append(Paragraph(macro_title, self.styles['SectionTitle']))

        # Calculer les macros de maintenance
        from .calculations import NutritionCalculator
        calculator = NutritionCalculator()

        # Créer les paramètres pour la maintenance
        maintenance_params = params.copy()
        maintenance_params['deficit_surplus_kcal'] = 0
        maintenance_calories = results.tdee

        # Recalculer les macros pour la maintenance
        from .data_models import NutritionParams
        nutrition_params = NutritionParams(
            formule_metabolisme=params.get('formule_metabolisme', 'mifflin_st_jeor'),
            facteur_activite=params.get('facteur_activite', 1.55),
            deficit_surplus_kcal=0,  # Pour maintenance
            proteines_g_par_kg=params.get('proteines_g_par_kg', 2.0),
            lipides_g_par_kg=params.get('lipides_g_par_kg', 1.0)
        )

        maintenance_proteines_g, maintenance_lipides_g, maintenance_glucides_g = calculator.calculate_macros(
            client, nutrition_params, maintenance_calories
        )

        # Calculer les pourcentages pour la maintenance
        maintenance_proteines_kcal = maintenance_proteines_g * 4
        maintenance_lipides_kcal = maintenance_lipides_g * 9
        maintenance_glucides_kcal = maintenance_glucides_g * 4
        maintenance_total_kcal = maintenance_proteines_kcal + maintenance_lipides_kcal + maintenance_glucides_kcal

        maintenance_pourcentages = {
            'proteines': (maintenance_proteines_kcal / maintenance_total_kcal) * 100,
            'lipides': (maintenance_lipides_kcal / maintenance_total_kcal) * 100,
            'glucides': (maintenance_glucides_kcal / maintenance_total_kcal) * 100
        }

        # Créer les deux tableaux côte à côte
        maintenance_table = self._create_compact_macro_table(
            "MAINTENANCE", maintenance_proteines_g, maintenance_lipides_g, maintenance_glucides_g,
            maintenance_proteines_kcal, maintenance_lipides_kcal, maintenance_glucides_kcal,
            maintenance_pourcentages, maintenance_calories
        )

        objectif_table = self._create_compact_macro_table(
            "OBJECTIF", results.proteines_g, results.lipides_g, results.glucides_g,
            results.proteines_kcal, results.lipides_kcal, results.glucides_kcal,
            results.macros_pourcentages, results.calories_objectif
        )

        # Créer une flèche entre les tableaux
        arrow_style = ParagraphStyle(
            'ArrowStyle',
            fontSize=24,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary'],
            alignment=TA_CENTER,
            spaceAfter=5,
            spaceBefore=5
        )
        arrow = Paragraph("➤", arrow_style)

        # Tableau combiné avec flèche - Autofit
        combined_data = [[maintenance_table, arrow, objectif_table]]
        combined_table = Table(combined_data, colWidths=[7*cm, 2*cm, 7*cm])
        combined_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # Centrer la flèche
        ]))

        elements.append(combined_table)
        elements.append(Spacer(1, 8))

        return elements

    def _create_premium_pie_chart(self, results: NutritionResults) -> Image:
        """Crée un graphique en secteurs premium"""
        # Configuration du graphique - Compact pour A4
        fig, ax = plt.subplots(figsize=(3.5, 3.5), facecolor='white')

        # Données
        labels = ['Protéines', 'Lipides', 'Glucides']
        sizes = [
            results.macros_pourcentages['proteines'],
            results.macros_pourcentages['lipides'],
            results.macros_pourcentages['glucides']
        ]
        colors = ['#2E86AB', '#F24236', '#4CAF50']

        # Création du pie chart premium
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=90,
            textprops={'fontsize': 10, 'fontweight': 'bold'},
            wedgeprops={'linewidth': 2, 'edgecolor': 'white'}
        )

        # Style premium
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)

        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')
            text.set_color('#2C3E50')

        # Titre du graphique
        ax.set_title('Répartition Calorique', fontsize=12, fontweight='bold',
                    color='#2C3E50', pad=20)

        # Suppression des axes
        ax.axis('equal')

        # Sauvegarde en mémoire
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none', pad_inches=0.1)
        buffer.seek(0)
        plt.close()

        return Image(buffer, width=6.5*cm, height=6.5*cm)  # Plus compact pour A4

    def _create_compact_macro_table(self, titre: str, proteines_g: float, lipides_g: float, glucides_g: float,
                                   proteines_kcal: float, lipides_kcal: float, glucides_kcal: float,
                                   pourcentages: Dict, total_kcal: float) -> Table:
        """Crée un tableau compact des macronutriments"""
        # Données du tableau compact
        table_data = [
            [titre, 'g', 'kcal', '%'],
            ['Protéines', f"{proteines_g:.0f}", f"{int(proteines_kcal)}", f"{pourcentages['proteines']:.0f}"],
            ['Lipides', f"{lipides_g:.0f}", f"{int(lipides_kcal)}", f"{pourcentages['lipides']:.0f}"],
            ['Glucides', f"{glucides_g:.0f}", f"{int(glucides_kcal)}", f"{pourcentages['glucides']:.0f}"],
            ['TOTAL', f"{proteines_g + lipides_g + glucides_g:.0f}", f"{int(total_kcal)}", "100"]
        ]

        # Configuration du tableau compact
        macro_table = Table(table_data, colWidths=[2.2*cm, 1.2*cm, 1.2*cm, 1.2*cm])
        macro_table.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.colors['white']),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

            # Corps du tableau
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 8),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('TEXTCOLOR', (0, 1), (-1, -2), self.colors['dark_gray']),

            # Ligne total
            ('BACKGROUND', (0, -1), (-1, -1), self.colors['card_bg']),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 8),
            ('TEXTCOLOR', (0, -1), (-1, -1), self.colors['primary']),

            # Bordures
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['light_gray']),
            ('LINEABOVE', (0, -1), (-1, -1), 1, self.colors['primary']),

            # Padding réduit
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))

        return macro_table

    def _create_weight_projection(self, client: ClientData,
                                 deficit_surplus: int) -> List:
        """Crée le graphique de projection de poids"""
        elements = []

        # Titre de section
        elements.append(Paragraph("EVOLUTION DE POIDS ESTIMEE", self.styles['SectionTitle']))

        # Calcul de la projection sur 12 semaines
        weeks = np.arange(0, 13)
        weight_loss_per_week = (deficit_surplus * 7) / 7700  # 1kg = 7700 kcal
        projected_weights = client.poids_kg + (weeks * weight_loss_per_week)

        # Création du graphique
        fig, ax = plt.subplots(figsize=(12, 4), facecolor='white')

        # Couleur selon l'objectif
        line_color = '#F24236' if deficit_surplus < 0 else '#4CAF50' if deficit_surplus > 0 else '#FF9800'
        fill_color = line_color + '20'  # Transparence

        # Ligne principale
        ax.plot(weeks, projected_weights, color=line_color, linewidth=3,
               marker='o', markersize=6, markerfacecolor=line_color,
               markeredgecolor='white', markeredgewidth=2)

        # Zone de confiance
        confidence = 0.5  # ±0.5kg de variabilité
        ax.fill_between(weeks, projected_weights - confidence,
                       projected_weights + confidence,
                       alpha=0.2, color=line_color)

        # Style du graphique
        ax.set_xlabel('Semaines', fontweight='bold', fontsize=11)
        ax.set_ylabel('Poids (kg)', fontweight='bold', fontsize=11)
        ax.set_title('Projection sur 12 semaines', fontweight='bold', fontsize=12, pad=15)

        # Grille subtile
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#FAFAFA')

        # Annotations des points clés
        ax.annotate(f'Départ: {client.poids_kg}kg',
                   xy=(0, client.poids_kg), xytext=(1, client.poids_kg + 1),
                   fontsize=9, fontweight='bold',
                   arrowprops=dict(arrowstyle='->', color=line_color))

        target_weight = projected_weights[-1]
        ax.annotate(f'Cible: {target_weight:.1f}kg',
                   xy=(12, target_weight), xytext=(10, target_weight + 1),
                   fontsize=9, fontweight='bold',
                   arrowprops=dict(arrowstyle='->', color=line_color))

        # Limites et ticks
        ax.set_xlim(0, 12)
        ax.set_xticks(range(0, 13, 2))

        plt.tight_layout()

        # Sauvegarde
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        plt.close()

        # Ajout du graphique
        graph_image = Image(buffer, width=16*cm, height=6*cm)
        elements.append(graph_image)

        # Résumé textuel
        weight_change = target_weight - client.poids_kg
        summary_text = f"<b>Poids actuel:</b> {client.poids_kg}kg → <b>Poids cible:</b> {target_weight:.1f}kg ({weight_change:+.1f}kg en 12 semaines)"
        elements.append(Paragraph(summary_text, self.styles['BodyText']))
        elements.append(Spacer(1, 20))

        return elements

    def _create_personalized_advice(self, client: ClientData, results: NutritionResults,
                                   objectif_type: str) -> List:
        """Crée la section conseils personnalisés compacte"""
        elements = []

        # Titre de section avec symbole
        advice_title = "► CONSEILS ESSENTIELS"
        elements.append(Paragraph(advice_title, self.styles['SectionTitle']))

        # Conseils en tableau compact avec symboles
        if objectif_type == "perte":
            conseils_data = [
                ['○ HYDRATATION', f"{results.hydratation_ml/1000:.1f}L/jour minimum"],
                ['○ RÉPARTITION', '3 repas + 1-2 collations légères'],
                ['○ FOCUS', 'Légumes + protéines à chaque repas'],
                ['○ ACTIVITÉ', 'Cardio 150min/semaine + musculation 2-3x']
            ]
        elif objectif_type == "prise":
            conseils_data = [
                ['○ HYDRATATION', f"{results.hydratation_ml/1000:.1f}L/jour minimum"],
                ['○ RÉPARTITION', '3 repas + 2-3 collations nutritives'],
                ['○ FOCUS', 'Bonnes graisses + glucides post-training'],
                ['○ ACTIVITÉ', 'Musculation intensive 3-4x/semaine']
            ]
        else:
            conseils_data = [
                ['○ HYDRATATION', f"{results.hydratation_ml/1000:.1f}L/jour minimum"],
                ['○ RÉPARTITION', '3 repas équilibrés + 1 collation'],
                ['○ FOCUS', 'Composition corporelle vs poids'],
                ['○ ACTIVITÉ', 'Training mixte force + conditionnement']
            ]

        conseils_table = Table(conseils_data, colWidths=[3*cm, 13*cm])
        conseils_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), self.colors['primary']),
            ('TEXTCOLOR', (1, 0), (1, -1), self.colors['dark_gray']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['light_gray']),
        ]))

        elements.append(conseils_table)
        elements.append(Spacer(1, 8))

        # Note importante compacte
        note_text = "<b>Important :</b> Adapter selon ressenti, consulter un medecin si pathologie, sommeil 7-9h/nuit."
        elements.append(Paragraph(note_text, self.styles['BodyText']))
        elements.append(Spacer(1, 10))

        return elements

    def _create_premium_footer(self) -> List:
        """Crée un pied de page premium avec signature coach"""
        elements = []

        # Ligne séparatrice élégante
        elements.append(Spacer(1, 15))

        # Informations de génération
        date_str = datetime.now().strftime("%d/%m/%Y")
        coach_name = self.config['coach_info']['name']

        footer_line1 = f"Fiche etablie le {date_str} par {coach_name} - Coaching Nutritionnel Professionnel"
        elements.append(Paragraph(footer_line1, self.styles['Footer']))

        # Contacts avec symboles ASCII
        coach_info = self.config['coach_info']
        contacts = f"Instagram: @{coach_info.get('instagram', '')} | Tel: {coach_info.get('phone', '')} | Email: {coach_info.get('email', '')}"
        elements.append(Paragraph(contacts, self.styles['Footer']))

        # Message professionnel
        message = "Cette fiche est personnalisée selon votre profil. Pour tout ajustement, contactez-moi."
        elements.append(Paragraph(message, self.styles['Footer']))

        return elements

    def _create_weight_prediction_chart(self, client: ClientData, results: NutritionResults,
                                       params_dict: Dict[str, Any]) -> List:
        """Crée un graphique de prédiction de variation de poids"""
        elements = []

        # Titre
        title_style = ParagraphStyle(
            'ChartTitle',
            fontSize=16,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary'],
            spaceAfter=15,
            alignment=TA_CENTER
        )
        elements.append(Paragraph("Prédiction de Variation de Poids", title_style))

        try:
            # Calcul de la variation prévue
            deficit_surplus = params_dict.get('deficit_surplus_kcal', 0)
            weeks = 12  # Prédiction sur 12 semaines

            # 1 kg de graisse = environ 7700 kcal
            weekly_weight_change = (deficit_surplus * 7) / 7700

            # Génération des données
            weeks_data = list(range(0, weeks + 1))
            weight_data = [client.poids_kg + (week * weekly_weight_change) for week in weeks_data]

            # Fermer toutes les figures existantes
            plt.close('all')

            # Configuration du graphique
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('white')

            # Couleur selon l'objectif
            if deficit_surplus < -50:
                color = '#F24236'  # Rouge pour perte
                objective = "Perte de poids"
            elif deficit_surplus > 50:
                color = '#4CAF50'  # Vert pour prise
                objective = "Prise de poids"
            else:
                color = '#FF9800'  # Orange pour maintenance
                objective = "Maintien du poids"

            ax.plot(weeks_data, weight_data, color=color, linewidth=3, marker='o', markersize=4)
            ax.fill_between(weeks_data, weight_data, alpha=0.3, color=color)

            ax.set_title(f'Évolution Prévue - {objective}', fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel('Semaines', fontsize=12)
            ax.set_ylabel('Poids (kg)', fontsize=12)
            ax.grid(True, alpha=0.3)

            # Annotation des points clés
            ax.annotate(f'Départ: {client.poids_kg:.1f} kg',
                       xy=(0, weight_data[0]), xytext=(1, weight_data[0] + 1),
                       arrowprops=dict(arrowstyle='->', color=color, alpha=0.7))

            ax.annotate(f'Objectif 12 sem: {weight_data[-1]:.1f} kg',
                       xy=(weeks, weight_data[-1]), xytext=(weeks-2, weight_data[-1] + 1),
                       arrowprops=dict(arrowstyle='->', color=color, alpha=0.7))

            plt.tight_layout()

            # Sauvegarde temporaire
            temp_file = BytesIO()
            plt.savefig(temp_file, format='png', dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            temp_file.seek(0)
            plt.close(fig)

            # Ajout au PDF
            img = Image(ImageReader(temp_file), width=14*cm, height=8*cm)
            img.hAlign = 'CENTER'
            elements.append(img)

        except Exception as e:
            # Message d'erreur si échec
            error_text = f"Erreur graphique poids: {str(e)}"
            elements.append(Paragraph(error_text, self.styles['BodyText']))

        elements.append(Spacer(1, 20))
        return elements

    def _create_macro_pie_charts(self, results: NutritionResults) -> List:
        """Crée les pie charts des macronutriments"""
        elements = []

        # Titre
        title_style = ParagraphStyle(
            'ChartTitle',
            fontSize=16,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary'],
            spaceAfter=15,
            alignment=TA_CENTER
        )
        elements.append(Paragraph("Répartition des Macronutriments", title_style))

        try:
            # Données pour le pie chart
            macros = results.macros_pourcentages
            labels = ['Protéines', 'Lipides', 'Glucides']
            sizes = [macros['proteines'], macros['lipides'], macros['glucides']]
            colors = ['#3498db', '#e74c3c', '#f39c12']

            # Fermer toutes les figures existantes
            plt.close('all')

            # Création du graphique
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            fig.patch.set_facecolor('white')

            # Pie chart en pourcentages
            wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                               startangle=90, textprops={'fontsize': 10})
            ax1.set_title('Répartition en %', fontsize=12, fontweight='bold')

            # Pie chart en grammes
            grams = [results.proteines_g, results.lipides_g, results.glucides_g]
            wedges2, texts2, autotexts2 = ax2.pie(grams, labels=[f'{label}\n{gram:.0f}g'
                                                                 for label, gram in zip(labels, grams)],
                                                  colors=colors, startangle=90,
                                                  textprops={'fontsize': 9})
            ax2.set_title('Quantités en grammes', fontsize=12, fontweight='bold')

            plt.tight_layout()

            # Sauvegarde temporaire
            temp_file = BytesIO()
            plt.savefig(temp_file, format='png', dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            temp_file.seek(0)
            plt.close(fig)

            # Ajout au PDF
            img = Image(ImageReader(temp_file), width=16*cm, height=8*cm)
            img.hAlign = 'CENTER'
            elements.append(img)

        except Exception as e:
            # Message d'erreur si échec
            error_text = f"Erreur pie charts: {str(e)}"
            elements.append(Paragraph(error_text, self.styles['BodyText']))

        elements.append(Spacer(1, 20))
        return elements

    def _create_colored_separator(self, color: Color = None) -> Drawing:
        """Crée un séparateur coloré décoratif"""
        if color is None:
            color = self.colors['primary']

        drawing = Drawing(16*cm, 0.5*cm)
        drawing.add(Rect(0, 0, 16*cm, 0.3*cm, fillColor=color, strokeColor=None))
        drawing.add(Circle(0.2*cm, 0.15*cm, 0.15*cm, fillColor=color, strokeColor=None))
        drawing.add(Circle(15.8*cm, 0.15*cm, 0.15*cm, fillColor=color, strokeColor=None))
        return drawing

    def _create_decorative_header_box(self) -> List:
        """Crée une boîte décorative pour l'en-tête"""
        elements = []

        # Ligne décorative colorée
        separator = self._create_colored_separator(self.colors['primary'])
        elements.append(separator)
        elements.append(Spacer(1, 5))

        return elements

    def generate_premium_pdf(self, client: ClientData, results: NutritionResults,
                           params_dict: Dict[str, Any], output_path: str,
                           conseils: List[str] = None) -> str:
        """
        Génère le PDF premium niveau Coach Celebrity

        Args:
            client: Données du client
            results: Résultats des calculs nutritionnels
            params_dict: Paramètres utilisés pour les calculs
            output_path: Chemin de sortie du PDF
            conseils: Liste de conseils personnalisés

        Returns:
            Chemin du fichier PDF généré
        """
        try:
            # Configuration du document premium - Optimisé A4
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=25,
                leftMargin=25,
                topMargin=30,
                bottomMargin=30,
                title="Fiche Nutritionnelle Premium"
            )

            # Construction du contenu premium
            story = []

            # En-tête premium
            story.extend(self._create_premium_header())
            story.extend(self._create_decorative_header_box())

            # Profil client moderne
            story.extend(self._create_client_profile_card(client, params_dict))

            # Besoins caloriques infographiques
            story.extend(self._create_caloric_needs_infographic(results, params_dict))
            story.append(self._create_colored_separator(self.colors['accent_maintain']))
            story.append(Spacer(1, 10))

            # Macronutriments avec deux tableaux et pie charts
            story.extend(self._create_macronutrient_section(results, client, params_dict))
            story.append(self._create_colored_separator(self.colors['primary']))
            story.append(Spacer(1, 10))

            # Page break pour recto verso
            story.append(PageBreak())

            # Graphique de variation de poids estimée (page 2)
            story.extend(self._create_weight_prediction_chart(client, results, params_dict))

            # Pie charts des macronutriments
            story.extend(self._create_macro_pie_charts(results))

            # Conseils personnalisés
            calculator = NutritionCalculator()
            objectif_type = calculator.get_objectif_description(params_dict.get('deficit_surplus_kcal', 0))
            story.extend(self._create_personalized_advice(client, results, objectif_type))

            # Pied de page premium
            story.extend(self._create_premium_footer())

            # Construction du PDF
            doc.build(story)

            return output_path

        except Exception as e:
            raise Exception(f"Erreur lors de la génération du PDF premium: {str(e)}")

    def generate_filename(self, client: ClientData) -> str:
        """Génère un nom de fichier standardisé"""
        date_str = datetime.now().strftime("%Y%m%d")
        prenom_clean = "".join(c for c in client.prenom if c.isalnum())
        nom_clean = "".join(c for c in client.nom if c.isalnum())
        return f"Fiche_Premium_{prenom_clean}_{nom_clean}_{date_str}.pdf"


# Alias pour compatibilité
PDFGenerator = PremiumPDFGenerator