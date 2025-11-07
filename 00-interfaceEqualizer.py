import tkinter as tk
from tkinter import ttk  # Pour des widgets plus modernes
from tkinter import filedialog

# --- Fonctions (pour l'instant, elles affichent juste un message) ---

def select_file():
    """
    Ouvre une boîte de dialogue pour sélectionner un fichier WAV.
    """
    file_path = filedialog.askopenfilename(
        title="Sélectionner un fichier WAV",
        filetypes=[("Fichiers WAV", "*.wav")]
    )
    if file_path:
        print(f"Fichier sélectionné : {file_path}")
        # C'est ici que vous pourriez appeler wavfile.read(file_path)
        # par exemple : freq_ech, data = wavfile.read(file_path)

def process_audio():
    """
    Récupère les valeurs des 5 sliders et lance le traitement.
    """
    # Récupérer les valeurs actuelles de tous les sliders
    gains = [var.get() for var in slider_vars]
    
    print("Lancement du traitement...")
    print(f"Gains sélectionnés (Bande 0 à 4): {gains}")
    # C'est ici que vous appliquerez vos filtres audio
    # en utilisant les valeurs dans la liste 'gains'

def update_label(value, slider_index):
    """
    Met à jour le label sous le slider pour afficher la valeur actuelle.
    """
    # Formate la valeur pour avoir une seule décimale
    formatted_value = f"{float(value):.1f}"
    
    # Met à jour le texte du label correspondant
    slider_labels[slider_index].config(text=f"Bande{slider_index}: {formatted_value}")


# --- Création de l'interface principale ---

# 1. Fenêtre principale
root = tk.Tk()
root.title("Égaliseur Simple")
root.geometry("400x300") # Taille de la fenêtre (largeur x hauteur)
root.resizable(False, False) # Empêche le redimensionnement

# Style pour les widgets
style = ttk.Style(root)
style.configure("TButton", padding=5)
style.configure("TScale", troughcolor='#d3d3d3')

# --- Widgets ---

# 2. Bouton "Sélectionner un fichier" (en haut)
# Nous utilisons un Frame pour mieux contrôler le placement
top_frame = ttk.Frame(root, padding=10)
top_frame.pack(side="top", fill="x")

btn_select = ttk.Button(top_frame, text="Sélectionner un fichier WAV", command=select_file)
btn_select.pack() # Se centre automatiquement dans le 'top_frame'

# 3. Frame pour les 5 sliders (au milieu)
# Ce 'Frame' contiendra 5 autres 'Frames' (un pour chaque paire slider+label)
sliders_frame = ttk.Frame(root, padding=10)
sliders_frame.pack(side="top", fill="both", expand=True)

# Listes pour garder une référence aux variables et labels des sliders
slider_vars = []   # Stocke les variables (pour lire leur valeur)
slider_labels = [] # Stocke les widgets Label (pour mettre à jour leur texte)

for i in range(5):
    # Crée un Frame pour chaque paire (Slider + Label)
    pair_frame = ttk.Frame(sliders_frame)
    # 'side="left"' aligne les paires horizontalement
    # 'expand=True' et 'fill="x"' les espacent uniformément
    pair_frame.pack(side="left", expand=True, fill="x", padx=5)

    # Variable Tkinter pour stocker la valeur du slider (un float)
    # Nous la réglons sur 0.0 par défaut
    var = tk.DoubleVar(value=0.0)
    slider_vars.append(var)

    # Crée le Slider (Curseur) vertical
    # 'from_' et 'to' définissent la plage (par exemple, gain de -12dB à +12dB)
    # 'command' est lié à notre fonction de mise à jour du label
    slider = ttk.Scale(
        pair_frame,
        from_=12.0,  # Valeur du haut
        to=-12.0,    # Valeur du bas
        orient="vertical",
        variable=var,
        # Le 'lambda' est nécessaire pour passer 'i' (l'index) à la fonction
        command=lambda value, index=i: update_label(value, index)
    )
    slider.pack(side="top", fill="y", expand=True)

    # Crée le Label sous le slider
    label_text = f"Bande{i}: 0.0"
    label = ttk.Label(pair_frame, text=label_text)
    label.pack(side="bottom", pady=5)
    slider_labels.append(label)


# 4. Bouton "Effectuer le traitement" (en bas)
bottom_frame = ttk.Frame(root, padding=10)
bottom_frame.pack(side="bottom", fill="x")

btn_process = ttk.Button(bottom_frame, text="Effectuer le traitement", command=process_audio)
btn_process.pack()


# --- Lancement de la boucle principale ---
# C'est ce qui fait "tourner" l'application et la maintient ouverte
root.mainloop()