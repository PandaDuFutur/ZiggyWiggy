import tkinter as tk
from tkinter import simpledialog
import os

# Initialiser la fenêtre principale (invisible)
root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale

# Demander les informations dans des popups
ip = simpledialog.askstring("ip", "ip serveur :")
Xaero = simpledialog.askstring("xaero", "xaero loca ? :")

# Vérifier que les informations sont saisies
if ip and Xaero:
    print(f"IP: {ip}, Xaero: {Xaero}")  # Impression de débogage
    
    # Créer le dossier data s'il n'existe pas
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Enregistrer les informations dans un fichier texte
    user_data_path = os.path.join(data_dir, "user_data.txt")
    with open(user_data_path, "w") as file:
        file.write(f"ip = {ip}\n")
        file.write(f"xearo = {Xaero}\n")
    print(f"Les données ont été écrites dans {user_data_path}")  # Impression de débogage
else:
    print("Saisie annulée ou incomplète.")
root.destroy()