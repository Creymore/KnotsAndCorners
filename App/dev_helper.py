# The dev_helper is only supposed to help me Test my work
# Non of these Funtions should be used in the Main file in normal opperation

import FreeCAD as App
import FreeCADGui as Gui
import random
import json
from App.ChatGBTs_utils import print_dict
from App.ChatGBTs_utils import convert_vectors
from App.ChatGBTs_utils import convert_lists_to_vectors
import utils

def TransformKnot(Knot,axis,angle): # angle in deg
	rot = App.Rotation(axis,angle)
	n = 0
	while n < len(Knot): #Would be more elegant with a for Loop but i dont know how
		V = Knot[f"P{n}"]["Direction"]
		V = rot.multVec(V)
		Knot[f"P{n}"].update({"Direction":V})
		n = n+1
	return(Knot)

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

def GenerateKnot(proflies=5,type="x",angle=0,sym=4):
	knot = {}
	for i in range(proflies):
		knot.update({f"P{i}" : GenerateProfile()})
	return knot

def GenerateKnots(n=2):
	knots = {}
	for i in range(n):
		knots.update({f"Knot{i}":GenerateKnot()})
	return knots

def GenerateKnotPair(Knot):
	angle = random.randrange(-180,180,1)
	axis = GenerateVector()
	transformnedKnot = TransformKnot(Knot,axis,angle)
	return [transformnedKnot,Knot]

def FcVecToVecArray(V):
	v = [
		V.x,
		V.y,
		V.z
	]
	return v

def VecArrayToFcVec(V):
	v = App.Vector(V[0],V[1],V[2])
	return v

def SaveKnots(knots,dir="App/DummyKnots.json"):
	knots = convert_vectors(knots) # Somehow the FreeCAD Json does not like FreeCAD Vector Objects https://github.com/FreeCAD/FreeCAD/issues/25566
	jknots = json.dumps(knots,indent=4)
	with open(dir,"w") as f:
		f.write(jknots)

def LoadKnot(n=0,dir="App\DummyKnots.json"):
	with open(dir,"r") as f:
		data = json.load(f)
		try:
			data = data[f"Knot{n}"]
			data = convert_lists_to_vectors(data) # Needs converting back https://github.com/FreeCAD/FreeCAD/issues/25566
			return data
		except:
			print(f"Knot{n} does not exsit")
			return False
		


def GenerateDocTest(name,BASEPATH):
	
	doc = App.newDocument(name)
	mypart = doc.addObject('App::Part','Part') # Somehow need to make it visibal
	# Gui.getDocument(name).getObject("Part").Visibility = True
	# mypart.addProperty("App::PropertyString", "ThePropertyName", "Subsection", "Description for tooltip")
	mypart.addProperty("App::PropertyString", "KnotID", "KnotInformation", "This is the Knot ID")
	mypart.KnotID = "Tesrt"
	doc.recompute()

	path = f"{BASEPATH}/{name}"
	App.getDocument(name).saveAs(path)

def ReadKnotID(name,BASEPATH):
	path = f"{BASEPATH}/{name}.FCstd"
	open(path)
	doc = App.getDocument(name)
	mypart = doc.getObject("Part")
	KnotID = mypart.KnotID
	print(KnotID)
	pass

def loadBASEPATH(dir="APP/myPC.json"):
	with open(dir,"r") as f:
		data = json.load(f)
	return data

if __name__ == "__main__" :
	
	
	myBASEPATH = loadBASEPATH()

	myname = "TEST1"
	GenerateDocTest(name=myname,BASEPATH=myBASEPATH)
	ReadKnotID(name=myname,BASEPATH=myBASEPATH)

	pass