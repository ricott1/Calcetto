import random
def move(ball, matrix):
	print 'ball is in ',ball, ' where could go to', matrix[ball[0]][ball[1]]
	go = random.sample(matrix[ball[0]][ball[1]],1)[0]
	print 'madonna wants to ',go
	return go
