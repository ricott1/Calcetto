import random
def move(pos, matrix, turn):
    moves = matrix[pos[0]][pos[1]]
    print 'ball is in ',pos, ' where could go to', moves
    return random.sample(moves,1)[0]
	

def __str__():
    return "Juda"