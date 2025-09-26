# Prompt amélioration header et icônes - PDF professionnel

## 🎯 MISSION : Moderniser le header et remplacer tous les carrés colorés par des icônes

Le PDF nécessite un header personnalisé avec le nom du client et l'intégration d'icônes professionnelles pour remplacer tous les symboles ■ actuels.

## 🔧 MODIFICATIONS PRIORITAIRES

### 1. **HEADER PERSONNALISÉ** ⭐
```python
def create_personalized_header(client_data):
    """Header avec nom du client au lieu de 'Coaching Professionnel'"""
    
    # Coordonnées simplifiées
    contact_style = ParagraphStyle(
        name='ContactStyle',
        fontSize=8,
        fontName='Helvetica',
        textColor=colors.white,
        alignment=2,
        leading=9
    )
    
    contact_text = """
    @virtus.training_<br/>
    07 69 39 43 83<br/>
    virtustraining.fit@gmail.com
    """
    
    # Titre personnalisé avec nom du client
    title_style = ParagraphStyle(
        name='PersonalizedTitle',
        fontSize=15,
        fontName='Helvetica-Bold',
        textColor=colors.white,
        alignment=1,
        leading=17
    )
    
    personalized_title = f"""
    <b>FICHE NUTRITIONNELLE<br/>
    PERSONNALISÉE<br/>
    {client_data['first_name']} {client_data['last_name']}</b>
    """
    
    # Structure header
    header_data = [
        [
            create_logo_cell(),
            Paragraph(personalized_title, title_style),
            Paragraph(contact_text, contact_style)
        ]
    ]
    
    header_table = Table(header_data, colWidths=[60, 360, 160])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2E86AB')),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    return header_table
```

### 2. **LISTE COMPLÈTE DES ICÔNES À INTÉGRER** ⭐

#### **Contact et réseaux sociaux :**
- `instagram.png` - Pour remplacer les mentions Instagram
- `email.png` - Pour les adresses email
- `phone.png` - Pour les numéros de téléphone
- `website.png` - Pour les sites web (si ajouté)

#### **Profil et données personnelles :**
- `user.png` - Pour la section "Profil Personnel"
- `scale.png` - Pour le poids et IMC
- `ruler.png` - Pour la taille
- `calendar.png` - Pour l'âge et durée
- `activity.png` - Pour le niveau d'activité
- `target.png` - Pour les objectifs

#### **Nutrition et macronutriments :**
- `nutrition.png` - Pour la section "Macronutriments"
- `protein.png` - Pour les protéines (peut être une icône viande/œuf)
- `fat.png` - Pour les lipides (icône avocat/huile)
- `carbs.png` - Pour les glucides (icône pain/céréales)
- `plate.png` - Pour la répartition des repas
- `apple.png` - Pour les conseils nutritionnels généraux

#### **Hydratation et timing :**
- `water.png` - Pour l'hydratation
- `clock.png` - Pour le timing des repas
- `glass.png` - Pour les quantités d'eau spécifiques

#### **Énergie et métabolisme :**
- `energy.png` - Pour les besoins énergétiques
- `fire.png` - Pour le métabolisme de base
- `battery.png` - Pour la maintenance énergétique
- `bullseye.png` - Pour l'objectif calorique

#### **Conseils et attention :**
- `lightbulb.png` - Pour les conseils personnalisés
- `warning.png` - Pour les points d'attention
- `checkmark.png` - Pour les recommandations positives
- `sleep.png` - Pour les conseils de sommeil

#### **Évolution et suivi :**
- `chart.png` - Pour l'évolution du poids
- `trending-up.png` ou `trending-down.png` - Selon l'objectif
- `progress.png` - Pour le suivi général

### 3. **PIE CHART 600 DPI** ⭐
```python
def create_ultra_high_resolution_pie_chart():
    """Pie chart 600 DPI pour qualité maximale"""
    
    fig, ax = plt.subplots(figsize=(7, 7), dpi=600)  # 600 DPI !!!
    
    # Données
    values = [calculations['protein_kcal'], calculations['fat_kcal'], calculations['carb_kcal']]
    labels = ['Protéines', 'Lipides', 'Glucides']
    colors_modern = ['#2E86AB', '#E74C3C', '#27AE60']
    
    # PIE CHART ULTRA HAUTE RÉSOLUTION
    wedges, texts, autotexts = ax.pie(
        values, 
        labels=labels, 
        colors=colors_modern,
        autopct='%1.1f%%',
        startangle=90,
        explode=(0.03, 0.03, 0.03),
        shadow=False,
        textprops={'fontsize': 14, 'fontweight': 'bold'},  # Texte encore plus gros
        wedgeprops={'linewidth': 3, 'edgecolor': 'white'}   # Bordures plus épaisses
    )
    
    # Style premium
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(13)
    
    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')
        text.set_color('#2C3E50')
    
    ax.set_title('Répartition calorique', 
                fontsize=16, fontweight='bold', 
                pad=25, color='#2C3E50')
    
    ax.axis('equal')
    plt.tight_layout()
    
    # Sauvegarder avec 600 DPI
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=600, bbox_inches='tight', 
                facecolor='white', edgecolor='none', 
                transparent=False, optimize=True)
    img_buffer.seek(0)
    plt.close()
    
    from reportlab.platypus import Image
    from reportlab.lib.utils import ImageReader
    img = Image(ImageReader(img_buffer), width=200, height=200)  # Taille augmentée
    
    return img
```

### 4. **INTÉGRATION DES ICÔNES DANS LE PDF** ⭐
```python
def create_icon_paragraph(icon_name, text, style):
    """Créer un paragraphe avec icône + texte"""
    
    # Chemin vers les icônes
    icon_path = os.path.join("assets", "icons", icon_name)
    
    if os.path.exists(icon_path):
        # Créer une table avec icône + texte
        icon_img = Image(icon_path, width=12, height=12)
        
        content = [[icon_img, Paragraph(text, style)]]
        icon_table = Table(content, colWidths=[15, 400])
        icon_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        return icon_table
    else:
        # Fallback si icône manquante
        return Paragraph(f"• {text}", style)

# Remplacer tous les ■ par des icônes appropriées
def create_section_title_with_icon(icon_name, title_text):
    """Titre de section avec icône"""
    return create_icon_paragraph(icon_name, f"<b>{title_text}</b>", section_style)

# Exemples d'utilisation :
story.append(create_section_title_with_icon("user.png", "PROFIL PERSONNEL"))
story.append(create_section_title_with_icon("energy.png", "BESOINS ÉNERGÉTIQUES"))
story.append(create_section_title_with_icon("nutrition.png", "MACRONUTRIMENTS"))
story.append(create_section_title_with_icon("chart.png", "ÉVOLUTION DU POIDS (12 SEMAINES)"))
story.append(create_section_title_with_icon("lightbulb.png", "CONSEILS PERSONNALISÉS"))
```

### 5. **CONSEILS AVEC ICÔNES** ⭐
```python
def create_conseils_with_icons():
    """Conseils avec icônes au lieu de carrés colorés"""
    
    conseils_sections = [
        {
            'icon': 'water.png',
            'title': 'HYDRATATION',
            'content': '→ 2,6 L d\'eau par jour (2600 ml)<br/>→ Ajoutez 250 ml avant/après entrainement',
            'border_color': '#2E86AB',
            'bg_color': '#E3F2FD'
        },
        {
            'icon': 'clock.png',
            'title': 'TIMING DES REPAS', 
            'content': '→ Gardez 60% de vos glucides autour de vos séances<br/>→ Petit-déjeuner riche en protéines',
            'border_color': '#F39C12',
            'bg_color': '#FFF3E0'
        },
        {
            'icon': 'target.png',
            'title': 'SPÉCIFIQUE À VOTRE OBJECTIF',
            'content': '→ Déficit contrôlé : -300 kcal/j<br/>→ Protéines : 96,0 g/j<br/>→ 2/3 assiette = légumes',
            'border_color': '#27AE60',
            'bg_color': '#E8F5E8'
        },
        {
            'icon': 'warning.png',
            'title': 'POINTS D\'ATTENTION',
            'content': '→ Aliments frais privilégiés<br/>→ Sommeil 7h minimum<br/>→ Consulter médecin si besoin',
            'border_color': '#E74C3C',
            'bg_color': '#FFEBEE'
        }
    ]
    
    conseils_story = []
    
    for conseil in conseils_sections:
        # Titre avec icône
        titre_avec_icone = create_icon_paragraph(
            conseil['icon'], 
            f"<b>{conseil['title']}</b>", 
            conseil_title_style
        )
        
        conseil_data = [
            [titre_avec_icone],
            [Paragraph(conseil['content'], conseil_content_style)]
        ]
        
        conseil_box = Table(conseil_data, colWidths=[500])
        conseil_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(conseil['bg_color'])),
            ('BORDER', (0, 0), (-1, -1), 2, colors.HexColor(conseil['border_color'])),
            ('LINEABOVE', (0, 0), (-1, 0), 4, colors.HexColor(conseil['border_color'])),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        conseils_story.append(conseil_box)
        conseils_story.append(Spacer(1, 8))
    
    return conseils_story
```

### 6. **CARDS ÉNERGÉTIQUES AVEC ICÔNES** ⭐
```python
def create_energy_cards_with_icons():
    """Cards énergétiques avec icônes spécifiques"""
    
    cards_data = [
        {
            'icon': 'fire.png',
            'title': 'MÉTABOLISME DE BASE',
            'value': '1330',
            'unit': 'kcal / jour',
            'hint': 'Mifflin-St Jeor',
            'border_color': '#6C757D'
        },
        {
            'icon': 'battery.png',
            'title': 'MAINTENANCE',
            'value': '2128', 
            'unit': 'kcal / jour',
            'hint': 'BMR x 1.60 activité',
            'border_color': '#2E86AB'
        },
        {
            'icon': 'bullseye.png',
            'title': 'OBJECTIF',
            'value': '1828',
            'unit': 'kcal / jour', 
            'hint': 'Variation de -300 kcal',
            'border_color': '#E74C3C'
        }
    ]
    
    cards = []
    for card in cards_data:
        # Titre avec icône
        title_with_icon = create_icon_paragraph(
            card['icon'], 
            f"<b>{card['title']}</b>", 
            card_title_style
        )
        
        card_content = [
            [title_with_icon],
            [Paragraph(f"<b>{card['value']}</b>", create_card_value_style(card['border_color']))],
            [Paragraph(card['unit'], create_card_unit_style())],
            [Paragraph(card['hint'], create_card_hint_style())]
        ]
        
        card_table = Table(card_content, colWidths=[160], rowHeights=[30, 40, 18, 30])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAFAFA')),
            ('BORDER', (0, 0), (-1, -1), 3, colors.HexColor(card['border_color'])),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEABOVE', (0, 0), (-1, 0), 6, colors.HexColor(card['border_color'])),
        ]))
        
        cards.append(card_table)
    
    return Table([cards], colWidths=[170, 170, 170])
```

## 📂 STRUCTURE DES ICÔNES REQUISE

Créer le dossier `assets/icons/` avec toutes les icônes PNG (24x24px recommandé) :

```
assets/
└── icons/
    ├── instagram.png
    ├── email.png
    ├── phone.png
    ├── user.png
    ├── scale.png
    ├── ruler.png
    ├── calendar.png
    ├── activity.png
    ├── target.png
    ├── nutrition.png
    ├── protein.png
    ├── fat.png
    ├── carbs.png
    ├── plate.png
    ├── water.png
    ├── clock.png
    ├── glass.png
    ├── energy.png
    ├── fire.png
    ├── battery.png
    ├── bullseye.png
    ├── lightbulb.png
    ├── warning.png
    ├── checkmark.png
    ├── sleep.png
    ├── chart.png
    ├── trending-down.png
    └── apple.png
```

## 🎯 RÉSULTAT ATTENDU

Un PDF **ultra-professionnel** avec :
- ✅ Header personnalisé avec nom du client
- ✅ Pie chart 600 DPI pour netteté parfaite
- ✅ Toutes les icônes remplacent les carrés colorés
- ✅ Navigation visuelle intuitive
- ✅ Cohérence graphique totale
- ✅ Niveau premium reconnaissable

**Le PDF doit avoir l'apparence d'un document créé par un designer professionnel !**