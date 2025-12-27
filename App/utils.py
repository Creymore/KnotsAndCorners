import math

def arraySum(A):
	sum = 0
	for i in A:
		sum = i + sum
	return sum

def isFCfile(path)->bool:
	if str(path).endswith(".FCStd"):
		return True
	return False

def getDirection(edge):
	return (edge.Vertexes[0].Point - edge.Vertexes[1].Point).normalize()