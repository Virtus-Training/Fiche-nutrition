# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a complete Python application for generating professional nutrition fact sheets (fiches nutritionnelles) for fitness coaches. The application uses CustomTkinter for the GUI and ReportLab for PDF generation.

## Architecture

### Technology Stack
- **Python 3.8+** - Core language
- **CustomTkinter** - Modern GUI framework
- **ReportLab** - PDF generation
- **Matplotlib** - Charts and graphs
- **Pillow** - Image processing

### Project Structure
```
nutrition_generator/          # Main application package
├── main.py                  # Application entry point
├── gui/                     # User interface components
│   ├── main_window.py       # Main application window
│   ├── components/          # Reusable GUI components
│   │   ├── client_form.py   # Client data input form
│   │   ├── calculations_panel.py # Nutrition calculations
│   │   └── pdf_preview.py   # PDF management and preview
│   └── theme.json          # UI theme configuration
├── core/                    # Business logic
│   ├── calculations.py      # Nutrition calculation algorithms
│   ├── pdf_generator.py     # PDF creation and formatting
│   └── data_models.py       # Data structures and validation
├── config/                  # Application configuration
│   └── settings.json        # App settings and coach info
└── assets/                  # Static resources
    └── icons/              # Application icons
```

## Common Development Commands

### Running the application
```bash
python main.py
```

### Installing dependencies
```bash
pip install -r requirements.txt
```

### Debug mode
```bash
python main.py --debug
```

### Testing with sample data
Press `F5` in the running application to load example data.

## Key Components

### Data Models (`core/data_models.py`)
- `ClientData`: Personal client information with validation
- `NutritionParams`: Nutritional parameters and objectives
- `NutritionResults`: Calculated nutritional requirements
- `FicheMetadata`: PDF file metadata for tracking

### Calculations (`core/calculations.py`)
- Multiple BMR formulas: Harris-Benedict, Mifflin-St Jeor, Katch-McArdle
- TDEE calculations with activity factors
- Macronutrient distribution algorithms
- Hydration requirements calculation

### PDF Generation (`core/pdf_generator.py`)
- Professional PDF layout with branding
- Embedded charts using Matplotlib
- Customizable coach information
- Multi-section document structure

### GUI Components
- **ClientForm**: Input validation for personal data
- **CalculationsPanel**: Parameter adjustment with real-time updates
- **PDFPreview**: Results display and PDF management
- **MainWindow**: Application coordination and event handling

## Configuration

### Coach Information
Edit `nutrition_generator/config/settings.json` to customize:
- Coach name and contact details
- Default nutritional parameters
- PDF formatting settings

### UI Theming
Modify `nutrition_generator/gui/theme.json` for:
- Color schemes
- Font configurations
- Component styling

## Development Guidelines

### Code Style
- French language for user-facing text and comments
- English for technical variables and functions
- Type hints for all function parameters and returns
- Comprehensive docstrings for classes and methods

### Error Handling
- Comprehensive input validation in data models
- User-friendly error messages in GUI
- Detailed logging for debugging
- Graceful degradation for missing dependencies

### Testing
- Use F5 shortcut to load test data
- Enable debug mode for detailed error traces
- Check logs/ directory for application logs
- Validate PDF output in output/fiches/ directory

## File Naming Conventions
- Generated PDFs: `Fiche_Prénom_Nom_AAAAMMJJ.pdf`
- Log files: `nutrition_app_AAAAMMJJ.log`
- Configuration files: JSON format with UTF-8 encoding

## Common Issues and Solutions

### Missing Dependencies
Ensure all packages in requirements.txt are installed. The application checks dependencies on startup.

### PDF Generation Errors
- Verify output/fiches/ directory exists and is writable
- Check that all input data is validated before PDF generation
- Review matplotlib backend compatibility

### GUI Layout Issues
- Minimum window size: 1000x700
- Uses responsive grid layout
- Test on different screen resolutions

## Extension Points

The application is designed for easy extension:
- Add new BMR formulas in `MetabolismCalculator`
- Extend PDF sections in `PDFGenerator`
- Create new GUI components in `gui/components/`
- Add configuration options in settings.json

## Production Deployment

For distribution:
1. Ensure all dependencies are included
2. Test on target operating system
3. Consider PyInstaller for executable creation
4. Include sample configuration files
5. Provide user documentation