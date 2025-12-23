import math

def arraySum(A): # Move to utils
	sum = 0
	for i in A:
		sum = i + sum
	return sum


def isFCfile(path)->bool:
	if str(path).endswith(".FCStd"):
		return True
	return False
