from PIL import Image, ImageTk
import random
import tkinter as tk
from tkinter import ttk


# %% Main Configuration
root = tk.Tk()
root.state('normal')

style = ttk.Style()
style.configure('TButton', foreground='black')
style.configure('Correct.TButton', foreground='green')
style.configure('False.TButton', foreground='red')

# %% Récupération des images
reference = {'Åland':'ax.png',
            'Albanie':'al.png',
            'Allemagne':'de.png',
            'Andorre':'ad.png',
            'Angleterre':'gb-eng.png',
            'Arménie':'am.png',
            'Autriche':'at.png',
            'Azerbaïdjan':'az.png',
            'Belgique':'be.png',
            'Biélorussie':'by.png',
            'Bosnie-Herzégovine':'ba.png',
            'Bulgarie':'bg.png',
            'Chypre':'cy.png',
            'Croatie':'hr.png',
            'Danemark':'dk.png',
            'Écosse':'gb-sct.png',
            'Espagne':'es.png',
            'Estonie':'ee.png',
            'Finlande':'fi.png',
            'France':'fr.png',
            'Géorgie':'ge.png',
            'Gibraltar':'gi.png',
            'Grèce':'gr.png',
            'Guernessey':'gg.png',
            'Hongrie':'hu.png',
            'Île de Man':'im.png',
            'Îles Féroé':'fo.png',
            'Irlande':'ie.png',
            'Irlande du Nord':'gb-nir.png',
            'Islande':'is.png',
            'Italie':'it.png',
            'Jersey':'je.png',
            'Kasakhstan':'kz.png',
            'Kosovo':'xk.png',
            'Lettonie':'lv.png',
            'Liechtenstein':'li.png',
            'Lituanie':'lt.png',
            'Luxembourg':'lu.png',
            'Macédoine du Nord':'mk.png',
            'Malte':'mt.png',
            'Moldavie':'md.png',
            'Monaco':'mc.png',
            'Monténégro':'me.png',
            'Norvège':'bv.png',
            'Pays de Galles':'gb-wls.png',
            'Pays-Bas':'nl.png',
            'Pologne':'ax.png',
            'Portugal':'pt.png',
            'Roumanie':'ro.png',
            'Royaume-Uni':'gb.png',
            'Russie':'ru.png',
            'Saint-Marin':'sm.png',
            'Serbie':'rs.png',
            'Slovaquie':'sk.png',
            'Slovénie':'si.png',
            'Suède':'se.png',
            'Suisse':'ch.png',
            'Tchéquie':'cz.png',
            'Turquie':'tr.png',
            'Ukraine':'ua.png',
            'Union européenne':'nf.png',
            'Vatican':'va.png',}

reference_test = {'Åland':'ax.png',
            'Albanie':'al.png',
            'Allemagne':'de.png',
            'Andorre':'ad.png',
            'Angleterre':'gb-eng.png',
            'Tchéquie':'cz.png',}


drapeaux = dict()

for r in reference:
    a = Image.open('img/img-reste/' + reference[r])
    w, h = a.size

    b = a.resize((250 * w // h, 250), Image.ANTIALIAS)
    c = ImageTk.PhotoImage(b)
    drapeaux[r] = c


# %% app1
app1 = ttk.LabelFrame(padding='1c', text='app1')
app1.pack(expand=True)


def start():
    global to_do, done
    to_do = set(drapeaux)
    done = set()


def check(v, selection, i):
    
    print(v == selection, v)
    print()
    if v == selection:
        score['text'] = 'score : ' + str(int(score['text'].split(': ')[-1]) + 1) # à tester avec +100 drapeaux
        if i == 1:
            button1['style'] = 'Correct.TButton'
        elif i == 2:
            button2['style'] = 'Correct.TButton'
        elif i == 3:
            button3['style'] = 'Correct.TButton'
        else:
            button4['style'] = 'Correct.TButton'
        root.after(200, suivant)
    else:
        heart['text'] = 'vie : ' + str(int(heart['text'].split(': ')[-1]) - 1) # à tester avec +100 drapeaux
        if i == 1:
            button1['style'] = 'False.TButton'
        elif i == 2:
            button2['style'] = 'False.TButton'
        elif i == 3:
            button3['style'] = 'False.TButton'
        else:
            button4['style'] = 'False.TButton'
    
    if int(heart['text'].split(': ')[-1]) == 0:
        print("T'AS PERDU NUL NUL NUL NUL NUL NUL NUL NUL NUL NUL NUL")
        


def suivant():
    button1['style'] = 'TButton'
    button2['style'] = 'TButton'
    button3['style'] = 'TButton'
    button4['style'] = 'TButton'
    print()
    choices = []
    print(f'reste : {len(to_do - done)}\n')
    choices.append(random.choice(list(to_do - done)))
    for i in range(3):
        choices.append(random.choice(list(set(drapeaux) - set(choices))))
    #choices = random.choices(list(drapeaux), k=3)
    
    
    result = choices[0]
    done.add(result)
    
    if to_do - done == set():
        start()
    
    flag['image'] = drapeaux[result]
    
    random.shuffle(choices)
    button1['text'], button1['command'] = choices[3], lambda:check(result, choices[3], 1)
    button2['text'], button2['command'] = choices[2], lambda:check(result, choices[2], 2)
    button3['text'], button3['command'] = choices[1], lambda:check(result, choices[1], 3)
    button4['text'], button4['command'] = choices[0], lambda:check(result, choices[0], 4)
    
    

score = ttk.Label(app1, text='score : 0')
heart = ttk.Label(app1, text='vie : 3')
flag = ttk.Label(app1)
button1 = ttk.Button(app1)
button2 = ttk.Button(app1)
button3 = ttk.Button(app1)
button4 = ttk.Button(app1)

score.grid(row=0, column=0, sticky='w')
heart.grid(row=0, column=1, sticky='e')
flag.grid(row=1, column=0, columnspan=2, pady=(0,20))
button1.grid(row=2, column=0, sticky='ew', ipady=7)
button2.grid(row=2, column=1, sticky='ew', ipady=7)
button3.grid(row=3, column=0, sticky='ew', ipady=7)
button4.grid(row=3, column=1, sticky='ew', ipady=7)

start()
suivant()


root.mainloop()