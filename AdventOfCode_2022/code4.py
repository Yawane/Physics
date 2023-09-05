result1 = result2 = 0

f = open('file4.txt', 'r')

for line in f:
    A = set(range(int(line.split(',')[0].split('-')[0]), int(line.split(',')[0].split('-')[1])+1))
    B = set(range(int(line.split(',')[1].split('-')[0]), int(line.split(',')[1].split('-')[1])+1))
    if A <= B or B <= A:
        result1 += 1
    if len(A & B) != 0:
        result2 += 1
f.close()