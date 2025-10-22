#!/usr/bin/env python3
"""
Interface graphique pour l'extraction de texte de fichiers PDF
Utilise tkinter pour l'interface et pypdf/pdfplumber pour l'extraction
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import sys


class PDFExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Extracteur de Texte PDF")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.pdf_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.method = tk.StringVar(value="auto")
        self.progress_var = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Prêt")
        
        self.extracted_text = ""
        self.is_extracting = False
        
        self.create_widgets()
        self.center_window()
    
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
        
        # Frame principal avec padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # === Section 1: Sélection du fichier PDF ===
        ttk.Label(main_frame, text="Fichier PDF:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        pdf_frame = ttk.Frame(main_frame)
        pdf_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        pdf_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(pdf_frame, textvariable=self.pdf_path, state='readonly').grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(pdf_frame, text="Parcourir...", command=self.browse_pdf).grid(
            row=0, column=1)
        
        # === Section 2: Méthode d'extraction ===
        ttk.Label(main_frame, text="Méthode d'extraction:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        method_frame = ttk.Frame(main_frame)
        method_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        
        ttk.Radiobutton(method_frame, text="Automatique (recommandé)", 
                       variable=self.method, value="auto").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(method_frame, text="PyPDF (rapide)", 
                       variable=self.method, value="pypdf").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(method_frame, text="PDFPlumber (précis)", 
                       variable=self.method, value="pdfplumber").pack(side=tk.LEFT)
        
        # === Section 3: Fichier de sortie ===
        ttk.Label(main_frame, text="Fichier de sortie:", font=('Arial', 10, 'bold')).grid(
            row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(output_frame, textvariable=self.output_path).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="Choisir...", command=self.browse_output).grid(
            row=0, column=1)
        
        # === Section 4: Boutons d'action ===
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=(0, 15))
        
        self.extract_button = ttk.Button(button_frame, text="📄 Extraire le texte", 
                                        command=self.start_extraction, width=20)
        self.extract_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = ttk.Button(button_frame, text="💾 Sauvegarder", 
                                     command=self.save_text, width=20, state='disabled')
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="🗑️ Effacer", 
                                      command=self.clear_all, width=20)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # === Section 5: Barre de progression ===
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # === Section 6: Status ===
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(status_frame, text="Statut:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(status_frame, textvariable=self.status_text, foreground='blue').pack(side=tk.LEFT)
        
        # === Section 7: Zone de texte ===
        ttk.Label(main_frame, text="Texte extrait:", font=('Arial', 10, 'bold')).grid(
            row=9, column=0, sticky=tk.W, pady=(0, 5))
        
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                   width=80, height=20, font=('Courier', 9))
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === Section 8: Barre d'informations ===
        info_frame = ttk.Frame(main_frame, relief='sunken', borderwidth=1)
        info_frame.grid(row=11, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.info_label = ttk.Label(info_frame, text="Aucun fichier chargé", font=('Arial', 8))
        self.info_label.pack(side=tk.LEFT, padx=5)
    
    def browse_pdf(self):
        """Ouvre un dialogue pour sélectionner un fichier PDF"""
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier PDF",
            filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.pdf_path.set(filename)
            # Suggérer un nom de fichier de sortie
            pdf_file = Path(filename)
            output_file = pdf_file.with_suffix('').with_name(f"{pdf_file.stem}_text.txt")
            self.output_path.set(str(output_file))
            self.status_text.set(f"Fichier sélectionné: {pdf_file.name}")
    
    def browse_output(self):
        """Ouvre un dialogue pour choisir le fichier de sortie"""
        filename = filedialog.asksaveasfilename(
            title="Enregistrer le texte sous",
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
    
    def start_extraction(self):
        """Démarre l'extraction dans un thread séparé"""
        if not self.pdf_path.get():
            messagebox.showwarning("Attention", "Veuillez sélectionner un fichier PDF")
            return
        
        if not Path(self.pdf_path.get()).exists():
            messagebox.showerror("Erreur", "Le fichier PDF n'existe pas")
            return
        
        if self.is_extracting:
            messagebox.showinfo("Info", "Une extraction est déjà en cours")
            return
        
        # Désactiver les boutons pendant l'extraction
        self.extract_button.config(state='disabled')
        self.save_button.config(state='disabled')
        self.text_area.delete(1.0, tk.END)
        self.progress_var.set(0)
        
        # Lancer l'extraction dans un thread
        thread = threading.Thread(target=self.extract_text, daemon=True)
        thread.start()
    
    def extract_text(self):
        """Extrait le texte du PDF"""
        self.is_extracting = True
        method = self.method.get()
        
        try:
            self.status_text.set("Extraction en cours...")
            self.progress_var.set(10)
            
            if method == "auto":
                # Essayer pdfplumber d'abord
                text = self.extract_with_pdfplumber()
                if text is None:
                    self.root.after(0, lambda: self.status_text.set("Essai avec pypdf..."))
                    text = self.extract_with_pypdf()
            elif method == "pdfplumber":
                text = self.extract_with_pdfplumber()
            else:  # pypdf
                text = self.extract_with_pypdf()
            
            if text is None:
                self.root.after(0, self.show_library_error)
                return
            
            self.extracted_text = text
            
            # Afficher le texte dans la zone de texte
            self.root.after(0, lambda: self.text_area.insert(1.0, text))
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self.status_text.set(
                f"Extraction terminée! {len(text)} caractères extraits"))
            self.root.after(0, lambda: self.info_label.config(
                text=f"📄 {Path(self.pdf_path.get()).name} | {len(text):,} caractères"))
            self.root.after(0, lambda: self.save_button.config(state='normal'))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur lors de l'extraction:\n{str(e)}"))
            self.root.after(0, lambda: self.status_text.set("Erreur lors de l'extraction"))
        finally:
            self.is_extracting = False
            self.root.after(0, lambda: self.extract_button.config(state='normal'))
    
    def extract_with_pypdf(self):
        """Extrait avec pypdf"""
        try:
            from pypdf import PdfReader
        except ImportError:
            return None
        
        try:
            reader = PdfReader(self.pdf_path.get())
            text = ""
            total_pages = len(reader.pages)
            
            for i, page in enumerate(reader.pages, 1):
                progress = 10 + (80 * i / total_pages)
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda i=i, t=total_pages: 
                               self.status_text.set(f"Extraction avec pypdf... Page {i}/{t}"))
                
                text += f"\n{'='*60}\nPAGE {i}\n{'='*60}\n\n"
                text += page.extract_text()
                text += "\n"
            
            return text
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erreur pypdf", str(e)))
            return None
    
    def extract_with_pdfplumber(self):
        """Extrait avec pdfplumber"""
        try:
            import pdfplumber
        except ImportError:
            return None
        
        try:
            text = ""
            with pdfplumber.open(self.pdf_path.get()) as pdf:
                total_pages = len(pdf.pages)
                
                for i, page in enumerate(pdf.pages, 1):
                    progress = 10 + (80 * i / total_pages)
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    self.root.after(0, lambda i=i, t=total_pages: 
                                   self.status_text.set(f"Extraction avec pdfplumber... Page {i}/{t}"))
                    
                    text += f"\n{'='*60}\nPAGE {i}\n{'='*60}\n\n"
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                    text += "\n"
            
            return text
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erreur pdfplumber", str(e)))
            return None
    
    def show_library_error(self):
        """Affiche un message d'erreur pour les bibliothèques manquantes"""
        msg = ("Impossible d'extraire le texte.\n\n"
               "Veuillez installer les bibliothèques nécessaires:\n\n"
               "pip install pypdf --break-system-packages\n"
               "pip install pdfplumber --break-system-packages")
        messagebox.showerror("Bibliothèques manquantes", msg)
        self.status_text.set("Erreur: bibliothèques manquantes")
        self.extract_button.config(state='normal')
    
    def save_text(self):
        """Sauvegarde le texte extrait"""
        if not self.extracted_text:
            messagebox.showwarning("Attention", "Aucun texte à sauvegarder")
            return
        
        output_file = self.output_path.get()
        if not output_file:
            messagebox.showwarning("Attention", "Veuillez spécifier un fichier de sortie")
            return
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(self.extracted_text)
            
            messagebox.showinfo("Succès", f"Texte sauvegardé dans:\n{output_file}")
            self.status_text.set(f"Texte sauvegardé: {Path(output_file).name}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde:\n{str(e)}")
    
    def clear_all(self):
        """Efface tout"""
        if messagebox.askyesno("Confirmation", "Effacer tous les champs et le texte extrait?"):
            self.pdf_path.set("")
            self.output_path.set("")
            self.text_area.delete(1.0, tk.END)
            self.extracted_text = ""
            self.progress_var.set(0)
            self.status_text.set("Prêt")
            self.info_label.config(text="Aucun fichier chargé")
            self.save_button.config(state='disabled')


def main():
    root = tk.Tk()
    app = PDFExtractorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
