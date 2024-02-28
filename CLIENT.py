from tkinter import*
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import messagebox
import os 
import random
import tkinter as tk
import csv
from tkinter import ttk
import sqlite3
root = tk.Tk()
root.title('Restaurant')
root.geometry('2500x3000')
# Create a custom style for the Radiobutton
style = ttk.Style()

# Define the font for the Radiobutton
style.configure("Custom.TRadiobutton",background='#5454FF', font=("Helvetica", 12, 'bold'), fg='white')

        #time
def update_clock():
    now = datetime.now().strftime("%A, %D %B %Y  \n\t\t  %H:%M:%S")
    canvas.itemconfig(clock_label, text=now)
    root.after(1000, update_clock)
bg_image = Image.open('coverRes.png')
bg_image=bg_image.resize((2500,3000))
canvas = Canvas(root, width=bg_image.width, height=bg_image.height)
canvas.pack(fill=BOTH,expand=YES )
bg_image=ImageTk.PhotoImage(bg_image)
canvas.create_image(0,0, image=bg_image, anchor=NW)
clock_label =canvas.create_text(1125, 40, text="", fill="white", font=("Helvetica", 25))
text_canvas=canvas.create_text(600, 50, text="    Bienvenue dans votre Restaurant \nEt nous espérons passer un bon moment", fill="white", font=("Comic Sans MS", 22,"bold"))        #title
update_clock()
        #----------------logo-----------------------------------------
logo=ImageTk.PhotoImage(Image.open('img/logo2023.png').resize((300, 230)))
                                     
canvas.create_image(-20,-40, anchor=NW, image=logo)
text_canvas=canvas.create_text(500, 140, text="Num de table", fill="cornflowerblue", font=('cooper black',20,'bold'))    
       
           
        #text_canvas=canvas.create_text(500, 140, text="Num de table", fill="cornflowerblue", font=('cooper black',20,'bold'))    
        #numtabl=Entry(canvas,width=10,font=('times new roman',18,'bold'),textvariable=numtable,bd=2).place(x=600,y=120)


#commendboisson
#/********************************************************************************/
Frame2= tk.LabelFrame(root, text='LES BOISSONS',bd=2, font=('cooper black', 22, 'bold'), fg='gold', bg='#5454FF')
Frame2.place(x=10, y=180, width=450,height=330)
def clear_selection(index):
    optionsB_vars[index].set("")  

def show_selectionsB():
    selected_table=table_var.get()
    if not selected_table:
        messagebox.showerror("Erreur", "Veuillez choisir un numero de table.")
    else:
        selections = []
        for i, var in enumerate(optionsB_vars.values()):
            if var.get() == 1:
                nameBoisson = list(options.keys())[i]
                priceBoisson = options[nameBoisson]
                quantityBoisson = quantityBoisson_entries[i].get()
                if not quantityBoisson:
                    messagebox.showerror("Erreur", "Veuillez entrer une quantite pour l'option '{}'.".format(nameBoisson))
                else:
                    selections.append((nameBoisson, priceBoisson, quantityBoisson))
        if selections:
            show_selectionsB_window(selections)
total_label=None
def show_selectionsB_window(selections):
    global total_label
    selected_table = table_var.get()
    selections_window = tk.Toplevel(Frame2)
    selections_window.title("Sélections")
    selections_frame = ttk.Frame(selections_window)
    selections_frame.pack(padx=10, pady=10)
    total_label = ttk.Label(selections_frame, text="Total: 0")
    total_label.grid(row=len(selections)+1, column=1, columnspan=2, padx=5, pady=5)
    ttk.Label(selections_frame, text=f"Numero de table : {selected_table}").grid(row=0, column=3, columnspan=2, padx=5, pady=5) # Obtenir la valeur sélectionnée dans la combobox
    ttk.Label(selections_frame, text="Boisson").grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(selections_frame, text="Prix").grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(selections_frame, text="Quantite").grid(row=0, column=2, padx=5, pady=5)

    for i, (nameBoisson, priceBoisson, quantityBoisson) in enumerate(selections):
        ttk.Label(selections_frame, text=nameBoisson).grid(row=i+1, column=0, padx=5, pady=5)
        ttk.Label(selections_frame, text=priceBoisson).grid(row=i+1, column=1, padx=5, pady=5)
        ttk.Label(selections_frame, text=quantityBoisson).grid(row=i+1, column=2, padx=5, pady=5)
    def calculate_total():
        total = 0
        for _, priceBoisson, quantityBoisson in selections:
            total += int(priceBoisson) * int(quantityBoisson)
        total_label.config(text=f"Total: {total}")
    ttk.Button(selections_frame, text="Calculer Total", command=calculate_total).grid(row=len(selections)+2, column=1, columnspan=2, padx=5, pady=5)
    for i, (nameBoisson, priceBoisson, quantityBoisson) in enumerate(selections):
        ttk.Label(selections_frame, text=nameBoisson).grid(row=i+1, column=0, padx=5, pady=5)
        ttk.Label(selections_frame, text=priceBoisson).grid(row=i+1, column=1, padx=5, pady=5)
        ttk.Label(selections_frame, text=quantityBoisson).grid(row=i+1, column=2, padx=5, pady=5)
def clear_all_selectionsB():
    for var in optionsB_vars.values():
        var.set(0)
    for entry in quantityBoisson_entries.values():
        entry.delete(0, tk.END)

options_frame = ttk.Frame(Frame2)
options_frame.pack(pady=10)
# Create a custom style with the desired background color
style = ttk.Style()
style.configure("Options.TFrame", background='#5454FF')
options_frame.configure(style="Options.TFrame")


conn = sqlite3.connect("BDboissons.db")
cursor = conn.cursor()
options = {}
optionsB_vars = {}
quantityBoisson_entries = {}


for row in cursor.execute("SELECT name, prix FROM options"):
    nameBoisson = row[0]
    priceBoisson = row[1]
    options[nameBoisson] = priceBoisson
    var = tk.IntVar()
    optionsB_vars[list(options.keys()).index(nameBoisson)] = var
    clear_button = ttk.Button(options_frame, text="Annuler", command=lambda index=list(options.keys()).index(nameBoisson): clear_selection(index))
    clear_button.grid(row=list(options.keys()).index(nameBoisson), column=0, padx=10)
    option_radio = ttk.Radiobutton(options_frame, text=f"{nameBoisson} {priceBoisson} dh", variable=var, value=1, style="Custom.TRadiobutton") # Apply the custom style
    option_radio.grid(row=list(options.keys()).index(nameBoisson), column=1, sticky=tk.W)
    quantityBoisson_label = ttk.Label(options_frame, text=f"Quantite :")
    quantityBoisson_label.configure(background='#5454FF', font=("Helvetica", 12)) # Set the font for the label
    quantityBoisson_label.grid(row=list(options.keys()).index(nameBoisson), column=2, padx=10)
    quantityBoisson_entry = ttk.Entry(options_frame, width=5)
    quantityBoisson_entry.grid(row=list(options.keys()).index(nameBoisson), column=3)
    quantityBoisson_entries[list(options.keys()).index(nameBoisson)] = quantityBoisson_entry


conn.close()



show_selectionsB_button = tk.Button(canvas,height=1,width=36,bd=2,relief=GROOVE,bg='gold',font=('times new roman',16,'bold'), text="Afficher  Les Commandes Sélections",command=show_selectionsB)
show_selectionsB_button.place(x=12, y=520)

clear_all_button = tk.Button(canvas,height=1,width=36,bd=2,relief=GROOVE,bg='blue',font=('times new roman',16,'bold'), text="Effacer Les Commandes Sélections", command=clear_all_selectionsB)
clear_all_button.place(x=10, y=565)





        


######################################





#/********************************************************************************
#commendles salades
            #***************************************************
Frame3 = LabelFrame(root, text='LES SALADES',bd=2, font=('cooper black', 22, 'bold'), fg='gold', bg='#5454FF')
Frame3.place(x=465, y=180,width=445,height=330)
def clear_selectionS(index):
    optionsS_vars[index].set("")  

def show_selections():
    selected_table=table_var.get()
    if not selected_table:
        messagebox.showerror("Erreur", "Veuillez choisir un numero de table.")
    else:
        selections = []
        for i, var in enumerate(optionsS_vars.values()):
            if var.get() == 1:
                nameSalade = list(optionsS.keys())[i]
                priceSalade = optionsS[nameSalade]
                quantitySalade = quantitySalade_entries[i].get()
                if not quantitySalade:
                    messagebox.showerror("Erreur", "Veuillez entrer une quantite pour l'option '{}'.".format(nameSalade))
                else:
                    selections.append((nameSalade, priceSalade, quantitySalade))
        if selections:
            show_selections_window(selections)

totalS_labelS=None
def show_selections_window(selections):
    global totalS_labelS
    selected_table = table_var.get()
    selections_window = tk.Toplevel(Frame3)
    selections_window.title("Sélections")
    selections_frame = ttk.Frame(selections_window)
    selections_frame.pack(padx=10, pady=10)
    totalS_labelS = ttk.Label(selections_frame, text="Total: 0")
    totalS_labelS.grid(row=len(selections)+1, column=1, columnspan=2, padx=5, pady=5)
    ttk.Label(selections_frame, text=f"Numero de table : {selected_table}").grid(row=0, column=3, columnspan=2, padx=5, pady=5) # Obtenir la valeur sélectionnée dans la combobox
    ttk.Label(selections_frame, text="Salades").grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(selections_frame, text="Prix").grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(selections_frame, text="Quantite").grid(row=0, column=2, padx=5, pady=5)

    for i, (nameSalade, priceSalade, quantitySalade) in enumerate(selections):
        ttk.Label(selections_frame, text=nameSalade).grid(row=i+1, column=0, padx=5, pady=5)
        ttk.Label(selections_frame, text=priceSalade).grid(row=i+1, column=1, padx=5, pady=5)
        ttk.Label(selections_frame, text=quantitySalade).grid(row=i+1, column=2, padx=5, pady=5)
    def calculate_totalS():
        totalS = 0
        for _, priceSalade, quantitySalade in selections:
            totalS += int(priceSalade) * int(quantitySalade)
        totalS_labelS.config(text=f"TotalS: {totalS}")
    ttk.Button(selections_frame, text="Calculer Total", command=calculate_totalS).grid(row=len(selections)+2, column=1, columnspan=2, padx=5, pady=5)
    for i, (nameSalade, priceSalade, quantitySalade) in enumerate(selections):
        ttk.Label(selections_frame, text=nameSalade).grid(row=i+1, column=0, padx=5, pady=5)
        ttk.Label(selections_frame, text=priceSalade).grid(row=i+1, column=1, padx=5, pady=5)
        ttk.Label(selections_frame, text=quantitySalade).grid(row=i+1, column=2, padx=5, pady=5)
def clear_all_selections():
    for var in optionsS_vars.values():
        var.set(0)
    for entry in quantitySalade_entries.values():
        entry.delete(0, tk.END)

optionsS_frame = ttk.Frame(Frame3)
optionsS_frame.pack(pady=10)
# Create a custom style with the desired background color
style = ttk.Style()
style.configure("Options.TFrame", background='#5454FF')
optionsS_frame.configure(style="Options.TFrame")


conn = sqlite3.connect("BDsalades.db")
cursor = conn.cursor()
optionsS = {}
optionsS_vars = {}
quantitySalade_entries = {}
# Create a custom style for the Radiobutton

for row in cursor.execute("SELECT name, prix FROM options"):
    nameSalade = row[0]
    priceSalade = row[1]
    optionsS[nameSalade] = priceSalade
    var = tk.IntVar()
    optionsS_vars[list(optionsS.keys()).index(nameSalade)] = var
    clear_button = ttk.Button(optionsS_frame, text="Annuler", command=lambda index=list(optionsS.keys()).index(nameSalade): clear_selectionS(index))
    clear_button.grid(row=list(optionsS.keys()).index(nameSalade), column=0, padx=10)
    option_radio = ttk.Radiobutton(optionsS_frame, text=f"{nameSalade} {priceSalade} dh", variable=var, value=1,style="Custom.TRadiobutton")
    option_radio.grid(row=list(optionsS.keys()).index(nameSalade), column=1, sticky=tk.W)
    quantitySalade_label = ttk.Label(optionsS_frame,text=f"Quantite:")
    quantitySalade_label.configure(background='#5454FF', font=("Helvetica", 12)) # Set the font for the label

    quantitySalade_label.grid(row=list(optionsS.keys()).index(nameSalade), column=2, padx=10)
    quantitySalade_entry = ttk.Entry(optionsS_frame,width=5)
    quantitySalade_entry.grid(row=list(optionsS.keys()).index(nameSalade), column=3)
    quantitySalade_entries[list(optionsS.keys()).index(nameSalade)] = quantitySalade_entry

conn.close()
import re
table_var = tk.StringVar()
def read_table_numbers():
    with open('table_numbers.csv', mode='r') as file:
        reader = csv.reader(file)
        table_numbers = [int(re.findall('\d+', row[0])[0]) for row in reader if row[0].startswith('Table')]
        table_numbers.sort()
        table_numbers = ['Table' + str(n) for n in table_numbers]
        return table_numbers
# Create the combobox and set its initial value and position
table_combobox = ttk.Combobox(canvas, width=10, font=('times new roman',18,'bold'), textvariable=table_var)

# Set the values available in the combobox to the list of table numbers
table_combobox['values'] = read_table_numbers()



# Place the combobox in the desired position on the canvas
table_combobox.place(x=600, y=120)
show_selections_button = tk.Button(canvas,height=1,width=36,bd=2,relief=GROOVE,font=('times new roman',16,'bold'),bg='gold', text="Afficher les Commandes des Salades Sélections",command=show_selections)
show_selections_button.place(x=467, y=520)

clear_all_button = tk.Button(canvas,height=1,width=36,bd=2,relief=GROOVE,font=('times new roman',16,'bold'),bg='blue', text="Effacer les Commandes des Salade Sélections", command=clear_all_selections)
clear_all_button.place(x=467, y=565)





#*******************************************************
#****************commandes plats***********************************

Frame4= LabelFrame(root, text='LES PLATS',bd=2, font=('cooper black', 22, 'bold'), fg='gold', bg='#5454FF')
Frame4.place(x=914, y=180, width=440,height=330)
def clear_selectionP(index):
    optionsP_vars[index].set("")  

def show_selectionsP():
    selected_table=table_var.get()
    if not selected_table:
        messagebox.showerror("Erreur", "Veuillez choisir un numero de table.")
    else:
        selections = []
        for i, var in enumerate(optionsP_vars.values()):
            if var.get() == 1:
                namePlats = list(optionsP.keys())[i]
                pricePlats = optionsP[namePlats]
                quantityPlats = quantityPlats_entries[i].get()
                if not quantityPlats:
                    messagebox.showerror("Erreur", "Veuillez entrer une quantite pour l'option '{}'.".format(namePlats))
                else:
                    selections.append((namePlats, pricePlats, quantityPlats))
        if selections:
            show_selections_window(selections)
totalP_labelP=None
def show_selectionsP_window(selections):
    global totalP_labelP
    selected_table = table_var.get()
    selections_window = tk.Toplevel(Frame4)
    selections_window.title("Sélections")
    selections_frame = ttk.Frame(selections_window)
    selections_frame.pack(padx=10, pady=10)
    totalP_labelP = ttk.Label(selections_frame, text="Total: 0 dh")
    totalP_labelP.grid(row=len(selections)+1, column=1, columnspan=2, padx=5, pady=5)
    ttk.Label(selections_frame, text=f"Numero de table : {selected_table}").grid(row=0, column=3, columnspan=2, padx=5, pady=5) # Obtenir la valeur sélectionnée dans la combobox
    ttk.Label(selections_frame, text="Plats").grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(selections_frame, text="Prix").grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(selections_frame, text="Quantite").grid(row=0, column=2, padx=5, pady=5)

    for i, (namePlats, pricePlats, quantityPlats) in enumerate(selections):
        ttk.Label(selections_frame, text=namePlats).grid(row=i+1, column=0, padx=5, pady=5)
        ttk.Label(selections_frame, text=pricePlats).grid(row=i+1, column=1, padx=5, pady=5)
        ttk.Label(selections_frame, text=quantityPlats).grid(row=i+1, column=2, padx=5, pady=5)
    def calculate_totalP():
        totalP = 0
        for _, pricePlats, quantityPlats in selections:
            totalP += int(pricePlats) * int(quantityPlats)
        totalP_labelP.config(text=f"TotalP: {totalP} dh")
    ttk.Button(selections_frame, text="Calculer Total", command=calculate_totalP).grid(row=len(selections)+2, column=1, columnspan=2, padx=5, pady=5)
    for i, (namePlats, pricePlats, quantityPlats) in enumerate(selections):
        ttk.Label(selections_frame, text=namePlats).grid(row=i+1, column=0, padx=5, pady=5)
        ttk.Label(selections_frame, text=pricePlats).grid(row=i+1, column=1, padx=5, pady=5)
        ttk.Label(selections_frame, text=quantityPlats).grid(row=i+1, column=2, padx=5, pady=5)
def clear_all_selectionsP():
    for var in optionsP_vars.values():
        var.set(0)
    for entry in quantityPlats_entries.values():
        entry.delete(0, tk.END)

optionsP_frame = ttk.Frame(Frame4)
optionsP_frame.pack(pady=10)
# Create a custom style with the desired background color
style = ttk.Style()
style.configure("Options.TFrame", background='#5454FF')
optionsP_frame.configure(style="Options.TFrame")



conn = sqlite3.connect("BDplats.db")
cursor = conn.cursor()
optionsP = {}
optionsP_vars = {}
quantityPlats_entries = {}

for row in cursor.execute("SELECT name, prix FROM plats"):
    namePlats = row[0]
    pricePlats = row[1]
    optionsP[namePlats] = pricePlats
    var = tk.IntVar()
    optionsP_vars[list(optionsP.keys()).index(namePlats)] = var
    clear_button = ttk.Button(optionsP_frame, text="Annuler", command=lambda index=list(optionsP.keys()).index(namePlats): clear_selectionP(index))
    clear_button.grid(row=list(optionsP.keys()).index(namePlats), column=0, padx=10)
    option_radio = ttk.Radiobutton(optionsP_frame, text=f"{namePlats} {pricePlats} dh", variable=var, value=1, style="Custom.TRadiobutton")
    option_radio.grid(row=list(optionsP.keys()).index(namePlats), column=1, sticky=tk.W)
    quantityPlats_label = ttk.Label(optionsP_frame, text=f"Quantite :")
    quantityPlats_label.configure(background='#5454FF', font=("Helvetica", 12)) # Set the font for the label
 
    quantityPlats_label.grid(row=list(optionsP.keys()).index(namePlats), column=2, padx=10)
    quantityPlats_entry = ttk.Entry(optionsP_frame,width=5)
    quantityPlats_entry.grid(row=list(optionsP.keys()).index(namePlats), column=3)
    quantityPlats_entries[list(optionsP.keys()).index(namePlats)] = quantityPlats_entry

conn.close()


# Définir les valeurs disponibles dans la combobox


show_selections_button = tk.Button(canvas,height=1,width=36,bd=2,relief=GROOVE,font=('times new roman',16,'bold'),bg='gold', text="Afficher les commandes Salades Sélections",command=show_selectionsP)
show_selections_button.place(x=914, y=520)

clear_all_button = tk.Button(canvas,height=1,width=36,bd=2,relief=GROOVE,font=('times new roman',16,'bold'),bg='blue', text="Effacer les commandes Salades Sélections", command=clear_all_selectionsP)
clear_all_button.place(x=914, y=565)

#***********************************

#Facture 


#buttons

        #total_btn=Button(canvas,text='Total',command=total,width=17,bd=2,relief=GROOVE,font=('times new roman',16,'bold'),bg='green').place(x=470,y=550)
        #Gfacture_btn=Button(canvas,text='Generer Facture',command=Generer_Facture,width=17,bd=2,relief=GROOVE,font=('times new roman',16,'bold'),bg='#5454FF').place(x=760,y=550)
        #Reini_btn=Button(canvas,text='Reintialiser',command=Reintialiser,width=17,bd=2,relief=GROOVE,font=('times new roman',16,'bold'),bg='white').place(x=470,y=610)
        #sav_btn=Button(canvas,text='Confirme la Demande',command=sauvegarder,width=17,bd=2,relief=GROOVE,font=('times new roman',16,'bold'),bg='yellow').place(x=760,y=610)
      


########################################
def quitter():
    op=messagebox.askyesno("Quitter","Vouez-vous quitter?")
    if op>0:
        root.destroy()



#-----------------------------------------------------------------------
def open_remarque_window():
    def enregistrer_remarque():
        remarque = text_remarque.get("1.0", "end-1c")  # Obtenir le texte de la remarque
        if not remarque:
            messagebox.showerror("Erreur", "Veuillez saisir une remarque")
            return
        try:
            # Ajouter la remarque dans un fichier CSV
            with open("remarques.csv", mode="a", newline="") as fichier_csv:
                writer = csv.writer(fichier_csv)
                writer.writerow([remarque])
            messagebox.showinfo("Succès", "La remarque a été enregistrée")
            remarque_window.destroy()  # Fermer la fenêtre de remarque après l'enregistrement
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'enregistrement de la remarque : {e}")

    remarque_window = tk.Toplevel(root)
    remarque_window.title('Restaurant - Remarque')
    remarque_window.geometry('450x300')

    # Ajouter un champ de texte pour saisir la remarque
    label_remarque = Label(remarque_window, text="Remarque :", font=('cooper black', 20, 'bold'), fg='gold')
    label_remarque.place(x=0, y=0)
    text_remarque = Text(remarque_window, width=50, height=10)
    text_remarque.place(x=20, y=50)

    # Ajouter un bouton pour enregistrer la remarque
    button_enregistrer = Button(remarque_window, width=8, bd=2, relief=tk.GROOVE, font=('times new roman', 15, 'bold'),
                                text="Enregistrer", bg='green', command=enregistrer_remarque)
    button_enregistrer.place(x=80, y=250)
    button_quitter = Button(remarque_window, width=8, bd=2, relief=tk.GROOVE, font=('times new roman', 15, 'bold'),
                            text="Quitter", bg="red", command=remarque_window.destroy)
    button_quitter.place(x=250, y=250)        

 
Quiter_btn=Button(canvas,text='Quiter',command=quitter,width=8,bd=2,relief=GROOVE,font=('times new roman',20,'bold'),bg='red').place(x=1218,y=120)
Remarque_RQ=Button(canvas,text='Remarque',command=open_remarque_window,width=8,bd=2,relief=GROOVE,font=('times new roman',20,'bold'),bg='green',fg='white').place(x=1075,y=120)

###############################confirme le commande#################
def send_selections():
    selected_table = table_var.get()
    selections = []
    empty_quantities = []
    
    if not selected_table:
        messagebox.showerror("Erreur", "Veuillez entrer une num table pour l'option")
    else:
        for i, var in enumerate(optionsB_vars.values()):
            if var.get() == 1:
                nameBoisson = list(options.keys())[i]
                priceBoisson = options[nameBoisson]
                quantityBoisson = quantityBoisson_entries[i].get()
                if not quantityBoisson:
                    messagebox.showerror("Erreur", "Veuillez entrer une quantite pour l'option '{}'.".format(nameBoisson))
                    empty_quantities.append(nameBoisson)
                    optionsB_vars[i].set("")
                    continue
                else:
                    selections.append({'Nom': nameBoisson, 'Prix': priceBoisson, 'Quantite': quantityBoisson})
        
        for i, var in enumerate(optionsS_vars.values()):
            if var.get() == 1:
                nameSalade = list(optionsS.keys())[i]
                priceSalade = optionsS[nameSalade]
                quantitySalade = quantitySalade_entries[i].get()
                if not quantitySalade:
                    messagebox.showerror("Erreur", "Veuillez entrer une quantite pour l'option '{}'.".format(nameSalade))

                    empty_quantities.append(nameSalade)
                    optionsS_vars[i].set("")
                    continue
                else:
                    selections.append({'Nom': nameSalade, 'Prix': priceSalade, 'Quantite': quantitySalade})
        
        for i, var in enumerate(optionsP_vars.values()):
            if var.get() == 1:
                namePlats = list(optionsP.keys())[i]
                pricePlats = optionsP[namePlats]
                quantityPlats = quantityPlats_entries[i].get()
                if not quantityPlats:
                    messagebox.showerror("Erreur", "Veuillez entrer une quantite pour l'option '{}'.".format(namePlats))
                    empty_quantities.append(namePlats)
                    optionsP_vars[i].set("")
                    continue
                else:
                    selections.append({'Nom': namePlats, 'Prix': pricePlats, 'Quantite': quantityPlats})
        
        if not selections:
            messagebox.showerror("Erreur", "Aucune sélection n'a été faite.")
        else:
            # Récupérer le numero de table
            num_table = {'Numero de Table': selected_table}
            
            # Ajouter la date actuelle à chaque commande
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for selection in selections:
                selection.update({'Date': current_date})
            
            # Demander à l'utilisateur s'il veut sauvegarder les commandes
# Demander à l'utilisateur s'il veut sauvegarder les commandes
            save = messagebox.askyesno("Sauvegarde", "Voulez-vous sauvegarder les commandes sans modifier  ?")
            if save:
                # Ouvrir la boîte de dialogue "Enregistrer sous" pour que l'utilisateur puisse choisir l'emplacement et le nom du fichier
                
                # Vérifier si le fichier existe déjà
                file_exists = os.path.isfile("commandes.csv")

                # Écrire les en-têtes du fichier CSV s'ils n'existent pas encore
                with open("commandes.csv", 'a', newline='') as csvfile: 
                    fieldnames = ['Nom', 'Prix', 'Quantite', 'Numero de Table', 'Date']  # Ajouter 'Date' comme nom de colonne
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    if not file_exists:
                        writer.writeheader()
                    
                # Inclure le numero de table et la date à la fin de la liste selections uniquement s'ils n'ont pas déjà été inclus
                for selection in selections:
                    if 'Numero de Table' not in selection:
                        selection.update(num_table)
                    if 'Date' not in selection:
                        selection.update({'Date': current_date})
                            
                # Vérifier si l'utilisateur souhaite sauvegarder les commandes dans un fichier
                save_to_file = messagebox.askyesno("Sauvegarder", "Voulez-vous confirme les commandes  ?")
                if save_to_file:
                    # Demander le nom du fichier à l'utilisateur

                    with open("commandes.csv", 'a', newline='') as csvfile: 
                        fieldnames = ['Nom', 'Prix', 'Quantite', 'Numero de Table', 'Date']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                        if not file_exists:
                            writer.writeheader()
                            
                        for selection in selections:
                            selection.update(num_table)
                            selection.update({'Date': current_date})
                            writer.writerow(selection)
                            clear_all_selections()
                            clear_all_selectionsB()
                            clear_all_selectionsP()
                else:
                    messagebox.showinfo("Information", "Les commandes n'ont pas été sauvegardées.")
                    
                # Effacer les sélections après la sauvegarde
                clear_all_selections()
                clear_all_selectionsB()
                clear_all_selectionsP()




Btn_Valide= tk.Button(canvas,text="CONFIRME LES COMMANDES", command=send_selections,width=30,bd=2,relief=GROOVE,font=('cooper black', 22, 'bold'),bg='green',fg='white').place(x=360,y=630)



root.mainloop()




