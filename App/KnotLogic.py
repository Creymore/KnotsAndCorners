'''
Logic To Generate Knot IDs
Solve for Axis Angel Rotation
Test Fit Logic TODO
Solve All resuts for Axis Angle Rotation TODO

'''


import FreeCAD as App
from FreeCAD import Vector
import math
import dev_helper as dev_helper
from itertools import combinations
from itertools import permutations
from utils import arraySum

from ChatGBTs_utils import print_dict

# https://freecad.github.io/SourceDoc/d1/d13/classBase_1_1Vector3.html#a24f91e91499245ab4282c6d0d0b7630c

A1 = App.Vector(1,2,3)
A2 = App.Vector(12,3,64)

axis = App.Vector(112,3,1)
# axis = axis*3
alpha = 10
alpha = math.degrees(alpha)

rot = App.Rotation(axis, alpha)
B1 = rot.multVec(A1)
B2 = rot.multVec(A2)

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
		"Type": "x"				,
		"Angle":0				,
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(0,-2,5)	,
		"Type": "x"				,
		"Angle":0				,
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(2,-5,15),
		"Type": "x"				,
		"Angle":0				,
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(2,5,0),
		"Type": "x"				,
		"Angle":0				,
		"n-fold_Symeterty":4	
	}
]

Knot1WO = [
	{
		"Direction": App.Vector(1,2,5),
		"Offset": App.Vector(0,0,0), # Z is always 0
		"Type": "x"				,
		"Angle":0				,
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(0,-2,5)	,
		"Type": "x"				,
		"Angle":0				,
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(2,-5,15),
		"Type": "x"				,
		"Angle":0				,
		"n-fold_Symeterty":4	
	},
	{
		"Direction": App.Vector(2,-5,0),
		"Type": "x"				,
		"Angle":0				,
		"n-fold_Symeterty":4	
	}
]

Knot1ID = [
	{
		# "Direction": App.Vector(1,2,5)	,
		"Type": "x"							,
		"Angle":0							,
		"n-fold_Symeterty":4				,
		"Angels": [1,2,3]
	},
	{
		# "Direction": App.Vector(0,-2,5)	,
		"Type": "x"							,
		"Angle":0							,
		"n-fold_Symeterty":4				,
		"Angels": [1,2,3]
	},
	{
		# "Direction": App.Vector(2,-5,15)	,
		"Type": "x"							,
		"Angle":0							,
		"n-fold_Symeterty":4				,
		"Angels": [1,2,3]
	}
]


def isValidKnot(K)->bool: 
	pass

def updateKnot(K,Pn,data): #Functions as i intentended but i dont know why exactly
	Profile = K[f"P{Pn}"]
	Profile.update(data)
	return K

updateKnot(Knot1,1,{"Type":"y"})
print(Knot1)

def getAngleKnotP(Knot,n,m,deg=True)->float:
	Vn = Knot[f"P{n}"]["Direction"]
	Vm = Knot[f"P{m}"]["Direction"]
	alpha = Vn.getAngle(Vm) # Retruns the angle in rad

	if deg is True: # Is the function used in deg or rad mode
		return math.degrees(alpha)
	else:
		return alpha
	
def DictToList(K):
	List = []
	for item in K.items():
		List.append(item[1])
	return List

def ListToDict(L):
	Dict = {}
	for i in range(len(L)):
		Dict.update({f"P{i}":L[i]})
	return Dict

def SortDirections(K):
	# Perm = list(permutations(range(len(K)),2))
	for i in range(len(K)):
		Angels = []
		AngelSum = 0
		for n in range(len(K)):
			alpha = getAngleKnotP(K,i,n)
			Angels.append(alpha)
			AngelSum = AngelSum + alpha
		updateKnot(K,i,{"AngleSum":AngelSum})
	def AngleSort(S):
		return S["AngleSum"]
	KL = DictToList(K)
	KL.sort(key=AngleSort)
	return ListToDict(KL)

print_dict(SortDirections(Knot1))


def FCtoKnot():
	pass

def KnotToAngleID(K):
	L = len(K)
	Combinations = list(combinations(range(L),2))
	r = []
	for i in range(L):
		def myfilter(x,n=i):
			if x[0] == n:
				return True
			else:
				return False
		Com = list(filter(myfilter,Combinations))
		for C in Com:
			alpha = getAngleKnotP(K,C[0],C[1])
			r.append(alpha)
	return r

# print(KnotToAngleID(Knot1))

def KnotToID(K):
	L = len(K)
	Perm = list(permutations(range(L),2))
	for i in range(L):
		def myfilter(x,n=i):
			if x[0] == n:
				return True
			else:
				return False
		Pe = list(filter(myfilter,Perm))
		L = []
		for C in Pe:
			alpha = getAngleKnotP(K,C[0],C[1])
			L.append(alpha)
		updateKnot(K,i,{"Angles":L})
	for Key in K:
		K[Key].pop("Direction")

# Knot2 = dev_helper.LoadKnot(2)
# KnotToID(Knot2)
# print_dict(Knot2)

def IDToKnot(ID):
	pass


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
	Find Axis Angle, Returns the Axis and Angle Transformation, That A1 and B1 get Transformend into A2 and B2 around the Origin(0,0,0)
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

