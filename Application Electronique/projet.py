import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image



# %% Config générale
#  Tkinter app ---------------------------------
root = tk.Tk()
root.title("Calculateur de Résistance")
root.state('zoomed')
root.minsize(1057, 744)



# On définit les 3 Frames qui vont constituer les 3 pages de l'application
START = tk.Frame(root)
APP1 = tk.Frame(root)
APP2 = tk.Frame(root)

# le style qui s'applique à tout les ttk.
style = ttk.Style()
style.configure('TLabel', font=12)
style.configure('TButton', font=12)
style.configure('TEntry', font=12)
style.configure('TMenubutton', font=12)
style.configure('TEntry', font=12)
style.configure('TCheckbutton', font=12)

style.configure('Title.TLabel', font=('Arial black', 40, 'bold'))
style.configure('Quit.TLabel', font=('Arial black', 11, 'bold'), foreground='red')
style.configure('Return.TLabel', font=('Arial black', 11, 'bold'), foreground='blue')
style.configure('App.TButton', font=('Arial black', 35, 'bold'))
style.configure('Result.TLabel', font=('Chillax', 13))



# fonctions pour naviger à travers les pages de l'app
def to_start():
    APP1.pack_forget()
    APP2.pack_forget()
    START.pack(expand=True, side='bottom', pady=30, padx=30)

def to_app1():
    START.pack_forget()
    APP1.pack(expand=True, fill='both', side='bottom', pady=10, padx=10)

def to_app2():
    START.pack_forget()
    APP2.pack(expand=True, fill='both', side='bottom', pady=10, padx=10)

# ------------Grid configure weight--------------------
for i in range(3):
    APP1.columnconfigure(i, weight=1)
for i in range(7):
    APP1.rowconfigure(i, weight=1)
    
APP2.columnconfigure(0, weight=1)
for i in range(3):
    APP2.rowconfigure(i, weight=1)
APP2.rowconfigure(3, weight=5)
APP2.rowconfigure(4, weight=5)

# les Label et Button qui restent constamment sur la page
rootframe = tk.Frame(root)
ttk.Button(rootframe, text="retour", command=to_start, style='Return.TLabel').pack(expand=True, side='left', anchor='nw')
ttk.Label(rootframe, text="RESISTANCE CALCULATOR", style='Title.TLabel').pack(expand=True, side='left', padx=50, pady=(0,50))
ttk.Button(rootframe, text="quitter", command=root.destroy, style='Quit.TLabel').pack(expand=True, side='left', anchor='ne')





# %% START
ttk.Label(START, text="Choisir le nombre de résistances", font=('Chillax', 25, 'bold')).grid(row=0, column=0, columnspan=2, pady=30)
ttk.Button(START, text="2 ou 3", command=to_app1, style='App.TButton').grid(row=1, column=0, sticky='nsew')
ttk.Button(START, text="∞", command=to_app2, style='App.TButton').grid(row=1, column=1)


 
#%% APP2
def parallele(a, b):
    "Renvoie la valeur de 2 résistances en parallèles"
    a = float(a)
    b = float(b)
    return a * b / (a + b)


def calcul(A):
    """Cette fonction définit les relations de priorités entre + et //. 2 R en parallèles étant prioritaire sur la série, c'est undispensable.
    Renvoie le résultat final et modifie le Label pour mettre la réponse à jour."""
    s = 0
    B = A.split(' + ') # On identifie les groupes de résistance en série et en dérivation
    try:
        for c in B:
            if len(c) == 1:
                s += float(c) # si en série alors simplement ajouter
            else: # on calcule le résultat des résisances en dérivations
                L = c.split(' // ')
                a = float(L[0])
                for i in range(1, len(L)):
                    a = parallele(a, float(L[i]))
                s += a # on ajoute  le résultat des dérivations au résultat final
        result['text'] = round(s, 3) if unit_var2.get() == 'Ω' else round(s/1000, 3)
        return s # On a calculé Req en tenant compte des priorités de calcul de la dérivation
    except:
        result['text'] = 'Valeurs incorrectes'


def validate():
    "Reçoit les valeurs des Résistances, calcule Req et affiche sur le Label."
    n = var_nbr_resistance.get()
    R = []
    V = []
    A = ""
    for i in range(n):
        R.append(R_entry[f'{i+1}_var'].get())
        if i < n-1:
            V.append(R_option[f'{i}_var'].get())

    for i in range(len(V)):
        A += f'{R[i]} {V[i]} '
    A += R[-1]
    print(A)
    total = calcul(A)
    print('Calcul lancé !', 'Req =', total)


#------------------- Affichage-----------------------
def unit2(event):
    validate()

def display_R(n):
    "Affiche les résistances disponibles et les menus déroulants pour choisir + ou //"
    for j in range(1, 21): # retire tout
        try:
            R_labels[f'{j}_option'].grid_remove()
            R_option[f'{j}_option'].grid_remove()
        except:
            pass

    for i in range(n): # affiche uniquement les résistances demandées
        R_labels[f'{i}_option'] = ttk.Label(frame2, text=f'R{i+1}')
        R_labels[f'{i}_option'].grid(row=0, column=i*2, sticky='nsew')
        if i < n-1:
            R_option[f'{i}_var'] = tk.StringVar()
            R_option[f'{i}_option'] = ttk.OptionMenu(frame2, R_option[f'{i}_var'], '+', *['//', '+'])
            R_option[f'{i}_option'].grid(row=0, column=i*2+1, sticky='nsew')

    display_entry(n) # fonction qui affiche la suite


def display_entry(n):
    "affiche les entrées demandées"
    unit2_label.grid(row=n+2, column=0, sticky='nse')
    unit2.grid(row=n+2, column=1, sticky='nsw')
    line.grid(row=n+3, column=0, columnspan=3, sticky='nsew')
    result_label.grid(row=n+4, column=0, sticky='nse')
    result.grid(row=n+4, column=1, sticky='nsw')
    for j in range(1, 21): # retire tout les .grid
        try:
            R_entry[f'{j}_entry'].grid_forget()
            R_labels[f'{j}_entry'].grid_forget()
        except:
            pass

    for i in range(1, n+1): # affiche uniqiuement les entrées demandées
        R_labels[f'{i}_entry'] = ttk.Label(frame3, text=f'Entrez la résistance n°{i}')
        R_labels[f'{i}_entry'].grid(row=i+1, column=0, sticky='nsew')
        R_entry[f'{i}_var'] = tk.StringVar(value=str(i))
        R_entry[f'{i}_entry'] = ttk.Entry(frame3, textvariable=R_entry[f'{i}_var'])
        R_entry[f'{i}_entry'].grid(row=i+1, column=1, sticky='nsew')


frame1 = tk.Frame(APP2)
frame2 = tk.Frame(APP2)
frame3 = tk.Frame(APP2)
frame4 = tk.Frame(APP2)

for i in range(9):
    frame3.rowconfigure(i, weight=1)


R_option = dict()
R_entry = dict()
R_labels = dict()
#  End config -----------------------------------

#  Start parameter
ttk.Label(frame1, text='Choisir le nombre de résistances dans le circuit.', font=('Poppins', 15, 'bold')).grid(row=0, column=0, sticky='nsew', pady=10)

var_nbr_resistance = tk.IntVar() # va contenir le nombre de résistance voulu pour le calcul
option_nbr_resistance = ttk.OptionMenu(frame1, var_nbr_resistance, 4, *range(2, 21), command=display_R)


#  End parameter

# ------FRAME_3---------------------
ttk.Label(frame3, text="Remplissez les champs. Seuls les nombres sont autorisés.", font=('Poppins', 12, 'bold')).grid(row=0, column=0, columnspan=100)
#ttk.Label(frame3, text="Unité d'entrée :").grid(row=1, column=0, sticky='nse')
unit2_label = ttk.Label(frame3, text="Unité résultat :")

#unit_var1 = tk.StringVar() # unité d'entrée des Résistances
#unit1 = ttk.OptionMenu(frame3, unit_var1, 'Ω', *['kΩ', 'Ω'])
#unit1.grid(row=1, column=1, sticky='nsw')

unit_var2 = tk.StringVar() # unitée de sortie des Résistances (résultat)
unit2 = ttk.OptionMenu(frame3, unit_var2, 'Ω', *['kΩ', 'Ω'], command=unit2)

line = ttk.Separator(frame3, orient='horizontal')

result_label = ttk.Label(frame3, text='Req =', style='Result.TLabel')
result = ttk.Label(frame3, text='')
# ------FRAME_4---------------------

ttk.Button(frame4, text='valider', command=validate).grid(row=1, column=0, sticky='nsew') # Button qui lance  le calcul




# ----------------GRID-------------------- On grid tout ce qu'on peut
option_nbr_resistance.grid(row=0, column=1, sticky='nsew')
frame1.grid(row=1, column=0)
frame2.grid(row=2, column=0)
frame3.grid(row=3, column=0, sticky='ns')
frame4.grid(row=4, column=0)

display_R(4) # mise en page par défaut

# %% APP1

def unit(event):
    valider()



def valider():
    """La fonction calcule la valeur de Req en fonciton de l'image selectionnée (i) et en déduit le courant qui la traverse,
    Puis modifie de text de réponse (Req_label) pour afficher le résultat à 3 décimales près."""
    print('calcul lancé')
    print(root.winfo_width(), root.winfo_height())
    i = radio_var.get() # la valeur de l'image selectionnée.
    r1 = APP1_entry["1_var"].get()
    r2 = APP1_entry["2_var"].get()
    print(i, type(i))
    
    try: # si on veut en kΩ, on multiplie r par 1000 pour rester en SI quoi qu'il arrive
        r1 = float(r1) if APP1_option["1_var"].get() == 'Ω' else float(r1) * 1000
        r2 = float(r2) if APP1_option["2_var"].get() == 'Ω' else float(r2) * 1000
        if i != 1 and i != 2:
            print('oui ok')
            r3 = APP1_entry["3_var"].get()
            r3 = float(r3) if APP1_option["3_var"].get() == 'Ω' else float(r3) * 1000
    except:
        Req_label['text'] = 'Valeur incorrecte'
        return None
    
    if i == 1:
        r = serie(r1, r2)
        Req_label['text'] = round(r, 3) if R_var.get() == 'Ω' else round(r/1000, 3) # on divise le résultat par 1000 si on veut en kΩ
    elif i == 2:
        r = parallele1(r1, r2)
        Req_label['text'] = round(r, 3) if R_var.get() == 'Ω' else round(r/1000, 3)
    elif i == 3:
        r = serie(serie(r1, r2), r3)
        Req_label['text'] = round(r, 3) if R_var.get() == 'Ω' else round(r/1000, 3)
    elif i == 4:
        r = serie(r1, parallele1(r1, r2))
        Req_label['text'] = round(r, 3) if R_var.get() == 'Ω' else round(r/1000, 3)
    elif i == 5:
        r = parallele1(serie(r1, r2), r3)
        Req_label['text'] = round(r, 3) if R_var.get() == 'Ω' else round(r/1000, 3)
    elif i == 6:
        r = parallele1(parallele(r1, r2), r3)
        Req_label['text'] = round(r, 3) if R_var.get() == 'Ω' else round(r/1000, 3)
    
    
    
        
    if check_var.get():
        try:
            u = float(tension_var.get())
            if E_unit_var.get() == 'mV':
                u /= 1000
            elif E_unit_var.get() == 'kV': # Si on a séléctionné kV, on multiplie par 1000
                u *= 1000
            # Avant de faire le calcul, on met la tension en unité SI
            
            if I_var.get() == 'mA':
                I_label['text'] = round(u / r * 1000, 3)
            elif I_var.get() == 'A':
                I_label['text'] = round(u / r, 3)
            elif I_var.get() == 'kA':
                I_label['text'] = round(u / r / 1000, 3)
            elif I_var.get() == 'µA':
                I_label['text'] = round(u / r * 1e6, 3)
        except:
            I_label['text'] = 'Valeurs incorrectes'


def serie(r1, r2):
    "Calcul de Req pour 2 résistances en série"
    return r1 + r2


def parallele1(r1, r2):
    "Calcul de Req pour 2 résistances en dérivation"
    return r1 * r2 / (r1 + r2)


def radio_maj(i):
    "Met à jour les RadioButton et affiche le schéma complet de l'élément séléctionné."
    radio_var.set(i)
    test['text'] = i
    img_label['image'] = big_img[i]
    
    if i == 1 or i == 2:
        APP1_entry["3_entry"]['state'] = 'disabled'
    else:
        APP1_entry["3_entry"]['state'] = 'normal'


def check_maj():
    "Affiche ou pas le Entry correspondant à l'entrée de la source de tension."
    if check_var.get():
        tension_entry['state'] = 'normal'
        I_option['state'] = 'normal'
        E_unit['state'] = 'normal'
    else:
        tension_entry['state'] = 'disabled'
        I_option['state'] = 'disabled'
        E_unit['state'] = 'disabled'
    
    

ttk.Label(APP1, text="Séléctionner le montage et entrer les valeurs.", font=('Chillax', 17, 'bold')).grid(row=0, column=0, columnspan=3)

APP1frame = tk.Frame(APP1) # sous Frame qui contient les entrées, le bouton calcul, et les résultats


small_img = dict() #  On stocke tout dans des dictioinnaires pour simplifier la syntaxe et pour mieux retrouver une variable
big_img = dict()
radio = dict()
buttons = dict()
radio_var = tk.IntVar(value=3)  # contient le numéro de l'image cliqué

for i in range(1, 7):  # Création et stockage en image des schémas simplifiés et complets (avec PIL)
    a = Image.open(f"--img{i}.png")
    b = a.resize((400,80), Image.ANTIALIAS)
    c = ImageTk.PhotoImage(b)
    small_img[i] = c
    
    A = Image.open(f"_img{i}.png")
    B = A.resize((600,338), Image.ANTIALIAS)
    C = ImageTk.PhotoImage(B)
    big_img[i] = C

# création des Button et Radio avec les images, reliés à la fonciton radio_maj
buttons[1] = ttk.Button(APP1, image=small_img[1], command=lambda:radio_maj(1))
buttons[2] = ttk.Button(APP1, image=small_img[2], command=lambda:radio_maj(2))
buttons[3] = ttk.Button(APP1, image=small_img[3], command=lambda:radio_maj(3))
buttons[4] = ttk.Button(APP1, image=small_img[4], command=lambda:radio_maj(4))
buttons[5] = ttk.Button(APP1, image=small_img[5], command=lambda:radio_maj(5))
buttons[6] = ttk.Button(APP1, image=small_img[6], command=lambda:radio_maj(6))

radio[1] = ttk.Radiobutton(APP1, variable=radio_var, value=1)
radio[2] = ttk.Radiobutton(APP1, variable=radio_var, value=2)
radio[3] = ttk.Radiobutton(APP1, variable=radio_var, value=3)
radio[4] = ttk.Radiobutton(APP1, variable=radio_var, value=4)
radio[5] = ttk.Radiobutton(APP1, variable=radio_var, value=5)
radio[6] = ttk.Radiobutton(APP1, variable=radio_var, value=6)
    

# ---------------------- FRAME ------------------------------

APP1_entry = dict()
APP1_option = dict()
for i in range(1, 4): # création des champs d'entrée et menu déroulant pour les unités
    ttk.Label(APP1frame, text=f"R{i} =").grid(row=i-1, column=0)
    APP1_entry[f"{i}_var"] = tk.StringVar()
    APP1_entry[f"{i}_entry"] = ttk.Entry(APP1frame, textvariable=APP1_entry[f"{i}_var"])
    APP1_entry[f"{i}_entry"].grid(row=i-1, column=1)
    
    APP1_option[f"{i}_var"] = tk.StringVar()
    APP1_option[f"{i}_option"] = ttk.OptionMenu(APP1frame, APP1_option[f"{i}_var"], "Ω", *['kΩ', 'Ω'], command=unit)
    APP1_option[f"{i}_option"].grid(row=i-1, column=2)



ttk.Button(APP1frame, text='Calculer', command=valider).grid(row=3, column=0, columnspan=3)
ttk.Separator(APP1frame, orient='vertical').grid(row=0, column=3, rowspan=5, sticky='ns')


check_var = tk.BooleanVar() # pour savoir si on souhaite étudier le circuit complet ou si Req suffis
check = ttk.Checkbutton(APP1frame, text="Etude complète", variable=check_var, onvalue=True, offvalue=False, command=check_maj)

ttk.Label(APP1frame, text='E =').grid(row=1, column=4, sticky='e')
tension_var = tk.StringVar()
tension_entry = ttk.Entry(APP1frame, textvariable=tension_var, state='disabled')

ttk.Label(APP1frame, text='Req =').grid(row=2, column=4, sticky='e')
ttk.Label(APP1frame, text='I =').grid(row=3, column=4, sticky='e')
Req_label = ttk.Label(APP1frame, text='', style='Result.TLabel') # va contenir le résustat de Req
I_label = ttk.Label(APP1frame, text="off", style='Result.TLabel')

R_var = tk.StringVar()
APP1_R_option = ttk.OptionMenu(APP1frame, R_var, "Ω", *['kΩ', 'Ω'], command=unit) # menu déroulant pour choisir l'unité
I_var = tk.StringVar()
I_option = ttk.OptionMenu(APP1frame, I_var, "A", *['kA', 'A', 'mA', 'µA'], command=unit)

E_unit_var = tk.StringVar()
E_unit = ttk.OptionMenu(APP1frame, E_unit_var, "V", *['kV', 'V', 'mV'], command=unit)

img_label = ttk.Label(APP1, image=big_img[3])

# ----------------- GRID ---------------------------
# On grid tout ce qu'onn peut

buttons[1].grid(row=1, column=0, sticky='nsew')
buttons[2].grid(row=2, column=0, sticky='nsew')
buttons[3].grid(row=3, column=0, sticky='nsew')
buttons[4].grid(row=4, column=0, sticky='nsew')
buttons[5].grid(row=5, column=0, sticky='nsew')
buttons[6].grid(row=6, column=0, sticky='nsew')

radio[1].grid(row=1, column=1, sticky='w')
radio[2].grid(row=2, column=1, sticky='w')
radio[3].grid(row=3, column=1, sticky='w')
radio[4].grid(row=4, column=1, sticky='w')
radio[5].grid(row=5, column=1, sticky='w')
radio[6].grid(row=6, column=1, sticky='w')

test = ttk.Label(APP1, text=3)
test.grid(row=7, column=0, columnspan=2)
check.grid(row=0, column=4, columnspan=2, sticky='w')
tension_entry.grid(row=1, column=5)
E_unit.grid(row=1, column=6)
Req_label.grid(row=2, column=5, sticky='w')
APP1_R_option.grid(row=2, column=6, sticky='w')
I_label.grid(row=3, column=5, sticky='w')
I_option.grid(row=3, column=6, sticky='w')
    
APP1frame.grid(row=1, column=2, rowspan=2, sticky='ew')
img_label.grid(row=3, column=2, rowspan=4, sticky='nsew')

# %% General Grid


rootframe.pack(expand=False, fill='x') # ce qui reste constamment sur la page

START.pack(expand=True, side='bottom', pady=30, padx=30) # la page à ouvrir au lancement de l'app

check_maj()

root.mainloop()
