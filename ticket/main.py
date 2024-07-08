import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class TicketManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tickets Traxxouu")
        self.tickets_en_cours = []
        self.tickets_utilises = []

        #ouverture des données
        self.charger_donnees()

        # interface utilisateur
        self.creer_interface()

    def creer_interface(self):
        # Frame principale
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(padx=10, pady=10)

        # En cours
        label_en_cours = tk.Label(frame_principal, text="En cours")
        label_en_cours.grid(row=0, column=0)

        self.listbox_en_cours = tk.Listbox(frame_principal, selectmode=tk.SINGLE)
        self.listbox_en_cours.grid(row=1, column=0, padx=5)

        # Utilisés
        label_utilises = tk.Label(frame_principal, text="Utilisés")
        label_utilises.grid(row=0, column=1)

        self.listbox_utilises = tk.Listbox(frame_principal, selectmode=tk.SINGLE)
        self.listbox_utilises.grid(row=1, column=1, padx=5)

        # Bouton déplacer
        bouton_deplacer = tk.Button(frame_principal, text="Déplacer", command=self.deplacer_ticket)
        bouton_deplacer.grid(row=2, column=0, pady=5)

        # Bouton Ajouter
        bouton_ajouter = tk.Button(self.root, text="Ajouter Ticket", command=self.ajouter_ticket)
        bouton_ajouter.pack(pady=5)

        # Bouton Supprimer
        bouton_supprimer = tk.Button(self.root, text="Supprimer Ticket", command=self.supprimer_ticket)
        bouton_supprimer.pack(pady=5)

        # Bouton enregistrer et fermer
        bouton_enregistrer = tk.Button(self.root, text="Enregistrer et Fermer", command=self.enregistrer_et_fermer)
        bouton_enregistrer.pack(pady=10)

        # Bouton recherche
        bouton_recherche = tk.Button(self.root, text="Rechercher", command=self.rechercher_ticket)
        bouton_recherche.pack(pady=5)

        self.entry_recherche = tk.Entry(self.root)
        self.entry_recherche.pack(pady=5)

    def deplacer_ticket(self):
        selected_index = self.listbox_en_cours.curselection()
        if selected_index:
            ticket = self.tickets_en_cours.pop(selected_index[0])
            self.tickets_utilises.append(ticket)
            self.maj_listbox()

    def ajouter_ticket(self):
        nouveau_ticket = simpledialog.askstring("Ajouter un ticket", "Entrez le numéro du nouveau ticket:")
        if nouveau_ticket and nouveau_ticket not in self.tickets_en_cours + self.tickets_utilises:
            self.tickets_en_cours.append(nouveau_ticket)
            self.maj_listbox()

    def supprimer_ticket(self):
        selected_index = self.listbox_en_cours.curselection()
        if selected_index:
            ticket = self.tickets_en_cours.pop(selected_index[0])
            self.maj_listbox()

    def enregistrer_et_fermer(self):
        self.enregistrer_donnees()
        self.root.destroy()

    def rechercher_ticket(self):
        recherche = self.entry_recherche.get()
        for i, ticket in enumerate(self.tickets_en_cours):
            if recherche in ticket:
                messagebox.showinfo("Résultat de la recherche", f"Le ticket {ticket} se trouve dans la liste en cours.")
                return

        for i, ticket in enumerate(self.tickets_utilises):
            if recherche in ticket:
                messagebox.showinfo("Résultat de la recherche", f"Le ticket {ticket} se trouve dans la liste utilisée.")
                return

        messagebox.showinfo("Résultat de la recherche", f"Aucun résultat trouvé pour le ticket {recherche}.")

    def maj_listbox(self):
        self.listbox_en_cours.delete(0, tk.END)
        self.listbox_utilises.delete(0, tk.END)

        for ticket in self.tickets_en_cours:
            self.listbox_en_cours.insert(tk.END, ticket)

        for ticket in self.tickets_utilises:
            self.listbox_utilises.insert(tk.END, ticket)

    def charger_donnees(self):
        try:
            with open("donnees_tickets.json", "r") as file:
                data = json.load(file)
                self.tickets_en_cours = data.get("en_cours", [])
                self.tickets_utilises = data.get("utilises", [])
        except FileNotFoundError:
            pass

    def enregistrer_donnees(self):
        data = {"en_cours": self.tickets_en_cours, "utilises": self.tickets_utilises}
        with open("donnees_tickets.json", "w") as file:
            json.dump(data, file)

    def run(self):
        self.maj_listbox()
        self.root.mainloop()


#le truc chiant mais bien

if __name__ == "__main__":
    app = TicketManager()
    app.run()
