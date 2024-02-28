
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import datetime
import random
import string
from PIL import Image,ImageTk
from datetime import datetime

def show_orders():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showinfo('Info', 'Veuillez sélectionner un élément dans le Treeview.')
        return

    values = treeview.item(selected_item)['values']
    if len(values) < 4:
        messagebox.showinfo('Info', "L'élément sélectionné n'a pas assez de valeurs.")
        return

    table_number = values[3]
    date = values[4]

    matching_orders = [row for row in data if row['Numero de Table'] == table_number and row['Date'] == date]

    orders_window = tk.Toplevel(root)
    orders_window.title('Commandes pour Table {} - {}'.format(table_number, date))
    orders_window.configure(background="gold")
    orders_treeview = ttk.Treeview(orders_window, columns=('Nom', 'Prix', 'Quantite'), show='headings')
    orders_treeview.pack(expand=True, fill='both')

    for column in orders_treeview['columns']:
        orders_treeview.heading(column, text=column)

    for row in matching_orders:
        values = (row['Nom'], row['Prix'], row['Quantite'])
        orders_treeview.insert('', 'end', values=values)

    total_label = tk.Label(orders_window,bg='gold', text='Total:  0.00 Dhs')
    total_label.pack()

    total_sum = get_total_sum(orders_treeview)
    total_label.config(text='Total: {:.2f} Dhs'.format(total_sum))


    clear_button = tk.Button(orders_window,width=25, text='Commande Prête', command=lambda: clear_orders(treeview, selected_item))
    clear_button.pack()
    validate_button = tk.Button(orders_window,width=25, text='Imprimer Le Facture', command=lambda: export_orders_to_file(matching_orders, table_number, date, total_sum))
    validate_button.pack()
    quit_button = tk.Button(orders_window,width=25, text='Autre', command=lambda: orders_window.destroy())
    quit_button.pack()



def export_orders_to_file(matching_orders, table_number, date, total_sum):
    date = date.split()[0]
    date = datetime.strptime(date, '%Y-%m-%d') # Convertir la date en format datetime
    invoice_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) # Générer un numéro de facture aléatoire
    filename = f"Table_{table_number}{invoice_number}{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt".replace(" ", "_").replace(":", "-")
    with open(filename, 'w') as txtfile:
        txtfile.write('=============BIENVENUE CHEZ RESTAURANT MA===========\n')
        txtfile.write('Numero de facture: {}\n'.format(invoice_number))
        txtfile.write('Num de Table     : {}\n'.format(table_number))
        txtfile.write('Date et Heure    : {}\n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        txtfile.write('===================================================\n')
        txtfile.write('Nom               Prix                     Quantite\n')
        txtfile.write('===================================================\n')
        for order in matching_orders:
            txtfile.write('{:<20}{:<20}{:<20}\n'.format(order['Nom'], order['Prix'], order['Quantite']))
        txtfile.write('                Total: {:.2f} Dhs\n'.format(total_sum))
        txtfile.write('=============Merci de votre visite===================')

    messagebox.showinfo('Info', 'Commandes exportées avec succès dans le fichier {}'.format(filename))
    
    
def clear_orders(treeview_widget, selected_item):
    # Récupérer les valeurs de la commande sélectionnée
    selected_values = treeview_widget.item(selected_item)['values']
    table_number = selected_values[3]
    date = selected_values[4]

    # Parcourir tous les items du Treeview et effacer ceux qui ont le même numéro de table et la même date
    for item in treeview_widget.get_children():
        values = treeview_widget.item(item)['values']
        if values[3] == table_number and values[4] == date:
            treeview_widget.delete(item)


def get_total_sum(treeview_widget):
    # Logic to calculate the total sum of orders from the Treeview widget
    # You can modify this function to calculate the total sum as desired

    # Example code to calculate the total sum
    total_sum = 0
    for item in treeview_widget.get_children():
        values = treeview_widget.item(item)['values']
        price = float(values[1])
        quantity = float(values[2])
        total_sum += price * quantity

    return total_sum
def quit_app():
    # Afficher une boîte de dialogue de confirmation
    result = messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter l'application?")
    if result:
        root.destroy()  # Fermer la fenêtre principale de l'application

# ...

# Création du bouton Quitter

def clear_treeview():
    treeview.delete(*treeview.get_children())

# Define the reload_data() function
    # Effacer le contenu du fichier CSV
def clear_bdcsv():
    with open('commandes.csv', 'w') as csvfile:
        csvfile.truncate(0)

def reload_data():
    # Clear the Treeview
    clear_treeview()
    
    # Read data from the CSV file
    with open('commandes.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        # Store data from the CSV file in a list
        data = [row for row in reader]

    # Insert data rows
    for row in data:
        values = tuple(row[column] for column in treeview['columns'])
        treeview.insert('', 'end', values=values)
# Create a tkinter window

root = tk.Tk()
root.title('Gestion des Commandes')
root.geometry('2300x3000')
def update_clock():
    now = datetime.now().strftime("%A, %D %B %Y %H:%M:%S")
    canvas.itemconfig(clock_label, text=now)
    root.after(1000, update_clock)
bg_image = Image.open('img/coverRes.jpg')
bg_image=bg_image.resize((3000,3000))
canvas = tk.Canvas(root, width=bg_image.width, height=bg_image.height)
canvas.pack(expand=True, fill='both')
bg_image=ImageTk.PhotoImage(bg_image)
canvas.create_image(50,0,image=bg_image)
clock_label =canvas.create_text(1050, 19, text="", fill="gold", font=('cooper black', 22, 'bold'))
text_canvas=canvas.create_text(700, 70, text=" Suivre les Commandes ", fill="blue", font=('cooper black', 40, 'bold'))        #title
update_clock()
        #----------------logo-----------------------------------------
logo=ImageTk.PhotoImage(Image.open('img/logo2023.png').resize((270, 170)))
canvas.create_image(110,65, image=logo)
        

with open('commandes.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    # Store data from the CSV file in a list
    data = [row for row in reader]

# Create a Treeview widget

treeview = ttk.Treeview(canvas,columns=('Nom', 'Prix', 'Quantite', 'Numero de Table', 'Date'), show='headings')
treeview.pack(expand=True, fill='both', padx=215,pady=100)
treeview['columns'] = tuple(reader.fieldnames)

# Set column headings
for column in treeview['columns']:
    treeview.heading(column, text=column)

# Insert data rows
for row in data:
    values = tuple(row[column] for column in treeview['columns'])
    treeview.insert('', 'end', values=values)

# Create a button to show matching orders
show_orders_button = tk.Button(root, text='AFFICHER\n LES COMMANDES',width=19,height=5, command=show_orders,bd=3,font=('times new roman',12,'bold'),bg='gold')
show_orders_button.place(x=1170,y=270)
clear_button = tk.Button(root, text='EFFACER TABLEAU',width=19, command=clear_treeview,bd=3,font=('times new roman',12,'bold'),bg='red')
clear_button.place(x=1170,y=390)
reload_button = tk.Button(root, text='RECHARGER TABLEAU',width=19, command=reload_data,bd=3,font=('times new roman',12,'bold'),bg='green')
reload_button.place(x=1170,y=430)

# Create a button to reload data from CSV
clear_BD = tk.Button(root, text='EFFACER LA BASE DES DONNEES',width=35, command=clear_bdcsv,bd=2,font=('times new roman',12,'bold'),bg='red')
clear_BD.place(x=400,y=660)
quit_button = tk.Button(root, text='QUITTER',width=35, command=quit_app,bd=2,font=('times new roman',12,'bold'),bg='blue')
quit_button.place(x=730,y=660)
# Recharger le data dans CSV 
reload_data()

# Start the tkinter event loop
root.mainloop()