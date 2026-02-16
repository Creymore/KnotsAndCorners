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

def FCtoKnot(Selection): #Selection only works with Bodys/Profiles that Belong to one Knot
	for obj in Selection:
		Feature = obj.AttachmentSupport[0][0].Name
		Support = obj.AttachmentSupport[0][1][0]

		direction = obj.Placement.Rotation * App.Vector(0,0,1)
		Position = obj.Placement.Base # In the Local Coordinate System of the Parent Part/Assambly
	
		sub = App.ActiveDocument.getObject(Feature).Shape
		EndPoints = [sub.Vertexes[0].Point,sub.Vertexes[1].Point]

	pass



# On the TODO list
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
		for n in range(len(K[i]["OffsetAngels"])): #Because nan is not equal to nan, it gets repalced by 
			if math.isnan(K[i]["OffsetAngels"][n]):
				K[i]["OffsetAngels"][n] = "NotaNumber"
		K[i].update({
			"OffsetRadius": K[i]["Offset"].Length
		})
	for Profile in K:
		Profile.pop("Direction")
		Profile.pop("Offset")
	return K

# Codex made this
# It is not needed but is a fun challange, Also Codex failed to use the invuild FreeCAD functions So minus points for that
def IDToKnot(ID):
	if not ID:
		return []

	N = len(ID)
	eps = 1e-12

	def _is_degree_values(profiles, key):
		for p in profiles:
			for a in p.get(key, []):
				if abs(a) > (2 * math.pi + 1e-6):
					return True
		return False

	use_deg = _is_degree_values(ID, "DirectionAngels") or _is_degree_values(ID, "OffsetAngels")

	def _to_rad(a):
		return math.radians(a) if use_deg else a

	def _clamp(v, lo=-1.0, hi=1.0):
		if v < lo:
			return lo
		if v > hi:
			return hi
		return v

	def _dot(a, b):
		return (a[0] * b[0]) + (a[1] * b[1]) + (a[2] * b[2])

	def _norm(v):
		return math.sqrt(_dot(v, v))

	def _normalize(v):
		n = _norm(v)
		if n < eps:
			return (1.0, 0.0, 0.0)
		return (v[0] / n, v[1] / n, v[2] / n)

	def _solve3(A, b):
		# Fast explicit 3x3 solve via Cramer's rule
		(a11, a12, a13), (a21, a22, a23), (a31, a32, a33) = A
		det = (
			a11 * (a22 * a33 - a23 * a32)
			- a12 * (a21 * a33 - a23 * a31)
			+ a13 * (a21 * a32 - a22 * a31)
		)
		if abs(det) < eps:
			return None

		def det3(
			m11, m12, m13,
			m21, m22, m23,
			m31, m32, m33,
		):
			return (
				m11 * (m22 * m33 - m23 * m32)
				- m12 * (m21 * m33 - m23 * m31)
				+ m13 * (m21 * m32 - m22 * m31)
			)

		dx = det3(b[0], a12, a13, b[1], a22, a23, b[2], a32, a33)
		dy = det3(a11, b[0], a13, a21, b[1], a23, a31, b[2], a33)
		dz = det3(a11, a12, b[0], a21, a22, b[1], a31, a32, b[2])
		inv_det = 1.0 / det
		return (dx * inv_det, dy * inv_det, dz * inv_det)

	def _angle_ij(i, j, key):
		# key is either "DirectionAngels" or "OffsetAngels"
		arr = ID[i].get(key, [])
		d = (i - j) % N
		if d == 1 and len(arr) > 0:
			return _to_rad(arr[0])
		if d == 2 and len(arr) > 1:
			return _to_rad(arr[1])
		if d == 3 and len(arr) > 2:
			return _to_rad(arr[2])
		# fallback: read from j if present
		rd = (j - i) % N
		jarr = ID[j].get(key, [])
		if rd == 1 and len(jarr) > 0:
			return _to_rad(jarr[0])
		if rd == 2 and len(jarr) > 1:
			return _to_rad(jarr[1])
		if rd == 3 and len(jarr) > 2:
			return _to_rad(jarr[2])
		return 0.0

	# Rebuild direction vectors (unit length)
	D = []
	if N == 1:
		D = [(1.0, 0.0, 0.0)]
	elif N == 2:
		t01 = _angle_ij(0, 1, "DirectionAngels")
		D = [
			(1.0, 0.0, 0.0),
			(_clamp(math.cos(t01)), math.sin(t01), 0.0),
		]
	else:
		t01 = _angle_ij(0, 1, "DirectionAngels")
		t02 = _angle_ij(0, 2, "DirectionAngels")
		t12 = _angle_ij(1, 2, "DirectionAngels")

		c01 = _clamp(math.cos(t01))
		s01 = math.sin(t01)
		if abs(s01) < eps:
			s01 = eps if s01 >= 0 else -eps

		d0 = (1.0, 0.0, 0.0)
		d1 = _normalize((c01, s01, 0.0))
		x2 = _clamp(math.cos(t02))
		y2 = (math.cos(t12) - x2 * c01) / s01
		z2_sq = max(0.0, 1.0 - x2 * x2 - y2 * y2)
		d2 = _normalize((x2, y2, math.sqrt(z2_sq)))
		D = [d0, d1, d2]

		for i in range(3, N):
			c0 = _clamp(math.cos(_angle_ij(i, 0, "DirectionAngels")))
			c1 = _clamp(math.cos(_angle_ij(i, 1, "DirectionAngels")))
			c2 = _clamp(math.cos(_angle_ij(i, 2, "DirectionAngels")))
			A = [D[0], D[1], D[2]]
			solved = _solve3(A, [c0, c1, c2])
			if solved is None:
				# Stable fallback if the linear system is nearly singular
				solved = (c0, c1, c2)
			D.append(_normalize(solved))

	# Rebuild offsets from per-profile angle/radius constraints
	O = []
	for i in range(N):
		r = float(ID[i].get("OffsetRadius", 0.0))
		if r == 0.0:
			O.append((0.0, 0.0, 0.0))
			continue

		j1, j2, j3 = (i - 1) % N, (i - 2) % N, (i - 3) % N
		p1 = _to_rad(ID[i].get("OffsetAngels", [0.0, 0.0, 0.0])[0] if len(ID[i].get("OffsetAngels", [])) > 0 else 0.0)
		p2 = _to_rad(ID[i].get("OffsetAngels", [0.0, 0.0, 0.0])[1] if len(ID[i].get("OffsetAngels", [])) > 1 else 0.0)
		p3 = _to_rad(ID[i].get("OffsetAngels", [0.0, 0.0, 0.0])[2] if len(ID[i].get("OffsetAngels", [])) > 2 else 0.0)
		b = [r * _clamp(math.cos(p1)), r * _clamp(math.cos(p2)), r * _clamp(math.cos(p3))]
		A = [D[j1], D[j2], D[j3]]
		solved = _solve3(A, b)
		if solved is None:
			# Fallback vector still matches the requested radius quickly.
			solved = (r, 0.0, 0.0)
		O.append(solved)

	# Convert into Knot structure expected by KnotToID
	K = []
	for i in range(N):
		pi = ID[i]
		K.append({
			"Direction": App.Vector(D[i][0], D[i][1], D[i][2]),
			"Offset": App.Vector(O[i][0], O[i][1], O[i][2]),
			"Type": pi.get("Type", "x"),
			"Rotation": pi.get("Rotation", 0),
			"n-fold_Symeterty": pi.get("n-fold_Symeterty", 1),
		})
	return K

# KnotID1 = KnotToID(Knot1)
# Knot1B = IDToKnot(KnotID1)
# # print_list(Knot1B)
# KnotID2 = KnotToID(Knot1B)
# for i in range(len(KnotID1)):
# 	print(KnotID1[i])
# 	print(KnotID2[i])
# print(KnotID1 == KnotID2)

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

