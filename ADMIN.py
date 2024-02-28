import tkinter as tk
import tkinter as ttk
root = tk.Tk()
root.title("Page de connexion de l'administrateur")
root.geometry('2500x3000')

root.config(bg="#2c3e50")
label_username = tk.Label(root, text="Nom d'utilisateur", font=("Helvetica", 18), fg="white", bg="#2c3e50")
label_username.place(x=595,y=120)

entry_username = tk.Entry(root, font=("Helvetica", 18))
entry_username.place(x=550,y=160)

label_password = tk.Label(root, text="Mot de passe", font=("Helvetica", 18), fg="white", bg="#2c3e50")
label_password.place(x=595,y=195)

entry_password = tk.Entry(root, show="*", font=("Helvetica", 18))
entry_password.place(x=550,y=235)

button_login = tk.Button(root, text="Connexion", font=("Helvetica", 14), bg="#16a085", fg="white")
button_login.place(x=620,y=280)
# Fonction pour vérifier les informations de connexion
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Vérifier si les informations de connexion sont correctes
    if username == "admin" and password == "password":
        root.destroy()
        show_admin_page()
    else:
        label_error = tk.Label(root, text="Nom d'utilisateur ou mot de passe incorrect", font=("Helvetica", 12), fg="red", bg="#2c3e50")
        label_error.pack(pady=10)

# Fonction pour afficher la page d'administration
def show_admin_page():
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import ttk

    #--------------------------------------adminboisson------------------------------------------------------------
    # Fonction pour ouvrir la fenêtre adminboisson
    def ouvrir_fenetre_adminboisson():
        import tkinter as tk
        from tkinter import ttk
        import sqlite3
        # Connexion à la base de données SQLite3
        conn = sqlite3.connect('BDboissons.db')
        cursor = conn.cursor()
        # Création de la table si elle n'existe pas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prix INTEGER,
                name TEXT
            )
        ''')
        conn.commit()
        root = tk.Tk()
        root.title("Sélection de valeurs")
        root.geometry('950x300')

        tree = ttk.Treeview(root, columns=('prix', 'name'), show='headings', height=23)
        tree.heading('prix', text='Prix')
        tree.heading('name', text='Boissons')
        tree.place(x=280, y=10)

        options = []
        cursor.execute('SELECT prix, name FROM options')
        rows = cursor.fetchall()
        for row in rows:
            options.append((row[0], row[1]))
            tree.insert("", tk.END, values=row)

        combo = ttk.Combobox(root, values=[option[0] for option in options])
        combo.place(x=5, y=10)

        def close_app():
            result = messagebox.askquestion("Fermer", "Voulez-vous vraiment fermer l'application?")
            if result == 'yes':
                root.destroy()    
        def search_keyword():
            keyword = combo.get()

            # Effacer les résultats précédents dans le TreeView
            tree.delete(*tree.get_children())

            # Requête pour rechercher les résultats correspondants dans la base de données
            cursor.execute("SELECT prix, name FROM options WHERE name LIKE ?", ('%'+keyword+'%',))
            rows = cursor.fetchall()

            # Insérer les résultats dans le TreeView
            for row in rows:
                tree.insert("", tk.END, values=row)

        # Fonction de fermeture de l'application
        search_button = ttk.Button(root, text="Rechercher", command=search_keyword)
        search_button.place(x=150, y=8)
            # Création du bouton de fermeture
        close_button = ttk.Button(root,width=20, text="Fermer", command=close_app)
        close_button.place(x=5, y=230)
        def save():
            messagebox.showinfo("Succès", "Opération effectuée avec succès!")
        
        save_button = ttk.Button(root,width=20, text="Enregistrer", command=save)
        save_button.place(x=5, y=200)

        def add_option():
            def save_option():
                new_prix = prix_entry.get()
                new_name = name_entry.get()

                # Ajouter la nouvelle option à la liste d'options
                options.append((new_prix, new_name))

                # Ajouter la nouvelle ligne à la Treeview
                tree.insert("", tk.END, values=(new_prix, new_name))

                # Enregistrer les modifications dans la base de données
                cursor.execute("INSERT INTO options (prix, name) values (?, ?)", (new_prix, new_name))
                conn.commit()

                # Fermer la fenêtre
                add_window.destroy()

            # Créer une nouvelle fenêtre pour saisir le nom et le prix de la nouvelle option
            add_window = tk.Toplevel(root)
            add_window.geometry("200x200")

            add_window.title("Ajouter une option")
            prix_label = ttk.Label(add_window, text="Entrez le prix de la nouvelle option :")
            prix_label.pack()
            prix_entry = ttk.Entry(add_window)
            prix_entry.pack()
            name_label = ttk.Label(add_window, text="Entrez le nom de la nouvelle option :")
            name_label.pack()
            name_entry = ttk.Entry(add_window)
            name_entry.pack()

            # Ajouter un bouton pour enregistrer la modification dans la base de données
            save_button = ttk.Button(add_window, text="Enregistrer", command=save_option)
            save_button.place(x=25, y=100)
            ret_button = ttk.Button(add_window, text="Quitter", command=add_window.destroy)
            ret_button.place(x=100, y=100)

        add_option_button = ttk.Button(root,width=20, text="Ajouter une Boisson", command=add_option)
        add_option_button.place(x=5, y=140)

        def modify_optionB():
            selected_item = tree.selection()
            if selected_item:
                values = tree.item(selected_item)['values']
                if values:
                    selected_prix = values[0]
                    selected_name = values[1]

                    # Vérifier si l'option existe dans la liste d'options en utilisant soit le prix, soit le nom
                    selected_option = [option for option in options if option[0] == selected_prix or option[1] == selected_name]
                    if selected_option:
                        # Créer une fenêtre de modification
                        modify_window = tk.Toplevel(root)
                        modify_window.geometry("200x200")
                        modify_window.title("Modifier une Boisson")

                        # Créer des labels pour saisir les modifications
                        prix_label = ttk.Label(modify_window, text="Prix actuel :")
                        prix_label.pack()
                        prix_entry = ttk.Entry(modify_window)
                        prix_entry.insert(tk.END, selected_option[0][0])
                        prix_entry.pack()
                        name_label = ttk.Label(modify_window, text="Nom actuel:")
                        name_label.pack()
                        name_entry = ttk.Entry(modify_window)
                        name_entry.insert(tk.END, selected_option[0][1])
                        name_entry.pack()

                        def update_option():
                            new_prix = prix_entry.get()
                            new_name = name_entry.get()

                            # Mettre à jour la liste d'options avec les nouvelles valeurs
                            selected_option[0] = (new_prix, new_name)

                            # Mettre à jour la Treeview avec les nouvelles valeurs
                            tree.item(selected_item, values=(new_prix, new_name))

                            # Mettre à jour les données dans la base de données
                            cursor.execute("UPDATE options SET prix = ?, name = ? WHERE prix = ? OR name = ?", (new_prix, new_name, selected_prix, selected_name))
                            conn.commit()

                            # Fermer la fenêtre
                            modify_window.destroy()

                        # Créer un bouton pour effectuer la modification
                        update_button = ttk.Button(modify_window, text="Modifier", command=update_option)
                        update_button.place(x=25, y=100)
                        ret_button = ttk.Button(modify_window, text="Quitter", command=modify_window.destroy)
                        ret_button.place(x=100, y=100)
                    else:
                        # Afficher un message d'erreur si l'option n'est pas trouvée dans la liste d'options
                        messagebox.showerror("Erreur", "Option introuvable dans la liste d'options.")
                else:
                    # Afficher un message d'erreur si aucune option n'est sélectionnée dans la Treeview
                    messagebox.showerror("Erreur", "Aucune option sélectionnée.")
            else:
                # Afficher un message d'erreur si aucune option n'est sélectionnée dans la Treeview
                messagebox.showerror("Erreur", "Aucune option sélectionnée.")

        modify_button = ttk.Button(root,width=20, text="Modifier le Boisson", command=modify_optionB)
        modify_button.place(x=5, y=110)
        # Fonction pour supprimer une option sélectionnée
        def delete_option():
            selected_item = tree.selection()
            if selected_item:
                values = tree.item(selected_item)['values']
                if values:
                    selected_prix = values[0]
                    selected_name = values[1]
                    
                    # Vérifier si l'option existe dans la liste d'options en utilisant soit le prix, soit le nom
                    selected_option = [option for option in options if option[0] == selected_prix or option[1] == selected_name]
                    if selected_option:
                        options.remove(selected_option[0])
                        
                        tree.delete(selected_item)
                        
                        cursor.execute("DELETE FROM options WHERE prix = ? OR name = ?", (selected_prix, selected_name))
                        conn.commit()
                    else:
                        print("Option not found in options list!")
                else:
                    print("No values found for selected item in Treeview!")
            else:
                print("No item selected in Treeview!")
                
        delete_button = ttk.Button(root,width=20, text="Supprimer le boisson", command=delete_option)
        delete_button.place(x=5, y=170)
        root.mainloop()

        # Fermer la connexion à la base de données à la fin du programme
        conn.close()
    #----------------------------------------------------------------------------------------------------------------------------------------
    def ouvrir_fenetre_adminSalade():
        import tkinter as tk
        from tkinter import ttk
        import sqlite3
        from tkinter import messagebox
        # Connexion à la base de données SQLite3
        conn = sqlite3.connect('BDsalades.db')
        cursor = conn.cursor()

        # Création de la table si elle n'existe pas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prix INTEGER,
                name TEXT
            )
        ''')
        conn.commit()

        root = tk.Tk()
        root.title("Sélection de salades")
        root.geometry('950x300')

        tree = ttk.Treeview(root, columns=('prix', 'name'), show='headings', height=23)
        tree.heading('prix', text='Prix')
        tree.heading('name', text='Salades')
        tree.place(x=280, y=10)

        options = []
        cursor.execute('SELECT prix, name FROM options')
        rows = cursor.fetchall()
        for row in rows:
            options.append((row[0], row[1]))
            tree.insert("", tk.END, values=row)


        combo = ttk.Combobox(root, values=[option[1] for option in options])
        combo.place(x=5, y=10)

        def add_option():
            def save_option():
                new_prix = prix_entry.get()
                new_name = name_entry.get()

                # Ajouter la nouvelle option à la liste d'options
                options.append((new_prix, new_name))

                # Ajouter la nouvelle ligne à la Treeview
                tree.insert("", tk.END, values=(new_prix, new_name))

                # Enregistrer les modifications dans la base de données
                cursor.execute("INSERT INTO options (prix, name) values (?, ?)", (new_prix, new_name))
                conn.commit()

                # Fermer la fenêtre
                add_window.destroy()

            # Créer une nouvelle fenêtre pour saisir le nom et le prix de la nouvelle option
            add_window = tk.Toplevel(root)
            add_window.title("Ajouter une salade")
            add_window.geometry("200x200")
            prix_label = ttk.Label(add_window, text="Entrez le prix de la nouvelle salade :")
            prix_label.pack()
            prix_entry = ttk.Entry(add_window)
            prix_entry.pack()
            name_label = ttk.Label(add_window, text="Entrez le nom de la nouvelle salade :")
            name_label.pack()
            name_entry = ttk.Entry(add_window)
            name_entry.pack()

            # Ajouter un bouton pour enregistrer la modification dans la base de données
            save_button = ttk.Button(add_window, text="Enregistrer", command=save_option)
            save_button.place(x=25, y=100)
            ret_button = ttk.Button(add_window, text="Quitter", command=add_window.destroy)
            ret_button.place(x=100, y=100)

        add_option_button = ttk.Button(root,width=20, text="Ajouter une salade", command=add_option)
        add_option_button.place(x=5, y=140)
    # Création du bouton de recherche
        def close_app():
            result = messagebox.askquestion("Fermer", "Voulez-vous vraiment fermer l'application?")
            if result == 'yes':
                root.destroy()    
        def search_keyword():
            keyword = combo.get()

            # Effacer les résultats précédents dans le TreeView
            tree.delete(*tree.get_children())

            # Requête pour rechercher les résultats correspondants dans la base de données
            cursor.execute("SELECT prix, name FROM options WHERE name LIKE ?", ('%'+keyword+'%',))
            rows = cursor.fetchall()

            # Insérer les résultats dans le TreeView
            for row in rows:
                tree.insert("", tk.END, values=row)

        # Fonction de fermeture de l'application
        search_button = ttk.Button(root, text="Rechercher", command=search_keyword)
        search_button.place(x=150, y=8)
            # Création du bouton de fermeture
        close_button = ttk.Button(root,width=20, text="Fermer", command=close_app)
        close_button.place(x=5, y=230)
        def save():
            messagebox.showinfo("Succès", "Opération effectuée avec succès!")
        
        save_button = ttk.Button(root,width=20, text="Enregistrer", command=save)
        save_button.place(x=5, y=200)

        def modify_optionS():
            selected_item = tree.selection()
            if selected_item:
                values = tree.item(selected_item)['values']
                if values:
                    selected_prix = values[0]
                    selected_name = values[1]

                    # Vérifier si l'option existe dans la liste d'options en utilisant soit le prix, soit le nom
                    selected_option = [option for option in options if option[0] == selected_prix or option[1] == selected_name]
                    if selected_option:
                        # Créer une fenêtre de modification
                        modify_window = tk.Toplevel(root)
                        modify_window.geometry("200x200")
                        modify_window.title("Modifier une option")

                        # Créer des labels pour saisir les modifications
                        prix_label = ttk.Label(modify_window, text="Prix actuel :")
                        prix_label.pack()
                        prix_entry = ttk.Entry(modify_window)
                        prix_entry.insert(tk.END, selected_option[0][0])
                        prix_entry.pack()
                        name_label = ttk.Label(modify_window, text="Nom actuel:")
                        name_label.pack()
                        name_entry = ttk.Entry(modify_window)
                        name_entry.insert(tk.END, selected_option[0][1])
                        name_entry.pack()

                        def update_option():
                            new_prix = prix_entry.get()
                            new_name = name_entry.get()

                            # Mettre à jour la liste d'options avec les nouvelles valeurs
                            selected_option[0] = (new_prix, new_name)

                            # Mettre à jour la Treeview avec les nouvelles valeurs
                            tree.item(selected_item, values=(new_prix, new_name))

                            # Mettre à jour les données dans la base de données
                            cursor.execute("UPDATE options SET prix = ?, name = ? WHERE prix = ? OR name = ?", (new_prix, new_name, selected_prix, selected_name))
                            conn.commit()

                            # Fermer la fenêtre
                            modify_window.destroy()

                        # Créer un bouton pour effectuer la modification
                        update_button = ttk.Button(modify_window, text="Modifier", command=update_option)
                        update_button.place(x=25, y=100)
                        ret_button = ttk.Button(modify_window, text="Quitter", command=modify_window.destroy)
                        ret_button.place(x=100, y=100)
                    else:
                        # Afficher un message d'erreur si l'option n'est pas trouvée dans la liste d'options
                        messagebox.showerror("Erreur", "Option introuvable dans la liste d'options.")
                else:
                    # Afficher un message d'erreur si aucune option n'est sélectionnée dans la Treeview
                    messagebox.showerror("Erreur", "Aucune option sélectionnée.")
            else:
                # Afficher un message d'erreur si aucune option n'est sélectionnée dans la Treeview
                messagebox.showerror("Erreur", "Aucune option sélectionnée.")

        modify_button = ttk.Button(root,width=20, text="Modifier une Salade", command=modify_optionS)
        modify_button.place(x=5, y=110)
        def delete_option():
            selected_item = tree.selection()
            if selected_item:
                values = tree.item(selected_item)['values']
                if values:
                    selected_prix = values[0]
                    selected_name = values[1]
                    
                    # Vérifier si l'option existe dans la liste d'options en utilisant soit le prix, soit le nom
                    selected_option = [option for option in options if option[0] == selected_prix or option[1] == selected_name]
                    if selected_option:
                        options.remove(selected_option[0])
                        
                        tree.delete(selected_item)
                        
                        cursor.execute("DELETE FROM options WHERE prix = ? OR name = ?", (selected_prix, selected_name))
                        conn.commit()
                    else:
                        print("Option not found in options list!")
                else:
                    print("No values found for selected item in Treeview!")
            else:
                print("No item selected in Treeview!")
                

        delete_option_button = ttk.Button(root, text="Supprimer une salade", command=delete_option)
        delete_option_button.place(x=5, y=170)
        root.mainloop()

        # Fermer la connexion à la base de données SQLite3
        conn.close()

    def ouvrir_fenetre_adminPlat():
        import tkinter as tk
        from tkinter import ttk
        import sqlite3

        # Connexion à la base de données SQLite3
        conn = sqlite3.connect('BDplats.db')
        cursor = conn.cursor()

        # Création de la table si elle n'existe pas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prix INTEGER,
                name TEXT
            )
        ''')
        conn.commit()

        root = tk.Tk()
        root.title("Sélection de plats")
        root.geometry('950x300')

        tree = ttk.Treeview(root, columns=('prix', 'name'), show='headings', height=23)
        tree.heading('prix', text='Prix')
        tree.heading('name', text='Plats')
        tree.place(x=280, y=10)

        plats = []
        cursor.execute('SELECT prix, name FROM plats')
        rows = cursor.fetchall()
        for row in rows:
            plats.append((row[0], row[1]))
            tree.insert("", tk.END, values=row)

        combo = ttk.Combobox(root, values=[plat[0] for plat in plats])
        combo.place(x=5, y=10)
        #####################
        def close_app():
            result = messagebox.askquestion("Fermer", "Voulez-vous vraiment fermer l'application?")
            if result == 'yes':
                root.destroy()    
        def search_keyword():
            keyword = combo.get()

            # Effacer les résultats précédents dans le TreeView
            tree.delete(*tree.get_children())

            # Requête pour rechercher les résultats correspondants dans la base de données
            cursor.execute("SELECT prix, name FROM plats WHERE name LIKE ?", ('%'+keyword+'%',))
            rows = cursor.fetchall()

            # Insérer les résultats dans le TreeView
            for row in rows:
                tree.insert("", tk.END, values=row)

        # Fonction de fermeture de l'application
        search_button = ttk.Button(root, text="Rechercher", command=search_keyword)
        search_button.place(x=150, y=8)
            # Création du bouton de fermeture
        close_button = ttk.Button(root,width=20, text="Fermer", command=close_app)
        close_button.place(x=5, y=230)
        def save():
            messagebox.showinfo("Succès", "Opération effectuée avec succès!")
        
        save_button = ttk.Button(root,width=20, text="Enregistrer", command=save)
        save_button.place(x=5, y=200)



        def add_plat():
            def save_plat():
                new_prix = prix_entry.get()
                new_name = name_entry.get()

                # Ajouter le nouveau plat à la liste de plats
                plats.append((new_prix, new_name))

                # Ajouter la nouvelle ligne à la Treeview
                tree.insert("", tk.END, values=(new_prix, new_name))

                # Enregistrer les modifications dans la base de données
                cursor.execute("INSERT INTO plats (prix, name) values (?, ?)", (new_prix, new_name))
                conn.commit()

                # Fermer la fenêtre
                add_window.destroy()

            # Créer une nouvelle fenêtre pour saisir le nom et le prix du nouveau plat
            add_window = tk.Toplevel(root)
            add_window.title("Ajouter un plat")
            add_window.geometry("200x200")
            prix_label = ttk.Label(add_window, text="Entrez le prix du nouveau plat :")
            prix_label.pack()
            prix_entry = ttk.Entry(add_window)
            prix_entry.pack()
            name_label = ttk.Label(add_window, text="Entrez le nom du nouveau plat :")
            name_label.pack()
            name_entry = ttk.Entry(add_window)
            name_entry.pack()

            # Ajouter un bouton pour enregistrer la modification dans la base de données
            save_button = ttk.Button(add_window, text="Enregistrer", command=save_plat)
            save_button.place(x=25, y=100)
            ret_button = ttk.Button(add_window, text="Quitter", command=add_window.destroy)
            ret_button.place(x=100, y=100)

        add_plat_button = ttk.Button(root,width=20, text="Ajouter un plat", command=add_plat)
        add_plat_button.place(x=5, y=140)


        def modify_optionP():
            selected_item = tree.selection()
            if selected_item:
                values = tree.item(selected_item)['values']
                if values:
                    selected_prix = values[0]
                    selected_name = values[1]

                    # Vérifier si l'option existe dans la liste d'options en utilisant soit le prix, soit le nom
                    selected_option = [option for option in plats if option[0] == selected_prix or option[1] == selected_name]
                    if selected_option:
                        # Créer une fenêtre de modification
                        modify_window = tk.Toplevel(root)
                        modify_window.geometry("200x200")
                        modify_window.title("Modifier une option")

                        # Créer des labels pour saisir les modifications
                        prix_label = ttk.Label(modify_window, text="Prix actuel :")
                        prix_label.pack()
                        prix_entry = ttk.Entry(modify_window)
                        prix_entry.insert(tk.END, selected_option[0][0])
                        prix_entry.pack()
                        name_label = ttk.Label(modify_window, text="Nom actuel:")
                        name_label.pack()
                        name_entry = ttk.Entry(modify_window)
                        name_entry.insert(tk.END, selected_option[0][1])
                        name_entry.pack()

                        def update_option():
                            new_prix = prix_entry.get()
                            new_name = name_entry.get()

                            # Mettre à jour la liste d'options avec les nouvelles valeurs
                            selected_option[0] = (new_prix, new_name)

                            # Mettre à jour la Treeview avec les nouvelles valeurs
                            tree.item(selected_item, values=(new_prix, new_name))

                            # Mettre à jour les données dans la base de données
                            cursor.execute("UPDATE plats SET prix = ?, name = ? WHERE prix = ? OR name = ?", (new_prix, new_name, selected_prix, selected_name))
                            conn.commit()

                            # Fermer la fenêtre
                            modify_window.destroy()

                        # Créer un bouton pour effectuer la modification
                        update_button = ttk.Button(modify_window, text="Modifier", command=update_option)
                        update_button.place(x=25, y=100)
                        ret_button = ttk.Button(modify_window, text="Quitter", command=modify_window.destroy)
                        ret_button.place(x=100, y=100)
                    else:
                        # Afficher un message d'erreur si l'option n'est pas trouvée dans la liste d'options
                        messagebox.showerror("Erreur", "Option introuvable dans la liste d'options.")
                else:
                    # Afficher un message d'erreur si aucune option n'est sélectionnée dans la Treeview
                    messagebox.showerror("Erreur", "Aucune option sélectionnée.")
            else:
                # Afficher un message d'erreur si aucune option n'est sélectionnée dans la Treeview
                messagebox.showerror("Erreur", "Aucune option sélectionnée.")

        modify_button = ttk.Button(root,width=20, text="Modifier le Plat", command=modify_optionP)
        modify_button.place(x=5, y=110)

        def delete_plat():
            selected_item = tree.selection()
            if selected_item:
                values = tree.item(selected_item)['values']
                if values:
                    selected_prix = values[0]
                    selected_name = values[1]
                    
                    # Vérifier si l'option existe dans la liste d'plats en utilisant soit le prix, soit le nom
                    selected_option = [option for option in plats if option[0] == selected_prix or option[1] == selected_name]
                    if selected_option:
                        plats.remove(selected_option[0])
                        
                        tree.delete(selected_item)
                        
                        cursor.execute("DELETE FROM plats WHERE prix = ? OR name = ?", (selected_prix, selected_name))
                        conn.commit()
                    else:
                        print("Option not found in plats list!")
                else:
                    print("No values found for selected item in Treeview!")
            else:
                print("No item selected in Treeview!")
                

        delete_option_button = ttk.Button(root,width=20, text="Supprimer une Plat", command=delete_plat)
        delete_option_button.place(x=5, y=170)


        root.mainloop()

        # Fermer la connexion à la base de données à la fin du programme
        # cursor.close()
        conn.close()
############################
    def open_remarque_window():
        remarque_window = tk.Toplevel(root)
        remarque_window.title('Restaurant - Remarques')
        remarque_window.geometry('450x300')

        # Créer une Listbox pour afficher les remarques
        listbox_remarques = tk.Listbox(remarque_window, width=50, height=10)
        listbox_remarques.pack(pady=10)

        # Lire les remarques à partir du fichier
        try:
            with open("remarques.csv", "r") as fichier:
                remarques = fichier.readlines()
                for remarque in remarques:
                    listbox_remarques.insert(tk.END, remarque.strip())
        except FileNotFoundError:
            print("Le fichier de remarques n'a pas été trouvé.")
        def clear_bdcsv():
            with open('remarques.csv', 'w') as csvfile:
                csvfile.truncate(0)

        # Fermer la fenêtre de remarques
        button_fermer = tk.Button(remarque_window, text="Fermer", command=remarque_window.destroy,width=12, bd=2, relief=tk.GROOVE, font=('times new roman', 15, 'bold'), bg='green')
        button_fermer.pack()
        button_fermer = tk.Button(remarque_window, text="clear", command=clear_bdcsv,width=12, bd=2, relief=tk.GROOVE, font=('times new roman', 15, 'bold'), bg='red')
        button_fermer.pack()

        remarque_window.mainloop()
    def table():
        import csv
        import tkinter as tk
        from tkinter import ttk

        def write_table_number(table_number):
            with open('table_numbers.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Table' + table_number])

        def remove_table_number(table_number):
            with open('table_numbers.csv', mode='r') as file:
                reader = csv.reader(file)
                table_numbers = [row[0] for row in reader if row[0] != 'Table' + table_number]

            with open('table_numbers.csv', mode='w', newline='') as file:
                        writer = csv.writer(file)
                        for table_number in table_numbers:
                            writer.writerow([table_number])

        def modify_table_number(old_table_number, new_table_number):
            with open('table_numbers.csv', mode='r') as file:
                reader = csv.reader(file)
                table_numbers = [row[0] if row[0] != 'Table' + old_table_number else 'Table' + new_table_number for row in reader]

            with open('table_numbers.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                for table_number in table_numbers:
                    writer.writerow([table_number])

        def add_table_number():
            table_number = table_number_entry.get()
            write_table_number(table_number)
            table_number_entry.delete(0, tk.END)
            update_table_numbers_listbox(get_table_numbers())

        def delete_table_number():
                    table_number = delete_table_number_entry.get()
                    remove_table_number(table_number)
                    delete_table_number_entry.delete(0, tk.END)   
                    update_table_numbers_listbox(get_table_numbers())

        def modify_table_number_gui():
            old_table_number = table_numbers_listbox.get(table_numbers_listbox.curselection())
            new_table_number = new_table_number_entry.get()
            modify_table_number(old_table_number[5:], new_table_number)  # remove "Table" prefix from old table number
            table_number_entry.delete(0, tk.END)
            new_table_number_entry.delete(0, tk.END)
            update_table_numbers_listbox(get_table_numbers())

        def get_table_numbers():
            with open('table_numbers.csv', mode='r') as file:
                reader = csv.reader(file)
                table_numbers = [int(row[0][5:]) for row in reader if row[0].startswith('Table')]

            return ["Table" + str(table_number) for table_number in sorted(table_numbers)]

        def update_table_numbers_listbox(table_numbers):
            table_numbers_listbox.delete(0, tk.END)
            for table_number in table_numbers:
                table_numbers_listbox.insert(tk.END, table_number)
        

        table_window = tk.Toplevel(root)
        table_window.title("Gestion des tables")
        table_window.geometry("400x400")

        # Ajout d'une Frame pour les boutons d'actions
        actions_frame = ttk.Frame(table_window)
        actions_frame.pack(pady=20)

        # Création du label et de l'entrée pour ajouter une table
        table_number_label = ttk.Label(actions_frame, text="Numéro de table :")
        table_number_label.grid(row=0, column=0, padx=5, pady=5)

        table_number_entry = ttk.Entry(actions_frame)
        table_number_entry.grid(row=0, column=1, padx=5, pady=5)

        add_table_number_button = ttk.Button(actions_frame, text="Ajouter", command=add_table_number, style='Button.TButton')
        add_table_number_button.grid(row=0, column=2, padx=5, pady=5)

        # Création du label et de l'entrée pour modifier une table



        new_table_number_label = ttk.Label(actions_frame, text="Nouveau numéro de table :")
        new_table_number_label.grid(row=2, column=0, padx=5, pady=5)

        new_table_number_entry = ttk.Entry(actions_frame)
        new_table_number_entry.grid(row=2, column=1, padx=5, pady=5)

        modify_table_number_button = ttk.Button(actions_frame, text="Modifier", command=modify_table_number_gui, style='Button.TButton')
        modify_table_number_button.grid(row=2, column=2, padx=5, pady=5)

        # Création du label et de l'entrée pour supprimer une table
        delete_table_number_label = ttk.Label(actions_frame, text="Numéro de table à supprimer :")
        delete_table_number_label.grid(row=3, column=0, padx=5, pady=5)

        delete_table_number_entry = ttk.Entry(actions_frame)
        delete_table_number_entry.grid(row=3, column=1, padx=5, pady=5)

        delete_table_number_button = ttk.Button(actions_frame, text="Supprimer", command=delete_table_number, style='Button.TButton')
        delete_table_number_button.grid(row=3, column=2, padx=5, pady=5)
        delete_table_number_button = ttk.Button(actions_frame, text="Quitter", command=actions_frame.destroy, style='Button.TButton')
        delete_table_number_button.grid(row=4, column=2, padx=5, pady=5)


        # Création du Listbox pour afficher la liste des tables
        table_numbers =get_table_numbers()
        table_numbers_listbox = tk.Listbox(table_window, height=10)
        table_numbers_listbox.pack()
        delete_table_number_button = ttk.Button(actions_frame, text="Quitter", command=table_window.destroy, style='Button.TButton')
        delete_table_number_button.grid(row=4, column=2, padx=5, pady=5)
        update_table_numbers_listbox(table_numbers)
        table_window.mainloop()

    




    #########################**********************************************###############################333333################
    # Créer la fenêtre principale
    from datetime import datetime
    from tkinter import Canvas
    from PIL import Image,ImageTk

    root = tk.Tk()
    root.title("Fenêtre principale")
    root.geometry('2500x3000')

    # Créer une frame dans la fenêtre principale
    frame_principale = tk.Frame(root)
    frame_principale.pack(pady=20)

    # Ajouter du contenu dans la frame principale
    def update_clock():
        now = datetime.now().strftime("%A, %D %B %Y %H:%M:%S")
        canvas.itemconfig(clock_label, text=now)
        root.after(1000, update_clock)
    bg_image = Image.open('img/coverRes.jpg')
    bg_image=bg_image.resize((3900,2000))
    canvas = tk.Canvas(root, width=bg_image.width, height=bg_image.height)
    canvas.pack(expand=True, fill='both')
    bg_image=ImageTk.PhotoImage(bg_image)
    canvas.create_image(50,0,image=bg_image)
    clock_label =canvas.create_text(1000, 19, text="", fill="gold", font=('cooper black', 22, 'bold'))
    text_canvas=canvas.create_text(700, 200, text=" Gestion Des Commandes ", fill="blue",font=('cooper black', 40, 'bold'))        #title
    update_clock()

    logo=ImageTk.PhotoImage(Image.open('img/logo2023.png').resize((300, 200)))
    canvas.create_image(110,65, image=logo)

    # Créer un bouton pour ouvrir la fenêtre adminboisson
    bouton1 = tk.Button(canvas, text="Ouvrir fenêtre Boisson",bg='red',font=('cooper black', 25, 'bold'), command=ouvrir_fenetre_adminboisson)
    bouton1.place(x=11,y=300)
    bouton2 = tk.Button(canvas, text="Ouvrir fenêtre Salade",bg='green', command=ouvrir_fenetre_adminSalade,font=('cooper black', 25, 'bold'))
    bouton2.place(x=500,y=300)

    bouton3 = tk.Button(canvas, text="Ouvrir fenêtre Plat",bg='gold', command=ouvrir_fenetre_adminPlat,font=('cooper black', 25, 'bold'))
    bouton3.place(x=950,y=300)
    quit_button = tk.Button(canvas,width=12, text='Quitter',bd=2, font=('times new roman', 20, 'bold'), bg='red', fg='white', command=root.destroy)
    quit_button.place(x=1100,y=600)
    button_remarque = tk.Button(canvas, text="Voire les Remarques", command=open_remarque_window,width=17, bd=2, font=('times new roman', 20, 'bold'), bg='green', fg='white')
    button_remarque.place(x=800,y=600)
    button_table = tk.Button(canvas, text="Modifier Table", command=table,width=17, bd=2, font=('times new roman', 20, 'bold'), bg='blue', fg='white')
    button_table.place(x=500,y=600)


    root.mainloop()

# Ajouter une fonctionnalité au bouton de connexion
button_login.config(command=login)
def onglet1(tab):
    frame=tk.Frame(tab)
    label=tk.Label(frame,text="admin")
    label.pack(padx=50,pady=50)
    frame.pack(expand=True,fill="both")
# Afficher la fenêtre
root.mainloop()