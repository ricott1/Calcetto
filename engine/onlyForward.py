import random
def move(pos, matrix, turn):
    moves = matrix[pos[0]][pos[1]]
    print 'ball is in ',pos, ' where could go to', moves
    forward = [m for m in moves if m[1] == (-1)**turn]
    if forward:
        return random.sample(forward,1)[0]
    else:
	   return random.sample(moves,1)[0]
	