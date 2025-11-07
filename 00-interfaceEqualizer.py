import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
from scipy.io import wavfile
# --- Bibliothèques pour ouvrir le fichier ---
import webbrowser  # <-- Pour ouvrir un fichier avec l'application par défaut
import tempfile    # <-- Pour créer un fichier temporaire
import os          # <-- Pour gérer les chemins de fichiers

# --- Variables globales pour stocker l'audio ---
audio_data = None
modified_audio_data = None
sample_rate = None

# --- Fonctions ---

def select_file():
    """
    Ouvre une boîte de dialogue pour sélectionner un fichier WAV
    ET le charge en mémoire.
    """
    global audio_data, sample_rate, modified_audio_data

    file_path = filedialog.askopenfilename(
        title="Sélectionner un fichier WAV",
        filetypes=[("Fichiers WAV", "*.wav")]
    )
    if file_path:
        print(f"Fichier sélectionné : {file_path}")
        try:
            sample_rate, audio_data = wavfile.read(file_path)
            print("Fichier chargé avec succès.")
            
            modified_audio_data = None 
            
            # Normaliser en float32
            if audio_data.dtype != 'float32':
                max_val = np.iinfo(audio_data.dtype).max
                audio_data = audio_data.astype('float32') / max_val

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
            audio_data = None
            sample_rate = None

def process_audio():
    """
    Récupère les valeurs des sliders, applique le traitement,
    SAUVEGARDE dans un fichier temporaire et le JOUE via l'OS.
    """
    global audio_data, sample_rate, modified_audio_data 

    if audio_data is None:
        print("Erreur : Veuillez d'abord charger un fichier WAV.")
        return

    gains_db = [var.get() for var in slider_vars]
    print("Lancement du traitement...")
    print(f"Gains (dB) sélectionnés : {gains_db}")

    # --- Démo de traitement (inchangée) ---
    gain_lineaire = 10**(gains_db[0] / 20.0) 
    temp_data = audio_data * gain_lineaire
    temp_data = np.clip(temp_data, -1.0, 1.0)
    modified_audio_data = temp_data 

    # --- NOUVELLE PARTIE : Écoute via fichier temporaire ---
    try:
        # 1. Définir un chemin pour le fichier temporaire
        # ex: C:\Users\Hp\AppData\Local\Temp\temp_equalized.wav
        temp_path = os.path.join(tempfile.gettempdir(), "temp_equalized.wav")

        # 2. Convertir les données en int16 pour le fichier WAV
        data_to_save = (modified_audio_data * 32767).astype(np.int16)

        # 3. Écrire le fichier WAV temporaire
        wavfile.write(temp_path, sample_rate, data_to_save)

        # 4. Demander au système d'exploitation d'ouvrir ce fichier
        print(f"Lecture via le lecteur par défaut (fichier : {temp_path})")
        webbrowser.open(temp_path)

    except Exception as e:
        print(f"Erreur lors de la création ou lecture du fichier temporaire : {e}")
    # --- FIN DE LA NOUVELLE PARTIE ---


def save_file():
    """
    Ouvre une boîte de dialogue pour SAUVEGARDER le fichier audio modifié
    de manière permanente. (Fonction inchangée)
    """
    global modified_audio_data, sample_rate

    if modified_audio_data is None:
        print("Erreur : Vous devez d'abord 'Effectuer le traitement' avant d'enregistrer.")
        return
        
    if sample_rate is None:
        print("Erreur : 'sample_rate' est inconnu.")
        return

    file_path = filedialog.asksaveasfilename(
        title="Enregistrer le fichier modifié sous...",
        defaultextension=".wav",
        filetypes=[("Fichiers WAV", "*.wav")]
    )
    
    if not file_path:
        print("Enregistrement annulé.")
        return

    try:
        print("Conversion en int16...")
        data_to_save = (modified_audio_data * 32767).astype(np.int16)
        wavfile.write(file_path, sample_rate, data_to_save)
        print(f"Fichier modifié enregistré avec succès sous : {file_path}")

    except Exception as e:
        print(f"Erreur lors de l'enregistrement du fichier : {e}")

def update_label(value, slider_index):
    formatted_value = f"{float(value):.1f}"
    slider_labels[slider_index].config(text=f"Bande{slider_index}: {formatted_value}")


# --- Interface graphique (inchangée) ---
root = tk.Tk()
root.title("Égaliseur Simple")
root.geometry("400x320")
root.resizable(False, False)

style = ttk.Style(root)
style.configure("TButton", padding=5)
style.configure("TScale", troughcolor='#d3d3d3')

top_frame = ttk.Frame(root, padding=10)
top_frame.pack(side="top", fill="x")

btn_select = ttk.Button(top_frame, text="Sélectionner un fichier WAV", command=select_file)
btn_select.pack()

sliders_frame = ttk.Frame(root, padding=10)
sliders_frame.pack(side="top", fill="both", expand=True)

slider_vars = []   
slider_labels = [] 

for i in range(5):
    pair_frame = ttk.Frame(sliders_frame)
    pair_frame.pack(side="left", expand=True, fill="x", padx=5)
    var = tk.DoubleVar(value=0.0)
    slider_vars.append(var)
    slider = ttk.Scale(
        pair_frame, from_=12.0, to=-12.0,
        orient="vertical", variable=var,
        command=lambda value, index=i: update_label(value, index)
    )
    slider.pack(side="top", fill="y", expand=True)
    label = ttk.Label(pair_frame, text=f"Bande{i}: 0.0")
    label.pack(side="bottom", pady=5)
    slider_labels.append(label)

bottom_frame = ttk.Frame(root, padding=10)
bottom_frame.pack(side="bottom", fill="x")

btn_process = ttk.Button(bottom_frame, text="Effectuer le traitement", command=process_audio)
btn_process.pack(side="left", expand=True, padx=5) 

btn_save = ttk.Button(bottom_frame, text="Enregistrer sous...", command=save_file)
btn_save.pack(side="right", expand=True, padx=5) 

root.mainloop()