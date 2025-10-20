# Installation et utilisation

- Installer la dépendance :

```` python
      pip install PyPDF2
````
- Utilisation simple :

```` python
       python pdf_splitter.py mon_document.pdf
````
- Avec options :

```` python
# Découper en tranches de 10 Mo
      python pdf_splitter.py mon_document.pdf -s 10
````
# Spécifier un dossier de sortie
```` python
python pdf_splitter.py mon_document.pdf -o ./dossier_sortie/
````

# Combiner les options
```` python
python pdf_splitter.py mon_document.pdf -s 15 -o ./resultat/
````
