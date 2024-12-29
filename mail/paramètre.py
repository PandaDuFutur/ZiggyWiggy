import os
import tkinter as tk
from tkinter import messagebox

def read_user_data(file_path):
    print("Lecture des données utilisateur...")  # Impression de débogage
    with open(file_path, 'r') as file:
        data = {}
        for line in file:
            key, value = line.strip().split(' = ')
            data[key] = value
        return data

def save_user_data(file_path, data):
    print("Sauvegarde des données utilisateur...")  # Impression de débogage
    with open(file_path, 'w') as file:
        for key, value in data.items():
            file.write(f"{key} = {value}\n")

def show_user_data(data, user_data_file):
    print("Affichage des données utilisateur...")  # Impression de débogage
    def save_changes():
        data['ip'] = ip_entry.get()
        data['xearo'] = xearo_entry.get()
        save_user_data(user_data_file, data)
        messagebox.showinfo("Success", "Les données ont été mises à jour.")
        root.destroy()

    root = tk.Tk()
    root.title("Modifier les paramètres")

    tk.Label(root, text="IP:").grid(row=0, column=0, padx=10, pady=10)
    ip_entry = tk.Entry(root)
    ip_entry.grid(row=0, column=1, padx=10, pady=10)
    ip_entry.insert(0, data.get('ip', ''))

    tk.Label(root, text="Xaero:").grid(row=1, column=0, padx=10, pady=10)
    xearo_entry = tk.Entry(root)
    xearo_entry.grid(row=1, column=1, padx=10, pady=10)
    xearo_entry.insert(0, data.get('xearo', ''))

    save_button = tk.Button(root, text="Save", command=save_changes)
    save_button.grid(row=2, columnspan=2, pady=10)

    root.mainloop()

def main():
    print("Exécution de la fonction principale...")  # Impression de débogage
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    user_data_file = os.path.join(data_folder, 'user_data.txt')

    if os.path.exists(user_data_file):
        user_data = read_user_data(user_data_file)
        show_user_data(user_data, user_data_file)
    else:
        print(f"File {user_data_file} does not exist.")

main()