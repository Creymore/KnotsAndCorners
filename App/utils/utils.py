import math
from collections import Counter
import FreeCAD as App

def isFCfile(path)->bool:
	if str(path).endswith(".FCStd"):
		return True
	return False

def getDirection(edge):
	return (edge.Vertexes[0].Point - edge.Vertexes[1].Point).normalize()

def VecToTuple(FreeCADvector):
	return (
		FreeCADvector.x,
		FreeCADvector.y,
		FreeCADvector.z
	)

def copyVec(Vec):
	return App.Vector(
		Vec.x,
		Vec.y,
		Vec.z
	)

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

def ReplaceProfile(Body,NewProflie):

	#Finds the Pad to Replace the Profile in:

	def isProfile(obj):
		obj.Name == "Pad"
		obj.Label == "Profile"
	
	Pad = list(filter(isProfile,Body.Group))[0]

	OldSketch = Pad.Profile
	OldSketch = NewProflie

	pass