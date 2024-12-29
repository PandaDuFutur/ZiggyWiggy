import tkinter as tk
from tkinter import messagebox
import importlib.util
import os
import random

def verifier_premiere_fois():
    # Vérifie l'existence du fichier de configuration pour déterminer si c'est la première exécution
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    user_data_path = os.path.join(data_dir, "user_data.txt")
    return not os.path.exists(user_data_path)

def lancer_script():
    # Implémentez la logique pour le bouton "envoie"
    pass

def lancer_script2():
    # Implémentez la logique pour le bouton "recevoir"
    pass

def charger_et_executer_script(script_path):
    print(f"Chargement et exécution du script : {script_path}")  # Impression de débogage
    if os.path.exists(script_path):
        spec = importlib.util.spec_from_file_location("module.name", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        print(f"Le script {script_path} n'existe pas.")  # Impression de débogage

def on_closing():
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter?"):
        app.destroy()

def ouvrir_parametres():
    print("Ouverture des paramètres...")  # Impression de débogage
    parametre_path = os.path.join(os.path.dirname(__file__), "paramètre.py")
    print(f"Chemin du script paramètre : {parametre_path}")  # Impression de débogage
    charger_et_executer_script(parametre_path)

def annonce():
    current_color = clignotant_label.cget("foreground")
    next_color = "red" if current_color == "black" else "black"
    clignotant_label.config(foreground=next_color)
    app.after(500, annonce)


# Liste de messages pour le label clignotant
messages = [
    "I NEED MORE BULLETS",
    "Toujours Sans Paramètres fonctionnels",
    "Mio est ratted",
    "QUI CONTROLE LA MEUTE MéDIATIQUE???",
    "Un jour je vais demander de l'argent",
    "Sauvé par Loumunix"
]


# Vérification de la première exécution
premiere_fois = verifier_premiere_fois()

app = tk.Tk()
app.title("Mon Application")
app.geometry("600x400")

# Lier l'événement de fermeture de la fenêtre à la fonction on_closing
app.protocol("WM_DELETE_WINDOW", on_closing)

# Message de bienvenue en fonction de la première exécution
if premiere_fois:
    messagebox.showinfo("Bienvenue", "C'est la première fois que vous lancez cette application! Vous allez donc devoir configurer l'application")
    charger_et_executer_script(os.path.join(os.path.dirname(__file__), "2.py"))
else:
    messagebox.showinfo("Bienvenue", "Bienvenue de nouveau dans l'application!")

# Ajouter un label clignotant en haut de l'application
clignotant_label = tk.Label(app, text=random.choice(messages), font=("Arial", 16))
clignotant_label.pack(pady=10)
annonce()

label = tk.Label(app, text="Le Postier", font=("Arial", 12))
label.pack(pady=20)

button_envoie = tk.Button(app, text="envoie", command=lancer_script)
button_envoie.pack(pady=10)

button_recevoir = tk.Button(app, text="recevoir", command=lancer_script2)
button_recevoir.pack(pady=10)

button_parametre = tk.Button(app, text="paramètre", command=ouvrir_parametres)
button_parametre.pack(pady=10)

app.mainloop()