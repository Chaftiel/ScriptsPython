# Extracteur de Texte PDF

Un outil simple et efficace pour extraire le texte de fichiers PDF avec une interface graphique intuitive.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Méthodes d'extraction](#méthodes-dextraction)
- [Dépannage](#dépannage)
- [FAQ](#faq)

## Fonctionnalités

- **Interface graphique** intuitive et moderne
- **Extraction de texte** depuis n'importe quel PDF
- **Deux méthodes d'extraction** au choix (PyPDF et PDFPlumber)
- **Barre de progression** en temps réel
- **Sauvegarde** automatique du texte extrait
- **Prévisualisation** du texte dans l'application
- **Traitement multithreading** (interface reste réactive)

## Prérequis

- **Python 3.7 ou supérieur**
- **tkinter** (généralement inclus avec Python)
- Système d'exploitation : Windows, macOS, ou Linux

### Vérifier votre version de Python

```bash
python --version
# ou
python3 --version
```

Si Python n'est pas installé, téléchargez-le depuis [python.org](https://www.python.org/downloads/)

## Installation

### Option 1 : Installation rapide (recommandée)

#### Sur Windows

```bash
# Installer les dépendances
pip install pypdf pdfplumber

# Lancer l'application
python pdf_extractor_gui.py
```

#### Sur macOS

```bash
# Installer les dépendances
pip3 install pypdf pdfplumber

# Lancer l'application
python3 pdf_extractor_gui.py
```

#### Sur Linux (Ubuntu, Debian, etc.)

```bash
# Sur les systèmes Linux récents (Ubuntu 23+, Debian 12+)
pip install pypdf pdfplumber --break-system-packages

# Lancer l'application
python3 pdf_extractor_gui.py
```

### Option 2 : Installation avec environnement virtuel (recommandée pour les développeurs)

Cette méthode isole les dépendances du projet et évite les conflits.

#### Sur Windows

```bash
# Créer un environnement virtuel
python -m venv env

# Activer l'environnement
env\Scripts\activate

# Installer les dépendances
pip install pypdf pdfplumber

# Lancer l'application
python pdf_extractor_gui.py
```

#### Sur macOS / Linux

```bash
# Créer un environnement virtuel
python3 -m venv env

# Activer l'environnement
source env/bin/activate

# Installer les dépendances
pip install pypdf pdfplumber

# Lancer l'application
python3 pdf_extractor_gui.py
```

### Option 3 : Script en ligne de commande

Si vous préférez utiliser le script sans interface graphique :

```bash
# Installation identique aux options précédentes

# Utilisation du script CLI
python extract_pdf_text.py document.pdf
python extract_pdf_text.py document.pdf -o output.txt
python extract_pdf_text.py document.pdf --method pdfplumber
```

## Utilisation

### Interface graphique

1. **Lancer l'application**
   ```bash
   python pdf_extractor_gui.py
   ```

2. **Sélectionner un fichier PDF**
   - Cliquez sur le bouton "Parcourir..." dans la section "Fichier PDF"
   - Choisissez votre fichier PDF

3. **Choisir la méthode d'extraction** (optionnel)
   - **Automatique** : laisse le programme choisir la meilleure méthode (recommandé)
   - **PyPDF** : extraction rapide, idéale pour les PDF simples
   - **PDFPlumber** : extraction précise, meilleure pour les PDF complexes

4. **Définir le fichier de sortie** (optionnel)
   - Par défaut, le fichier sera nommé `[nom_pdf]_text.txt`
   - Vous pouvez modifier l'emplacement avec "Choisir..."

5. **Extraire le texte**
   - Cliquez sur "Extraire le texte"
   - Suivez la progression dans la barre
   - Le texte apparaîtra dans la zone de texte

6. **Sauvegarder**
   - Cliquez sur "Sauvegarder" pour enregistrer le texte extrait
   - Ou modifiez le texte avant de sauvegarder

### Script en ligne de commande

```bash
# Utilisation basique
python extract_pdf_text.py document.pdf

# Spécifier le fichier de sortie
python extract_pdf_text.py document.pdf -o resultat.txt

# Choisir la méthode d'extraction
python extract_pdf_text.py document.pdf --method pypdf
python extract_pdf_text.py document.pdf --method pdfplumber

# Afficher l'aide
python extract_pdf_text.py --help
```

## Méthodes d'extraction

### PyPDF
- **Rapide** : traitement très rapide
- **Léger** : peu de dépendances
- **Idéal pour** : documents textuels simples
- **Limitations** : peut avoir des problèmes avec les mises en page complexes

### PDFPlumber
- **Précis** : meilleure préservation de la mise en page
- **Robuste** : gère bien les PDF complexes
- **Idéal pour** : documents avec tableaux, colonnes multiples
- **Limitations** : légèrement plus lent que PyPDF

### Mode Automatique
- Essaie PDFPlumber en premier (meilleure qualité)
- Bascule vers PyPDF si PDFPlumber n'est pas disponible
- **Recommandé** pour la plupart des utilisateurs

## Dépannage

### Erreur : "externally-managed-environment"

**Problème** : Sur Linux récent, pip refuse d'installer les paquets.

**Solution 1** : Utiliser le flag `--break-system-packages`
```bash
pip install pypdf pdfplumber --break-system-packages
```

**Solution 2** : Utiliser un environnement virtuel (recommandé)
```bash
python3 -m venv env
source env/bin/activate
pip install pypdf pdfplumber
```

### Erreur : "No module named 'tkinter'"

**Problème** : tkinter n'est pas installé.

**Solution sur Ubuntu/Debian** :
```bash
sudo apt-get install python3-tk
```

**Solution sur Fedora/RHEL** :
```bash
sudo dnf install python3-tkinter
```

**Solution sur macOS** :
tkinter est normalement inclus. Si absent, réinstallez Python depuis [python.org](https://www.python.org)

### Erreur : "ModuleNotFoundError: No module named 'pypdf'"

**Problème** : Les dépendances ne sont pas installées.

**Solution** :
```bash
pip install pypdf pdfplumber
```

Si vous utilisez un environnement virtuel, assurez-vous qu'il est activé :
```bash
# Linux/macOS
source env/bin/activate

# Windows
env\Scripts\activate
```

### Le texte extrait est vide ou incomplet

**Causes possibles** :
1. Le PDF est scanné (image) et non textuel
2. Le PDF est protégé ou crypté
3. Le PDF utilise un encodage non standard

**Solutions** :
- Pour les PDF scannés, utilisez un logiciel OCR (reconnaissance optique de caractères)
- Essayez l'autre méthode d'extraction (PyPDF vs PDFPlumber)
- Vérifiez que le PDF n'est pas protégé

### L'interface graphique ne s'affiche pas correctement

**Solution** :
```bash
# Mettre à jour tkinter
pip install --upgrade tk

# Sur Linux, installer les paquets nécessaires
sudo apt-get install python3-tk python3-pil python3-pil.imagetk
```

## FAQ

### Puis-je extraire du texte de PDF scannés ?

Non, cet outil extrait uniquement le texte déjà présent dans le PDF. Pour les PDF scannés (images), vous aurez besoin d'un logiciel OCR comme :
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Adobe Acrobat avec OCR
- Des services en ligne comme SmallPDF

### Le programme fonctionne-t-il hors ligne ?

Oui, une fois les dépendances installées, le programme fonctionne entièrement hors ligne.

### Puis-je traiter plusieurs PDF en même temps ?

La version actuelle traite un PDF à la fois. Pour traiter plusieurs fichiers, lancez le programme plusieurs fois ou utilisez le script CLI dans une boucle :

```bash
for file in *.pdf; do
    python extract_pdf_text.py "$file"
done
```

### Les données de mon PDF sont-elles sécurisées ?

Oui, tout le traitement se fait localement sur votre ordinateur. Aucune donnée n'est envoyée sur internet.

### Quelle est la taille maximale de PDF supportée ?

Il n'y a pas de limite stricte, mais les très gros fichiers (>100 Mo) peuvent prendre du temps à traiter et consommer beaucoup de mémoire.

### Puis-je modifier le code ?

Oui, le code est open source. Vous êtes libre de le modifier selon vos besoins.

## Exemples d'utilisation

### Exemple 1 : Extraction simple
```bash
python pdf_extractor_gui.py
# 1. Sélectionnez votre PDF
# 2. Cliquez sur "Extraire le texte"
# 3. Cliquez sur "Sauvegarder"
```

### Exemple 2 : Extraction en ligne de commande avec options
```bash
# Extraire avec PDFPlumber et sauvegarder dans un dossier spécifique
python extract_pdf_text.py rapport.pdf --method pdfplumber -o ~/Documents/rapport_extrait.txt
```

### Exemple 3 : Traiter tous les PDF d'un dossier (Bash/Linux)
```bash
for pdf in *.pdf; do
    python extract_pdf_text.py "$pdf" --method auto
    echo "Traité: $pdf"
done
```

### Exemple 4 : Traiter tous les PDF d'un dossier (PowerShell/Windows)
```powershell
Get-ChildItem *.pdf | ForEach-Object {
    python extract_pdf_text.py $_.FullName --method auto
    Write-Host "Traité: $($_.Name)"
}
```

## Structure des fichiers

```
.
├── pdf_extractor_gui.py      # Interface graphique (recommandé)
├── extract_pdf_text.py        # Script en ligne de commande
└── README.md                  # Ce fichier
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Soumettre des pull requests

## Support

Si vous rencontrez des problèmes :
1. Consultez la section [Dépannage](#dépannage)
2. Vérifiez la [FAQ](#faq)
3. Ouvrez une issue sur GitHub (si applicable)

## Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le distribuer.

---

**Bon extraction de texte !**
