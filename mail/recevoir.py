import os
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def recevoir_fichiers(dossier, url, progress_bar, progress_label):
    response = requests.get(url)
    if response.status_code == 200:
        fichiers = response.json()  # Supposons que le serveur renvoie une liste de noms de fichiers
        total_fichiers = len(fichiers)
        
        for index, fichier in enumerate(fichiers):
            chemin_fichier = os.path.join(dossier, fichier)
            file_url = f"{url}/{fichier}"
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                with open(chemin_fichier, 'wb') as f:
                    f.write(file_response.content)
                print(f"Fichier {fichier} reçu avec succès.")
            else:
                print(f"Échec de la réception du fichier {fichier}. Statut: {file_response.status_code}")
            
            # Mettre à jour la barre de progression
            progress = (index + 1) / total_fichiers * 100
            progress_bar['value'] = progress
            progress_label.config(text=f"Progression : {index + 1}/{total_fichiers} fichiers reçus")
            root.update_idletasks()
        
        messagebox.showinfo("Terminé", "Tous les fichiers ont été reçus.")
    else:
        messagebox.showerror("Erreur", f"Échec de la récupération de la liste des fichiers. Statut: {response.status_code}")

def lancer_reception():
    dossier = os.path.join(os.path.dirname(__file__), "data")  # Dossier pour enregistrer les fichiers reçus
    os.makedirs(dossier, exist_ok=True)
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
            elif line.startswith("Xaero = "):
                xaero_path = line.split(" = ")[1].strip()
    
    if not ip or not xaero_path:
        messagebox.showerror("Erreur", "Les informations 'ip' ou 'Xaero' sont manquantes dans user_data.txt.")
        return
    
    url = f"http://{ip}/files"  # URL pour récupérer la liste des fichiers
    recevoir_fichiers(xaero_path, url, progress_bar, progress_label)

# Créer l'interface graphique
root = tk.Tk()
root.title("Réception de fichiers")
root.geometry("400x200")

progress_label = tk.Label(root, text="Progression : 0/0 fichiers reçus")
progress_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=20)

start_button = tk.Button(root, text="Commencer la réception", command=lancer_reception)
start_button.pack(pady=10)

root.mainloop()