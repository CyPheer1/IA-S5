from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

db = sqlite3.connect("vehicules.db")
cursor = db.cursor()


# Création des tables
def creer_tables():
    cursor.execute("""CREATE TABLE IF NOT EXISTS vehicule (
                        annee_achat INTEGER, 
                        prix_achat REAL, 
                        prix_courant REAL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS camion (
                        annee_achat INTEGER, 
                        prix_achat REAL, 
                        prix_courant REAL, 
                        volume REAL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS moteur (
                        annee_achat INTEGER, 
                        prix_achat REAL, 
                        prix_courant REAL, 
                        puissance REAL)""")
    db.commit()


creer_tables()


# Gestion des données
def ajouter_enregistrement(table, champs):
    try:
        cursor.execute(f"INSERT INTO {table} ({', '.join(champs.keys())}) VALUES ({', '.join(['?' for _ in champs])})", tuple(champs.values()))
        db.commit()
        messagebox.showinfo("Succès", "Enregistrement ajouté avec succès.")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")


def afficher_donnees(tree, table):
    cursor.execute(f"SELECT * FROM {table}")
    records = cursor.fetchall()
    for item in tree.get_children():
        tree.delete(item)
    for record in records:
        tree.insert("", "end", values=record)




# Interface graphique 
root = Tk()
root.title("Gestion des Véhicules, Camions et Moteurs")
root.geometry("1000x800")
root.configure(bg="#2c3e50")  


style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=("Helvetica", 10), background="#ecf0f1", foreground="#2c3e50", rowheight=25)
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#34495e", foreground="white")
style.configure("TButton", padding=10, relief="flat", background="#2980b9", foreground="white", font=("Helvetica", 10))

# En-tête principal
header = Frame(root, bg="#34495e", height=50)
header.pack(fill="x")

title = Label(header, text="Gestion des Véhicules", font=("Helvetica", 18, "bold"), bg="#34495e", fg="white", pady=10)
title.pack()

notebook = ttk.Notebook(root)
notebook.pack(pady=20, expand=True, fill="both")

# ------------------- Onglet Véhicules -------------------


tab_vehicule = Frame(notebook, bg="#ecf0f1")
notebook.add(tab_vehicule, text="Véhicules")

Label(tab_vehicule, text="Ajouter un Véhicule", font=("Helvetica", 14, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=10)

form_vehicule = Frame(tab_vehicule, bg="#ecf0f1")
form_vehicule.pack(pady=10)

Label(form_vehicule, text="Année d'achat:", bg="#ecf0f1", fg="#2c3e50").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_annee_vehicule = Entry(form_vehicule)
entry_annee_vehicule.grid(row=0, column=1, padx=10, pady=5)

Label(form_vehicule, text="Prix d'achat:", bg="#ecf0f1", fg="#2c3e50").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_prix_vehicule = Entry(form_vehicule)
entry_prix_vehicule.grid(row=1, column=1, padx=10, pady=5)

Button(form_vehicule, text="Ajouter Véhicule", command=lambda: ajouter_enregistrement("vehicule", {
    "annee_achat": int(entry_annee_vehicule.get()),
    "prix_achat": float(entry_prix_vehicule.get()),
    "prix_courant": (1.0 - ((2015 - int(entry_annee_vehicule.get())) * 0.01)) * float(entry_prix_vehicule.get())
})).grid(row=2, column=0, columnspan=2, pady=10)

tree_vehicule = ttk.Treeview(tab_vehicule, columns=("Année", "Prix Achat", "Prix Courant"), show="headings", height=10)

tree_vehicule.column("Année", width=150)
tree_vehicule.column("Prix Achat", width=150)
tree_vehicule.column("Prix Courant", width=150)

tree_vehicule.heading("Année", text="Année")
tree_vehicule.heading("Prix Achat", text="Prix Achat")
tree_vehicule.heading("Prix Courant", text="Prix Courant")
tree_vehicule.pack(pady=10)

Button(tab_vehicule, text="Afficher Véhicules", command=lambda: afficher_donnees(tree_vehicule, "vehicule")).pack(pady=5)


# ------------------- Onglet Camions-------------------


tab_camion = Frame(notebook, bg="#ecf0f1")
notebook.add(tab_camion, text="Camions")

Label(tab_camion, text="Ajouter un Camion", font=("Helvetica", 14, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=10)

form_camion = Frame(tab_camion, bg="#ecf0f1")
form_camion.pack(pady=10)

Label(form_camion, text="Année d'achat:", bg="#ecf0f1", fg="#2c3e50").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_annee_camion = Entry(form_camion)
entry_annee_camion.grid(row=0, column=1, padx=10, pady=5)

Label(form_camion, text="Prix d'achat:", bg="#ecf0f1", fg="#2c3e50").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_prix_camion = Entry(form_camion)
entry_prix_camion.grid(row=1, column=1, padx=10, pady=5)

Label(form_camion, text="Volume (m³):", bg="#ecf0f1", fg="#2c3e50").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_volume_camion = Entry(form_camion)
entry_volume_camion.grid(row=2, column=1, padx=10, pady=5)

def calculer_prix_courant_camion(prix_achat, volume):
    """Calcule le prix courant pour un camion."""
    return (1 - (0.1 * volume / 1000)) * prix_achat

Button(form_camion, text="Ajouter Camion", command=lambda: ajouter_enregistrement("camion", {
    "annee_achat": int(entry_annee_camion.get()),
    "prix_achat": float(entry_prix_camion.get()),
    "volume": float(entry_volume_camion.get()),
    "prix_courant": calculer_prix_courant_camion(float(entry_prix_camion.get()), float(entry_volume_camion.get()))
})).grid(row=3, column=0, columnspan=2, pady=10)

tree_camion = ttk.Treeview(tab_camion, columns=("Année", "Prix Achat", "Volume", "Prix Courant"), show="headings", height=10)

tree_camion.column("Année", width=150)
tree_camion.column("Prix Achat", width=150)
tree_camion.column("Volume", width=150)
tree_camion.column("Prix Courant", width=150)

tree_camion.heading("Année", text="Année")
tree_camion.heading("Prix Achat", text="Prix Achat")
tree_camion.heading("Volume", text="Volume")
tree_camion.heading("Prix Courant", text="Prix Courant")
tree_camion.pack(pady=10)

Button(tab_camion, text="Afficher Camions", command=lambda: afficher_donnees(tree_camion, "camion")).pack(pady=5)



# ------------------- Onglet Moteurs -------------------

tab_moteur = Frame(notebook, bg="#ecf0f1")
notebook.add(tab_moteur, text="Moteurs")

Label(tab_moteur, text="Ajouter un Moteur", font=("Helvetica", 14, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=10)

form_moteur = Frame(tab_moteur, bg="#ecf0f1")
form_moteur.pack(pady=10)

Label(form_moteur, text="Année d'achat:", bg="#ecf0f1", fg="#2c3e50").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_annee_moteur = Entry(form_moteur)
entry_annee_moteur.grid(row=0, column=1, padx=10, pady=5)

Label(form_moteur, text="Prix d'achat:", bg="#ecf0f1", fg="#2c3e50").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_prix_moteur = Entry(form_moteur)
entry_prix_moteur.grid(row=1, column=1, padx=10, pady=5)

Label(form_moteur, text="Puissance (kW):", bg="#ecf0f1", fg="#2c3e50").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_puissance_moteur = Entry(form_moteur)
entry_puissance_moteur.grid(row=2, column=1, padx=10, pady=5)

def calculer_prix_courant_moteur(prix_achat, puissance):
    """Calcule le prix courant pour un moteur."""
    return (1 - (0.05 * puissance / 100)) * prix_achat

Button(form_moteur, text="Ajouter Moteur", command=lambda: ajouter_enregistrement("moteur", {
    "annee_achat": int(entry_annee_moteur.get()),
    "prix_achat": float(entry_prix_moteur.get()),
    "puissance": float(entry_puissance_moteur.get()),
    "prix_courant": calculer_prix_courant_moteur(float(entry_prix_moteur.get()), float(entry_puissance_moteur.get()))
})).grid(row=3, column=0, columnspan=2, pady=10)

tree_moteur = ttk.Treeview(tab_moteur, columns=("Année", "Prix Achat", "Puissance", "Prix Courant"), show="headings", height=10)

tree_moteur.column("Année", width=150)
tree_moteur.column("Prix Achat", width=150)
tree_moteur.column("Puissance", width=150)
tree_moteur.column("Prix Courant", width=150)

tree_moteur.heading("Année", text="Année")
tree_moteur.heading("Prix Achat", text="Prix Achat")
tree_moteur.heading("Puissance", text="Puissance")
tree_moteur.heading("Prix Courant", text="Prix Courant")
tree_moteur.pack(pady=10)

Button(tab_moteur, text="Afficher Moteurs", command=lambda: afficher_donnees(tree_moteur, "moteur")).pack(pady=5)

# Lancement de l'application
root.mainloop()
