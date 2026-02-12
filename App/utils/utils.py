import math

def isFCfile(path)->bool:
	if str(path).endswith(".FCStd"):
		return True
	return False

def getDirection(edge):
	return (edge.Vertexes[0].Point - edge.Vertexes[1].Point).normalize()

# Maybe this Belongs in Profile Logic section
def FindBinder(Body):
	Features = Body.Group

	for i in range(len(Features)):
		Feature = Features[i]
		if Feature.TypeId == 'PartDesign::SubShapeBinder':
			return Feature
	print("No Binder in Body")
	return False

# Binder.Support = doc.getObject('Sketch')

def CopieBetweenDoc():

	pass