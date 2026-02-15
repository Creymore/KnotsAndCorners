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
	return True

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
			alpha = getAngleP2(K,i,n,"Direction","Direction")
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

def KnotToID(K,deg=False):
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

# print(isValidKnot(Knot1))
print_list(KnotToID(Knot1))

def IDToKnot(ID):
	K = copy.deepcopy(ID)
	n = len(K)
	if n != 4:
		raise ValueError("IDToKnot currently supports 4-profile knots only")
	tol = 1e-12

	def _solve3x3_rows(r1, r2, r3, b1, b2, b3):
		a11, a12, a13 = r1
		a21, a22, a23 = r2
		a31, a32, a33 = r3
		det = (
			a11 * (a22 * a33 - a23 * a32)
			- a12 * (a21 * a33 - a23 * a31)
			+ a13 * (a21 * a32 - a22 * a31)
		)
		if abs(det) < tol:
			raise ValueError("Degenerate knot ID (cannot solve 3x3 system)")
		inv_det = 1.0 / det
		dx = (
			b1 * (a22 * a33 - a23 * a32)
			- a12 * (b2 * a33 - a23 * b3)
			+ a13 * (b2 * a32 - a22 * b3)
		)
		dy = (
			a11 * (b2 * a33 - a23 * b3)
			- b1 * (a21 * a33 - a23 * a31)
			+ a13 * (a21 * b3 - b2 * a31)
		)
		dz = (
			a11 * (a22 * b3 - b2 * a32)
			- a12 * (a21 * b3 - b2 * a31)
			+ b1 * (a21 * a32 - a22 * a31)
		)
		return Vector(dx * inv_det, dy * inv_det, dz * inv_det)

	# Rebuild full symmetric direction-angle matrix from compact ID fields.
	A = [[0.0 for _ in range(n)] for _ in range(n)]
	for i, p in enumerate(K):
		a = p["DirectionAngels"]
		j0 = (i - 1) % n
		j1 = (i - 2) % n
		j2 = (i - 3) % n
		A[i][j0] = a[0]
		A[j0][i] = a[0]
		A[i][j1] = a[1]
		A[j1][i] = a[1]
		A[i][j2] = a[2]
		A[j2][i] = a[2]

	# Build four unit direction vectors from pairwise angles.
	a01 = A[0][1]
	c01 = math.cos(a01)
	s01 = math.sin(a01)
	if abs(s01) < tol:
		s01 = tol
	d0 = Vector(1.0, 0.0, 0.0)
	d1 = Vector(c01, s01, 0.0)

	c02 = math.cos(A[0][2])
	c12 = math.cos(A[1][2])
	x2 = c02
	y2 = (c12 - x2 * c01) / s01
	z2_sq = 1.0 - x2 * x2 - y2 * y2
	if z2_sq < 0.0:
		z2_sq = 0.0
	z2 = math.sqrt(z2_sq)
	d2 = Vector(x2, y2, z2)

	c03 = math.cos(A[0][3])
	c13 = math.cos(A[1][3])
	c23 = math.cos(A[2][3])
	d3 = _solve3x3_rows(
		(d0.x, d0.y, d0.z),
		(d1.x, d1.y, d1.z),
		(d2.x, d2.y, d2.z),
		c03, c13, c23
	)
	dirs = [d0.normalize(), d1.normalize(), d2.normalize(), d3.normalize()]

	# Rebuild offsets from their angles to the other 3 directions and radius.
	for i, p in enumerate(K):
		j0 = (i - 1) % n
		j1 = (i - 2) % n
		j2 = (i - 3) % n
		oa0, oa1, oa2 = p["OffsetAngels"]
		r = p["OffsetRadius"]
		b0 = r * math.cos(oa0)
		b1 = r * math.cos(oa1)
		b2 = r * math.cos(oa2)
		o = _solve3x3_rows(
			(dirs[j0].x, dirs[j0].y, dirs[j0].z),
			(dirs[j1].x, dirs[j1].y, dirs[j1].z),
			(dirs[j2].x, dirs[j2].y, dirs[j2].z),
			b0, b1, b2
		)
		K[i] = {
			"Direction": dirs[i],
			"Offset": o.projectToPlane(Vector(0,0,0), dirs[i]),
			"Type": p.get("Type", "x"),
			"Rotation": p["Rotation"],
			"n-fold_Symeterty": p["n-fold_Symeterty"],
		}
	return K

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

