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
		timer
	)
	from App.utils.GloabalPlacement import (
		get_global_placement,
	)
	from App.utils.utils import(
		VecToTuple,
		copyVec
	)
else:
	from .utils.ChatGBTs_utils import (
		print_list,
		print_list,
		timer
	)
	from .utils.GloabalPlacement import (
		get_global_placement
	)
	from .utils.utils import(
		VecToTuple,
		copyVec
	)

import FreeCAD as App
from FreeCAD import Vector
import math
import copy
from itertools import combinations
from itertools import permutations
from itertools import combinations_with_replacement
from collections import Counter

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
Knot1 = [
	{
		"Direction": App.Vector(1,2,5)	, # Direction Always Points away from the Knots center
		"Offset": App.Vector(10,0,0)	,
		"Type": "x"						,
		"Rotation":10					, #Should this be just the direction of the X or Y Axis of the Body
		"Nsym":4						, # How often the Crossection Matches itself along a 360 deg turn around its Geometric Center
	},
	{
		"Direction": App.Vector(0,-2,5)	,
		"Offset": App.Vector(0,10,0),
		"Type": "x"				,
		"Rotation":-20				,
		"Nsym":4	
	},
	{
		"Direction": App.Vector(2,-5,15),
		"Offset": App.Vector(0,10,0),
		"Type": "x"				,
		"Rotation":-1055				,
		"Nsym":4	
	},
	{
		"Direction": App.Vector(2,5,0),
		"Offset": App.Vector(0,10,0),
		"Type": "x"				,
		"Rotation":322				,
		"Nsym":4	
	}
]

Knot2 = [
	{
		"Direction": App.Vector(5,2,-1)	, 
		"Offset": App.Vector(10,0,0)	,
		"Type": "x"						,
		"Rotation":10					, 
		"Nsym":4						, 
	},
	{
		"Direction": App.Vector(5,-2,0)	,
		"Offset": App.Vector(0,10,0),
		"Type": "x"				,
		"Rotation":-20				,
		"Nsym":4	
	},
	{
		"Direction": App.Vector(15,-5,-2),
		"Offset": App.Vector(0,10,0),
		"Type": "x"				,
		"Rotation":-1055				,
		"Nsym":4	
	},
	{
		"Direction": App.Vector(0,5,-2),
		"Offset": App.Vector(0,10,0),
		"Type": "x"				,
		"Rotation":322				,
		"Nsym":4	
	}
]

def MemberstoKnot(Bodies): #Selection only works with Bodys/Profiles that Belong to one Knot
	'''
	Input: Bodies
	Output: Knot
	Discription:
	Turns the Selechted Bodies / Frame Members into a Knot to be used in the KnotToID function
	'''
################################################################################################
	#Get informations from Bodies to turn into a "PreKnot" which then gets Processed into a Knot
	PreKnot = []
	for obj in Bodies:
		Feature = obj.AttachmentSupport[0][0].Name
		Support = obj.AttachmentSupport[0][1][0]

		direction = obj.Placement.Rotation * App.Vector(0,0,1)
		Position = obj.Placement.Base # In the Local Coordinate System of the Parent Part/Assambly | Results in Offset somehow
		Rotation = obj.AttachmentOffset.Rotation.Angle # In radiants
		Rotation = math.degrees(Rotation)

		# How do I determin which Orientdation of the Profile Faces the Knot, Directions always must show away from the Knot center Point

		def isProfile(obj):
			if obj.Name.startswith("Pad") and obj.Label.startswith("Profile"):
				return True
			else:
				return False
	
		Pad = list(filter(isProfile,obj.Group))[0]
		Type = getattr(Pad.Profile[0], "Type", "NotProfile")
		sym = getattr(Pad.Profile[0], "Nysm", False)

		sub = App.ActiveDocument.getObject(Feature).getSubObject(Support)
		EndPoints = [sub.Vertexes[0].Point,sub.Vertexes[1].Point]
		
		data =	{
				"Feature": Feature,
				"Support": Support,
				"direction":direction,
				"Position": Position,
				"Rotation":Rotation,
				"Type": Type,
				"nsym": sym,
				"Points": EndPoints,
				}
		PreKnot.append(
			data
		)

#################################################################################

	allvalues = []
	for data in PreKnot:
		Points = data["Points"]
		for Point in Points:
			allvalues.append(
				(
					Point.x,
					Point.y,
					Point.z
				)
			)

	mostcommenValue = Counter(allvalues).most_common(1)[0][0]
	
	KnotCenter = App.Vector(mostcommenValue[0],mostcommenValue[1],mostcommenValue[2])
	
	for data in PreKnot:
		if not data["Points"][0].isEqual(KnotCenter,1e-6):
			data["Points"].reverse()
		if not data["Points"][0].isEqual(KnotCenter,1e-6):
			PreKnot.remove(data) 
			#Delets the data of the Profile not sharing the Knot center Point
			App.Console.PrintMessage("Removed non connected Profile")
			App.Console.PrintMessage("\n")

##################################################################################

	Knot = []
	for i in range(len(PreKnot)):
		Knot.append({
			"Direction": PreKnot[i]["Points"][1] - PreKnot[i]["Points"][0]	,
			"Offset": PreKnot[i]["Position"] - KnotCenter						,
			"Type": PreKnot[i]["Type"]										,
			"Rotation": PreKnot[i]["Rotation"]								,
			"Nsym": PreKnot[i]["nsym"]										,
		})
	
	return Knot


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
	def TypeSort(S):
		return S["Type"]
	K.sort(key=TypeSort)

	def RotationSort(S):
		return S["Rotation"]
	K.sort(key = RotationSort)

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

def NormalizeKnot(Knot,deg=True):
	'''
	Docstring for NormalizeKnot
	
	:param K: Knot
	
	Normalizes the Contents in a Knot, to make them Uniform
	'''
	for Profile in Knot:
		#Normaizes the Direction of the Profile
		D = Profile["Direction"]
		Profile.update({"Direction":D.normalize()})
		#Normalizes the Offset of the Profile
		O = Profile["Offset"]
		Profile.update({"Offset":O.projectToPlane(Vector(0,0,0),D)})
		#Normalizes the Roation
		R = Profile["Rotation"] #Rotation Degrees not Radiants
		Nsym = Profile["Nsym"]
		if Nsym is not False: # Is only False if there is No symetry like a Circlar od Ring Profile
			if R < 0: R = 360+(R % -360)
			Profile.update({"Rotation": R % (360/Nsym)})
		else:
			Profile.update({"Rotation": 0}) # Rotation does not Matter for a Cirular Profile

def KnotToID(K,deg=True):
	if not isValidKnot(K): 
		print("Knot is not Valid")
		return False
	K = copy.deepcopy(K) # Does not Mute the orignal data
	NormalizeKnot(K,deg)
	SortProfiles(K)
	L= len(K)
	for i in range(L):
		K[i].update({
			"DirectionAngels":[
				getAngleP2(K,i,(i+1)%L,"Direction","Direction",deg),
				getAngleP2(K,i,(i+2)%L,"Direction","Direction",deg),
				getAngleP2(K,i,(i+3)%L,"Direction","Direction",deg),
			]
		})
		K[i].update({
			"OffsetAngels":[
				getAngleP2(K,i,(i+1)%L,"Offset","Direction",deg),
				getAngleP2(K,i,(i+2)%L,"Offset","Direction",deg),
				getAngleP2(K,i,(i+3)%L,"Offset","Direction",deg),
			]
		})
		for n in range(len(K[i]["OffsetAngels"])): #Because nan is not equal to nan, it gets repalced by "NotaNumber"
			if math.isnan(K[i]["OffsetAngels"][n]):
				K[i]["OffsetAngels"][n] = "NotaNumber"
		K[i].update({
			"OffsetRadius": K[i]["Offset"].Length
		})
	for Profile in K:
		Profile.pop("Direction")
		Profile.pop("Offset")
	return K

#print_list(KnotToID(Knot2))

# Codex made this
# It is not needed but is a fun challange, Also Codex failed to use the incuild FreeCAD functions So minus points for that
def IDToKnot(ID):
	pass

#KnotID1 = KnotToID(Knot1)
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
	Find Axis Rotation, Returns the Axis and Rotation Transformation, That A1 and A2 get Transformend into B1 and B2 around the Origin(0,0,0)
	A1 transforms into B1
	A2 transforms into B2
	A gets Transformed / Start
	B is Stationary / Traget
	returns: (axis,angle) 
		axis as FreeCAD.Vector(x,y,z)
		angle as floate
	OR 
	returns False
		if there is no match found
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
	#print(T1.getAngle(B1))
	if T1.getAngle(B1)>tol: #getAngle interval 0,pi
		angle = -angle

	# One of the Printed Angels is Always Zer0 
	# print(T1.getAngle(B1))
	# rot = App.Rotation(axis, math.degrees(angle))
	# T1 = rot.multVec(A1)
	# T1 = T1.normalize()
	# print(T1.getAngle(B1))
	
	if deg is True: # Is the function used in deg or rad mode
		return (axis,math.degrees(angle))
	else:
		return (axis,angle)

def TransformKnot(Knot,axis,angle,deg=True):
	if deg is False: 				# Rotation argument for angle is degrees by default
		angle = math.degrees(angle) # so Radiants get convertertet right
	rot = App.Rotation(axis,angle)
	for Profile in Knot:
		Profile["Direction"] = rot.multVec(Profile["Direction"])
	return(Knot)

#print_list(Knot1)
#print_list(TransformKnot(Knot1,App.Vector(0,10,0),90))

def isKnotMatch(K1,K2): #What about tolerance ?????
	'''
	Finds out if the Knot 1 does match Knot 2
	Knot 1 is the Knot that is transfomed to
	Knot 2 is the Transformed Knot
	'''
	List1 = []
	List2 = []
	for L1 in K1:
		List1.append(VecToTuple(L1["Direction"]))
	
	for L2 in K2:
		List2.append(VecToTuple(L2["Direction"]))

	C1 = Counter(List1)
	C2 = Counter(List2)

	if C1 == C2:
		return True
	else:
		return False

#isKnotMatch(Knot1,TransformKnot(copy.deepcopy(Knot1),App.Vector(1,0,0),0))
@timer
def FindallMatches(K1,K2):
	'''
	K1: Knot1 Stationary, 
	K2: Knot2 gets Transformed
	Discription:
		Finds all the Machtches, wehere K2 gets Transformed into K1 successfully
	'''
	L = len(K1) #K1 has the same length as K2, otherwise something went wrong eralier
	per = list(permutations(range(L),2))
	allPairings = list(combinations_with_replacement(per,2))
	for pairing in allPairings:
		A1 = K2[pairing[1][0]]["Direction"] #Transformed
		A2 = K2[pairing[1][1]]["Direction"]

		B1 = K1[pairing[0][0]]["Direction"] #Stationarrys
		B2 = K1[pairing[0][1]]["Direction"]

		A1,B1,A2,B2 = copyVec(A1),copyVec(B1),copyVec(A2),copyVec(B2)
		
		axisAngle = FindAxisAngle(A1,B1,A2,B2)
		if axisAngle is not False:
			K2T = TransformKnot(copy.deepcopy(K2),axisAngle[0],axisAngle[1]) # deepcopy to not mute the orgnial Knont
			for i in range(len(K1)):
				print(K1[i])
				print(K2T[i])
			
			print(pairing)
			print(axisAngle)
			if isKnotMatch(K1,K2T) is True: #Rework the is match function
				print("Succes")
			
			

	pass

FindallMatches(Knot1,TransformKnot(copy.deepcopy(Knot1),App.Vector(1,0,0),90))
#FindallMatches(Knot1,Knot2)

# if __name__ == "__main__":
# 	import FreeCADGui as Gui
# 	sel = Gui.Selection.getSelection()
# 	Knot = MemberstoKnot(sel)
# 	KnotID = KnotToID(Knot)

# 	for data in KnotID:
# 		App.Console.PrintMessage(data)
# 		App.Console.PrintMessage("\n")
	