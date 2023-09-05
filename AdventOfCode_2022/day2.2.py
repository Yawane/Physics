f = open('file2.txt', 'r')

D = {'A X':4, 'A Y':8, 'A Z':3, 'B X':1, 'B Y':5, 'B Z':9, 'C X':7, 'C Y':2, 'C Z':6}
E = {'A X':3, 'A Y':4, 'A Z':8, 'B X':1, 'B Y':5, 'B Z':9, 'C X':2, 'C Y':6, 'C Z':7}

p1 = p2 = 0

for line in f:
    p1 += D[line.rstrip('\n')]
    p2 += E[line.rstrip('\n')]

f.close()

print(p1)
print(p2)
