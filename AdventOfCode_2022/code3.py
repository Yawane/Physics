f = open('file3.txt', 'r')
n = 0
m = 0

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
L = 0  # le numéro de la ligne (entre 1 et 3 pour la partie 2)

for line in f:
    #  Partie 2
    if L == 0:
        good = set(line.rstrip('\n'))  # ensemble qui contient toutes les lettres de ligne n°1
    elif L < 3:  # garde uniquement les lettres en commun
        good = good & set(line.rstrip('\n'))
    if L == 2:
        L = -1  # car il y a L += 1 plus tard
        m += ALPHABET.index(good.pop()) + 1  # il reste 1 element dans good, re récupère sa valeur
    # Partie 1
    b = line[(len(line))//2:-1]  # str qui à la 2nd moitié de la ligne
    for i in range((len(line)-1) // 2):  # i s'arrète à la moitié
        c = line[i]  # pour simplifier
        if c in b and c not in line[:i]:  # je vérifie que c n'a  jamais été ajouté à n pour éviter les doublons
            n += ALPHABET.index(c) + 1
    L += 1
f.close()
