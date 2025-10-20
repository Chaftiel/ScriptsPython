#!/usr/bin/env python3
"""
Script pour découper un PDF en plusieurs fichiers de taille maximale définie.
Version avec interface graphique.
Nécessite : pip install PyPDF2
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from PyPDF2 import PdfReader, PdfWriter
import argparse

class PDFSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Découpeur de PDF par taille")
        self.root.geometry("700x600")
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.max_size = tk.StringVar(value="20")
        self.is_processing = False
        
        # Style
        self.setup_styles()
        
        # Créer l'interface
        self.create_widgets()
        
        # Centrer la fenêtre
        self.center_window()
    
    def setup_styles(self):
        """Configure les styles pour l'interface"""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'))
        
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titre
        title_label = ttk.Label(main_frame, text="Découpeur de PDF par taille", 
                                style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Section: Fichier d'entrée
        ttk.Label(main_frame, text="Fichier PDF à découper:", 
                 style='Header.TLabel').grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_file, width=60)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(input_frame, text="Parcourir...", 
                  command=self.browse_input_file).grid(row=0, column=1)
        
        input_frame.columnconfigure(0, weight=1)
        
        # Section: Taille maximale
        ttk.Label(main_frame, text="Taille maximale par fichier (Mo):", 
                 style='Header.TLabel').grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        size_frame = ttk.Frame(main_frame)
        size_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.size_spinbox = ttk.Spinbox(size_frame, from_=1, to=500, 
                                        textvariable=self.max_size, width=15)
        self.size_spinbox.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(size_frame, text="Mo").grid(row=0, column=1, padx=(5, 0))
        
        # Boutons prédéfinis pour les tailles courantes
        ttk.Label(size_frame, text="Tailles courantes:").grid(row=0, column=2, padx=(30, 10))
        ttk.Button(size_frame, text="10 Mo", width=8,
                  command=lambda: self.max_size.set("10")).grid(row=0, column=3, padx=2)
        ttk.Button(size_frame, text="20 Mo", width=8,
                  command=lambda: self.max_size.set("20")).grid(row=0, column=4, padx=2)
        ttk.Button(size_frame, text="25 Mo", width=8,
                  command=lambda: self.max_size.set("25")).grid(row=0, column=5, padx=2)
        ttk.Button(size_frame, text="50 Mo", width=8,
                  command=lambda: self.max_size.set("50")).grid(row=0, column=6, padx=2)
        
        # Section: Dossier de sortie
        ttk.Label(main_frame, text="Dossier de sortie:", 
                 style='Header.TLabel').grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_dir, width=60)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(output_frame, text="Parcourir...", 
                  command=self.browse_output_dir).grid(row=0, column=1)
        
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Label(output_frame, text="(Laisser vide pour utiliser le dossier du fichier source)", 
                 font=('Arial', 8), foreground='gray').grid(row=1, column=0, sticky=tk.W, pady=(2, 0))
        
        # Bouton de traitement
        self.process_button = ttk.Button(main_frame, text="Découper le PDF", 
                                        command=self.process_pdf)
        self.process_button.grid(row=7, column=0, columnspan=3, pady=20)
        
        # Barre de progression
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Zone de log
        ttk.Label(main_frame, text="Journal d'exécution:", 
                 style='Header.TLabel').grid(row=9, column=0, sticky=tk.W, pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=12, width=70, 
                                                  wrap=tk.WORD, font=('Consolas', 9))
        self.log_text.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurer le redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(10, weight=1)
    
    def browse_input_file(self):
        """Ouvre un dialogue pour sélectionner le fichier PDF"""
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier PDF",
            filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Suggérer automatiquement le dossier de sortie
            if not self.output_dir.get():
                self.output_dir.set(os.path.dirname(filename))
    
    def browse_output_dir(self):
        """Ouvre un dialogue pour sélectionner le dossier de sortie"""
        dirname = filedialog.askdirectory(title="Sélectionner le dossier de sortie")
        if dirname:
            self.output_dir.set(dirname)
    
    def log(self, message):
        """Ajoute un message dans la zone de log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """Efface la zone de log"""
        self.log_text.delete(1.0, tk.END)
    
    def process_pdf(self):
        """Lance le traitement dans un thread séparé"""
        if self.is_processing:
            messagebox.showwarning("Traitement en cours", 
                                 "Un traitement est déjà en cours. Veuillez patienter.")
            return
        
        # Validation
        if not self.input_file.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier PDF à découper.")
            return
        
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Erreur", "Le fichier sélectionné n'existe pas.")
            return
        
        try:
            max_size = float(self.max_size.get())
            if max_size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "La taille maximale doit être un nombre positif.")
            return
        
        # Lancer le traitement dans un thread
        self.is_processing = True
        self.process_button.config(state='disabled')
        self.progress.start()
        self.clear_log()
        
        thread = threading.Thread(target=self.split_pdf_thread)
        thread.daemon = True
        thread.start()
    
    def split_pdf_thread(self):
        """Thread pour le découpage du PDF"""
        try:
            input_path = self.input_file.get()
            output_dir = self.output_dir.get() or os.path.dirname(input_path)
            max_size_mb = float(self.max_size.get())
            
            self.split_pdf_by_size(input_path, max_size_mb, output_dir)
            
            self.root.after(0, lambda: messagebox.showinfo("Succès", 
                                                          "Le PDF a été découpé avec succès!"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erreur", 
                                                           f"Une erreur est survenue:\n{str(e)}"))
            self.log(f"Erreur: {str(e)}")
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.process_button.config(state='normal'))
            self.root.after(0, lambda: self.progress.stop())
    
    def get_file_size_mb(self, file_path):
        """Retourne la taille du fichier en MB"""
        return os.path.getsize(file_path) / (1024 * 1024)
    
    def split_pdf_by_size(self, input_pdf_path, max_size_mb, output_dir):
        """Découpe un PDF en plusieurs fichiers de taille maximale définie"""
        
        # Créer le dossier de sortie si nécessaire
        os.makedirs(output_dir, exist_ok=True)
        
        # Nom de base pour les fichiers de sortie
        base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
        
        self.log(f"Lecture du PDF : {os.path.basename(input_pdf_path)}")
        self.log(f"Taille originale : {self.get_file_size_mb(input_pdf_path):.2f} Mo")
        self.log(f"Taille maximale par fichier : {max_size_mb} Mo")
        self.log(f"Dossier de sortie : {output_dir}")
        self.log("-" * 60)
        
        # Lecture du PDF
        reader = PdfReader(input_pdf_path)
        total_pages = len(reader.pages)
        
        self.log(f"Nombre total de pages : {total_pages}")
        self.log("")
        
        # Variables pour le découpage
        current_writer = PdfWriter()
        current_part = 1
        current_pages = []
        created_files = []
        
        for page_num in range(total_pages):
            # Ajouter la page courante
            page = reader.pages[page_num]
            current_writer.add_page(page)
            current_pages.append(page_num + 1)
            
            # Créer un fichier temporaire pour vérifier la taille
            temp_filename = os.path.join(output_dir, f"temp_check.pdf")
            with open(temp_filename, 'wb') as temp_file:
                current_writer.write(temp_file)
            
            current_size_mb = self.get_file_size_mb(temp_filename)
            
            # Si la taille dépasse la limite ou c'est la dernière page
            if (current_size_mb > max_size_mb and len(current_pages) > 1) or \
               (page_num == total_pages - 1 and len(current_pages) > 0):
                
                # Si on dépasse la limite, retirer la dernière page ajoutée
                if current_size_mb > max_size_mb and len(current_pages) > 1:
                    # Recréer le writer sans la dernière page
                    current_writer = PdfWriter()
                    for p in current_pages[:-1]:
                        current_writer.add_page(reader.pages[p-1])
                    pages_range = f"{current_pages[0]}-{current_pages[-2]}"
                    next_start = current_pages[-1]
                else:
                    # C'est la dernière page, on garde tout
                    pages_range = f"{current_pages[0]}-{current_pages[-1]}"
                    next_start = None
                
                # Sauvegarder le fichier
                output_filename = f"{base_name}_partie_{current_part:03d}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, 'wb') as output_file:
                    current_writer.write(output_file)
                
                final_size = self.get_file_size_mb(output_path)
                created_files.append(output_path)
                
                self.log(f"Créé : {output_filename}")
                self.log(f"   Pages : {pages_range} | Taille : {final_size:.2f} Mo")
                self.log("")
                
                # Préparer pour la partie suivante
                current_writer = PdfWriter()
                current_part += 1
                current_pages = []
                
                # Si on avait retiré la dernière page, la rajouter au nouveau writer
                if next_start and page_num < total_pages - 1:
                    current_writer.add_page(reader.pages[page_num])
                    current_pages.append(page_num + 1)
            
            # Nettoyer le fichier temporaire
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
        
        # Traiter les pages restantes si nécessaire
        if len(current_pages) > 0:
            output_filename = f"{base_name}_partie_{current_part:03d}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'wb') as output_file:
                current_writer.write(output_file)
            
            final_size = self.get_file_size_mb(output_path)
            created_files.append(output_path)
            
            pages_range = f"{current_pages[0]}-{current_pages[-1]}"
            self.log(f"Créé : {output_filename}")
            self.log(f"   Pages : {pages_range} | Taille : {final_size:.2f} Mo")
            self.log("")
        
        self.log("-" * 60)
        self.log(f"Terminé ! {len(created_files)} fichiers créés dans :")
        self.log(f"{output_dir}")

# Fonctions pour utilisation en ligne de commande
def get_file_size_mb(file_path):
    """Retourne la taille du fichier en MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def split_pdf_by_size(input_pdf_path, max_size_mb=20, output_dir=None):
    """Version ligne de commande du découpage PDF"""
    
    if not os.path.exists(input_pdf_path):
        raise FileNotFoundError(f"Le fichier {input_pdf_path} n'existe pas")
    
    if output_dir is None:
        output_dir = os.path.dirname(input_pdf_path)
    else:
        os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
    
    print(f"Lecture du PDF : {input_pdf_path}")
    print(f"Taille originale : {get_file_size_mb(input_pdf_path):.2f} MB")
    print(f"Taille maximale par fichier : {max_size_mb} MB")
    print("-" * 50)
    
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    
    print(f"Nombre total de pages : {total_pages}")
    
    current_writer = PdfWriter()
    current_part = 1
    current_pages = []
    created_files = []
    
    for page_num in range(total_pages):
        page = reader.pages[page_num]
        current_writer.add_page(page)
        current_pages.append(page_num + 1)
        
        temp_filename = os.path.join(output_dir, f"temp_check.pdf")
        with open(temp_filename, 'wb') as temp_file:
            current_writer.write(temp_file)
        
        current_size_mb = get_file_size_mb(temp_filename)
        
        if (current_size_mb > max_size_mb and len(current_pages) > 1) or \
           (page_num == total_pages - 1 and len(current_pages) > 0):
            
            if current_size_mb > max_size_mb and len(current_pages) > 1:
                current_writer = PdfWriter()
                for p in current_pages[:-1]:
                    current_writer.add_page(reader.pages[p-1])
                pages_range = f"{current_pages[0]}-{current_pages[-2]}"
                next_start = current_pages[-1]
            else:
                pages_range = f"{current_pages[0]}-{current_pages[-1]}"
                next_start = None
            
            output_filename = f"{base_name}_partie_{current_part:03d}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'wb') as output_file:
                current_writer.write(output_file)
            
            final_size = get_file_size_mb(output_path)
            created_files.append(output_path)
            
            print(f"Créé : {output_filename}")
            print(f"   Pages : {pages_range} | Taille : {final_size:.2f} MB")
            
            current_writer = PdfWriter()
            current_part += 1
            current_pages = []
            
            if next_start and page_num < total_pages - 1:
                current_writer.add_page(reader.pages[page_num])
                current_pages.append(page_num + 1)
        
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
    
    if len(current_pages) > 0:
        output_filename = f"{base_name}_partie_{current_part:03d}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'wb') as output_file:
            current_writer.write(output_file)
        
        final_size = get_file_size_mb(output_path)
        created_files.append(output_path)
        
        pages_range = f"{current_pages[0]}-{current_pages[-1]}"
        print(f"Créé : {output_filename}")
        print(f"   Pages : {pages_range} | Taille : {final_size:.2f} MB")
    
    print("-" * 50)
    print(f"Terminé ! {len(created_files)} fichiers créés")
    
    return created_files

def main():
    """Fonction principale - choisit entre GUI et ligne de commande"""
    
    # Si aucun argument, lancer l'interface graphique
    if len(sys.argv) == 1:
        root = tk.Tk()
        app = PDFSplitterGUI(root)
        root.mainloop()
    else:
        # Mode ligne de commande
        parser = argparse.ArgumentParser(
            description='Découper un PDF en plusieurs fichiers de taille maximale définie',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Exemples d'utilisation:
  %(prog)s                          # Lance l'interface graphique
  %(prog)s mon_fichier.pdf          # Mode ligne de commande
  %(prog)s mon_fichier.pdf -s 10
  %(prog)s mon_fichier.pdf -s 25 -o ./dossier_sortie/
            """
        )
        
        parser.add_argument('input_pdf', nargs='?',
                           help='Chemin vers le fichier PDF à découper')
        
        parser.add_argument('-s', '--size', 
                           type=float, 
                           default=20,
                           help='Taille maximale par fichier en MB (défaut: 20)')
        
        parser.add_argument('-o', '--output', 
                           help='Répertoire de sortie (défaut: même que le fichier d\'entrée)')
        
        args = parser.parse_args()
        
        if not args.input_pdf:
            # Pas de fichier spécifié, lancer l'interface graphique
            root = tk.Tk()
            app = PDFSplitterGUI(root)
            root.mainloop()
        else:
            # Mode ligne de commande
            try:
                split_pdf_by_size(
                    input_pdf_path=args.input_pdf,
                    max_size_mb=args.size,
                    output_dir=args.output
                )
            except FileNotFoundError as e:
                print(f"Erreur : {e}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Erreur inattendue : {e}", file=sys.stderr)
                sys.exit(1)

if __name__ == "__main__":
    main()
