def end(sequence):
    """Renvoie True si la séquence est toute différente --> On arrete de compter
    Renvoie False s'il faut continuer à compter"""
    for c in sequence:
        if sequence.count(c) != 1:
            return False
    return True


f = open('file6.txt', 'r')

line = f.readline()
n = m = 0  # n:Partie 1 ; m:Partie 2

PART1 = PART2 = True  # Je n'utilise pas break car elle arrete la boucle for. Ne permet pas de continuer pour la 2nd partie.
for i in range(len(line)):
    if PART1:  # Si la partie 1 n'est pas fini, alors faire
        if end(line[i:i+4]):
            n += 4
            PART1 = False  # Fin de la partie 1
        else:
            n += 1
            
    if PART2:
        if end(line[i:i+14]):
            m += 14
            PART2 = False
        else:
            m += 1

f.close()