import FreeCAD as App
import random
import json

def TransformKnot(K,axis,angle):
	rot = App.Rotation(axis,angle)
	n = -1
	while n < len(K): #Would be more elegant with a for Loop but i dont know how
		n = n+1
		V = K[f"P{n}"]["Direction"]
		V = rot.multVec(V)
		K[f"P{n}"].update({"Direction":V})
	return(K)

def GenerateVector(range=100,step=1):
	x = random.randrange(-range,range,step)
	y = random.randrange(-range,range,step)
	z = random.randrange(-range,range,step)
	return App.Vector(x,y,z)

def GenerateProfile(type="x",angle=0,sym=4):
	Profile = {
		"Direction": GenerateVector(),
		"Type": type,
		"Angle":angle,
		"n-fold_Symeterty":sym
	}
	return Profile

def GenerateKnot(proflies=3,type="x",angle=0,sym=4):
	knot = {}
	for i in range(proflies):
		knot.update({f"P{i}" : GenerateProfile()})
	return knot

def GenerateKnots(n=2):
	knots = {}
	for i in range(n):
		knots.update({f"Knot{i}":GenerateKnot()})
	return knots

def SaveKnots(dir="DummyKnots.json",knots):
	jknots = json.dumps(knots,indent=4)
	with open(dir,"w") as f:
		f.write(jknots)

def LoadKnot():
	
	pass

