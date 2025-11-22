import FreeCAD as App
from FreeCAD import Vector
import math
import helper

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

Knot1 = {
	"P0": {
		"Direction": App.Vector(1,2,5)	,
		"Type": "x"				,
		"Angle":0				,
		"n-fold_Symeterty":4	
	},
	"P1": {
		"Direction": App.Vector(0,-2,5)	,
		"Type": "x"				,
		"Angle":0				,
		"n-fold_Symeterty":4	
	},
	"P2": {
		"Direction": App.Vector(2,-5,15),
		"Type": "x"				,
		"Angle":0				,
		"n-fold_Symeterty":4	
	}
}

def FCtoKnot():
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
	A1,B1,A2,B2 = A1.normalize(),B1.normalize(),A2.normalize(),B2.normalize()
	if not IsTransformend(A1,B1,A2,B2):
		return
	
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

