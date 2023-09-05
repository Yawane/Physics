f = open('file7.txt', 'r')

D = {'/':[]}
for line in f:
    if line[0] == '$':
        if line[2:4].rstrip(' ') == 'cd':
            pwd = line[5:].rstrip('\n')
    
    D[pwd] = 4

f.close()