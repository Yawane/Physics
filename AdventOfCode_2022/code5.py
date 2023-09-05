f = open('file5.txt', 'r')

D = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
E = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}

for i in range(8):
    L = f.readline()
    for j in range(0, 36, 4):
        if L[j+1] != ' ':
            D[j//4].append(L[j+1])
            E[j//4].append(L[j+1])

f.readline()
f.readline()
for line in f:
    A = []
    A.append(int(line[5:7]))    # quantité
    A.append(int(line[12:14])-1)  # n° départ
    A.append(int(line[-2:])-1)    # n° arrivée
    
    B = D[A[1]][:A[0]]
    B.reverse()
    
    D[A[2]] = B + D[A[2]]
    E[A[2]] = E[A[1]][:A[0]] + E[A[2]]
    
    D[A[1]] = D[A[1]][A[0]:]
    E[A[1]] = E[A[1]][A[0]:]
f.close()


for i in range(9):
    print(D[i][0], end="")
    
print()

for i in range(9):
    print(E[i][0], end="")