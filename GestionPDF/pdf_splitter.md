 Installation et utilisation

Installer la dépendance :

bashpip install PyPDF2

Utilisation simple :

bashpython pdf_splitter.py mon_document.pdf

Avec options :

bash# Découper en tranches de 10 Mo
python pdf_splitter.py mon_document.pdf -s 10

# Spécifier un dossier de sortie
python pdf_splitter.py mon_document.pdf -o ./dossier_sortie/

# Combiner les options
python pdf_splitter.py mon_document.pdf -s 15 -o ./resultat/
