'''
Logic To Generate Knot IDs
Solve for Axis Angel Rotation
Test Fit Logic TODO
Solve All resuts for Axis Rotation Rotation TODO

'''
################################ IMPORT ####################################################
from pathlib import Path
import sys

# Support running this file directly (python App/KnotLogic.py)
# and as a module inside the App package.
if __package__ is None or __package__ == "":
    project_root = Path(__file__).resolve().parents[1]
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    from App.utils.ChatGBTs_utils import (
        print_list,
        print_list,
    )
else:
    from .utils.ChatGBTs_utils import (
        print_list,
        print_list,
    )
import FreeCAD as App
from FreeCAD import Vector
import math
import copy
from itertools import combinations
from itertools import permutations

##############################################################################################

# https://freecad.github.io/SourceDoc/d1/d13/classBase_1_1Vector3.html#a24f91e91499245ab4282c6d0d0b7630c

# A1 = App.Vector(1,2,3)
# A2 = App.Vector(12,3,64)

# axis = App.Vector(112,3,1)
# # axis = axis*3
# alpha = 10
# alpha = math.degrees(alpha)

# rot = App.Rotation(axis, alpha)
# B1 = rot.multVec(A1)
# B2 = rot.multVec(A2)

# print(A1.Length)
# print(A1)
# print(A2)
# print(axis)
# print(angle)
# print(B1)
# print(B2)
# print(A1.getAngle(A2))

#Data structure
# Should the Knot data be turned into a List ??? Probably better

Knot1 = [
	{
		"Direction": App.Vector(1,2,5)	,
		"Offset": App.Vector(10,0,0),
		"Type": "x"				,
		"Rotation":10				, #Should this be just the direction of the X or Y Axis of the Body
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(0,-2,5)	,
		"Offset": App.Vector(0,10,0),
		"Type": "x"				,
		"Rotation":-20				,
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(2,-5,15),
		"Offset": App.Vector(0,10,0),
		"Type": "x"				,
		"Rotation":-1055				,
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(2,5,0),
		"Offset": App.Vector(0,10,0),
		"Type": "x"				,
		"Rotation":322				,
		"n-fold_Symeterty":4	
	}
]

Knot2 = [
	{
		"Direction": App.Vector(2,-5,15)	,
		"Type": "x"				,
		"Rotation":0				,
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(1,2,5)	,
		"Type": "x"				,
		"Rotation":0				,
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(2,5,0),
		"Type": "x"				,
		"Rotation":0				,
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(0,-2,5),
		"Type": "x"				,
		"Rotation":0				,
		"n-fold_Symeterty":4	
	}
]

def isValidKnot(K)->bool:
	True
	pass

def updateKnot(K,Pn,data): # data = {"name":"value/Stuff"}
	Profile = K[Pn]
	Profile.update(data)
	return K

def removeKnotData(K,Pn,data): # data = "String"
	Profile = K[Pn]
	Profile.pop(data)
	return K

def removeKnotData2(Knot,data): # data = "String"
	for Profile in Knot:
		Profile.pop(data)

def getAngleKnotP(Knot,n,m,deg=True)->float:
	Vn = Knot[n]["Direction"]
	Vm = Knot[m]["Direction"]
	alpha = Vn.getAngle(Vm) # Retruns the angle in rad

	if deg is True: # Is the function used in deg or rad mode
		return math.degrees(alpha)
	else:
		return alpha

def getAngleP2(Knot,n,m,n_key,m_key,deg=True):
	Vn = Knot[n][n_key]
	Vm = Knot[m][m_key]
	alpha = Vn.getAngle(Vm) # Retruns the angle in rad

	if deg is True: # Is the function used in deg or rad mode
		return math.degrees(alpha)
	else:
		return alpha

def SortProfiles(K):
	'''
	Docstring for SortProfiles
	
	:param K: Knot
	:param tol: Tolerance
	Sorts the Profiles According to there Angle Sums
	'''
	for i in range(len(K)):
		AngelSum = 0
		for n in range(len(K)):
			alpha = getAngleKnotP(K,i,n)
			AngelSum = AngelSum + alpha
		updateKnot(K,i,{"AngleSum":AngelSum})
	def AngleSort(S):
		return S["AngleSum"]
	K.sort(key=AngleSort)
	removeKnotData2(K,"AngleSum")
	return K

def NormalizeKnot(K,deg=True):
	'''
	Docstring for NormalizeKnot
	
	:param K: Knot
	
	Normalizes the Contents in a Knot, to make them Uniform
	'''
	for Profile in K:
		#Normaizes the Direction of the Profile
		D = Profile["Direction"]
		Profile.update({"Direction":D.normalize()})
		#Normalizes the Offset of the Profile
		O = Profile["Offset"]
		Profile.update({"Offset":O.projectToPlane(Vector(0,0,0),D)})
		#Normalizes the Roation
		R = Profile["Rotation"] #Rotation Degrees not Radiants
		Nsym = Profile["n-fold_Symeterty"]
		if R < 0: R = 360+(R % -360)
		Profile.update({"Rotation": R % (360/Nsym)})

def KnotToID(K,deg=True):
	if not isValidKnot(K): 
		print("Knot is not Valid")
		return False
	K = copy.deepcopy(K) # Does not Mute the orignal data
	NormalizeKnot(K,deg)
	SortProfiles(K)
	for i in range(len(K)):
		K[i].update({
			"DirectionAngels":[
				getAngleP2(K,i,i-1,"Direction","Direction",deg),
				getAngleP2(K,i,i-2,"Direction","Direction",deg),
				getAngleP2(K,i,i-3,"Direction","Direction",deg),
			]
		})
		K[i].update({
			"OffsetAngels":[
				getAngleP2(K,i,i-1,"Offset","Direction",deg),
				getAngleP2(K,i,i-2,"Offset","Direction",deg),
				getAngleP2(K,i,i-3,"Offset","Direction",deg),
			]
		})
		K[i].update({
			"OffsetRadius": K[i]["Offset"].Length
		})
	for Profile in K:
		Profile.pop("Direction")
		Profile.pop("Offset")
	return K


def IDToKnot(ID):
	pass

#----------------------------------------------------------------------------------------------------------------------------------
#Find Axis and Rotation

def IsTransformend(A1,B1,A2,B2,tol = 1e-6):
	a = A1.getAngle(A2)
	b = B1.getAngle(B2)
	if a - b < tol: #What about Tolerance
		return True
	else:
		print("Vector Pairs A1 A2 does not Match B1 B2") #Debug
		return False

def IsOppesite(V1,V2,tol = 1e-6):
	C = V1.cross(V2)
	if C.Length < tol:
		return True
	else:
		return False



def FindAxisAngle(A1,B1,A2,B2,deg = True,tol = 1e-6):
	'''
	Find Axis Rotation, Returns the Axis and Rotation Transformation, That A1 and B1 get Transformend into A2 and B2 around the Origin(0,0,0)
	A1 transforms into A2
	B1 transforms into B2
	'''
	A1,B1,A2,B2 = A1.normalize(),B1.normalize(),A2.normalize(),B2.normalize()
	if not IsTransformend(A1,B1,A2,B2):
		return False
	
	if IsOppesite(A1,B1):
		E1 = A1
	else:
		N1 = A1.cross(B1)
		C1 = (A1+B1).normalize()
		E1 = N1.cross(C1)

	if IsOppesite(A2,B2): # Should Always be True if the first is True => Could be consoledated
		E2 = A2
	else:
		N2 = A2.cross(B2)
		C2 = (A2+B2).normalize()
		E2 = N2.cross(C2)

	axis = E1.cross(E2)
	axis = axis.normalize()

	A1p = A1.projectToPlane(Vector(0,0,0),axis)
	B1p = B1.projectToPlane(Vector(0,0,0),axis)

	angle = A1p.getAngle(B1p)

	# Test if angle needs a negative sign
	A1 = A1.normalize()
	rot = App.Rotation(axis, math.degrees(angle))
	T1 = rot.multVec(A1)
	T1 = T1.normalize()
	if T1.getAngle(B1)>tol: #getAngle interval 0,pi
		angle = -angle

	# One of the Printed Angels is Always Zer0 
	# print(T1.getAngle(B1))
	# rot = App.Rotation(axis, math.degrees(angle))
	# T1 = rot.multVec(A1)
	# T1 = T1.normalize()
	# print(T1.getAngle(B1))
	
	if deg is True: # Is the function used in deg or rad mode
		return [axis,math.degrees(angle)]
	else:
		return [axis,angle]

