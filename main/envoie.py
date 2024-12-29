import os
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def envoyer_fichiers(dossier, url, progress_bar, progress_label):
    fichiers = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
    total_fichiers = len(fichiers)
    
    for index, fichier in enumerate(fichiers):
        chemin_fichier = os.path.join(dossier, fichier)
        with open(chemin_fichier, 'rb') as f:
            files = {'file': (fichier, f)}
            response = requests.post(url, files=files)
            if response.status_code == 200:
                print(f"Fichier {fichier} envoyé avec succès.")
            else:
                print(f"Échec de l'envoi du fichier {fichier}. Statut: {response.status_code}")
        
        # Mettre à jour la barre de progression
        progress = (index + 1) / total_fichiers * 100
        progress_bar['value'] = progress
        progress_label.config(text=f"Progression : {index + 1}/{total_fichiers} fichiers envoyés")
        root.update_idletasks()
    
    messagebox.showinfo("Terminé", "Tous les fichiers ont été envoyés.")

def lancer_envoi():
    dossier = os.path.join(os.path.dirname(__file__), "data")  # Dossier contenant les fichiers à envoyer
    user_data_path = os.path.join(dossier, 'user_data.txt')  # Chemin complet vers user_data.txt
    if not os.path.exists(user_data_path):
        messagebox.showerror("Erreur", f"Le fichier {user_data_path} n'existe pas.")
        return
    
    with open(user_data_path, 'r') as file:
        lines = file.readlines()
        ip = None
        xaero_path = None
        for line in lines:
            if line.startswith("ip = "):
                ip = line.split(" = ")[1].strip()
            elif line.startswith("xaero = "):
                xaero_path = line.split(" = ")[1].strip()
    
    if not ip or not xaero_path:
        messagebox.showerror("Erreur", "Les informations 'ip' ou 'xaero' sont manquantes dans user_data.txt.")
        return
    
    url = f"http://{ip}/upload"
    envoyer_fichiers(xaero_path, url, progress_bar, progress_label)

# Créer l'interface graphique
root = tk.Tk()
root.title("Envoi de fichiers")
root.geometry("400x200")

progress_label = tk.Label(root, text="Progression : 0/0 fichiers envoyés")
progress_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=20)

start_button = tk.Button(root, text="Commencer l'envoi", command=lancer_envoi)
start_button.pack(pady=10)

root.mainloop()