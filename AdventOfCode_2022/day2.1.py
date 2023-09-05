f = open('file.txt', 'r')

def game(play):
    if play in ('A X', 'B Y', 'C Z'):
        return ('equal', play[0], play[-1])
    elif play in ('A Z', 'C Y', 'B X'):
        return ('p1', play[0])
    else:
        return ('p2', play[-1])

player1 = player2 = 0
point = {'A':1, 'B':2, 'C':3,
        'X':1, 'Y':2, 'Z':3}

for line in f:
    play = line.rstrip('\n')
    win = game(play)[0]
    if win == 'equal':
        player1 += 3 + point[game(play)[1]]
        player2 += 3 + point[game(play)[2]]
    elif win == 'p1':
        player1 += point[game(play)[1]] + 6
    else:
        player2 += point[game(play)[1]] + 6

f.close()

print(player1, player2)
