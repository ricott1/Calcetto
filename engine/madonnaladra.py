import random
def move(pos, matrix):
	print 'ball is in ',pos, ' where could go to', matrix[pos[0]][pos[1]]
	go = random.sample(matrix[pos[0]][pos[1]],1)[0]
	print 'madonna wants to ',go
	return go
