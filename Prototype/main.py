# Datenstructure 
from math_utils import Angle3D
from math_utils import OrthoPro
from math_utils import CrossP
from helper import LoadData
from math_utils import Norm
from math_utils import RotateThroughAxis
from math_utils import Add
from math_utils import Scale
from math_utils import IsOppesite

Knot1 = {
    "D0":{
    "Profiltype" : "20x20",
    "Vector" : [-1,1,0]
    },
    "D1":{
    "Profiltype" : "20x20",
    "Vector" : [0,1,0]
    },
     "D2":{
    "Profiltype" : "20x20",
    "Vector" : [0,-1,0]
    },
     "D3":{
    "Profiltype" : "20x20",
    "Vector" : [0,-1,1]
    }
}

# This Functions gets the Axis and Angle with which Matching Families of Knots can be Transformed in to each other
def FindAxisAngle(A1,B1,A2,B2,InDeg=False,tol=1e-7): # ALL = [X,Y,Z] , tol = Tolarance
  A1,B1,A2,B2 = Norm(A1),Norm(B1),Norm(A2),Norm(B2) #Normalizes all the Input Vectors
  def TestMatch(A1,B1,A2,B2,tol=1e-7): #tol = toleranz
    a = Angle3D(A1,A2,1)
    b = Angle3D(B1,B2,1)
    c = a - b
    if c < tol:
      # print("Match")
      return True
    else:
      # print("Not a Match")
      return False
  if not TestMatch(A1,B1,A2,B2,tol):
    return

  if IsOppesite(A1,B1):
    E1 = A1
  else:
    N1 = CrossP(A1,B1)
    c1 = Scale(Add(A1,B1),1/2)
    E1 = CrossP(N1,c1)

  if IsOppesite(A2,B2):
    E2 = A2
  else:
    N2 = CrossP(A2,B2)
    c2 = Scale(Add(A2,B2),1/2)
    E2 = CrossP(N2,c2)
  
  Axis = Norm(CrossP(E1,E2))

  A1p = OrthoPro(A1,Axis)
  B1p = OrthoPro(B1,Axis)
  alpha = Angle3D(A1p,B1p,InDeg)

  # Test if alpha needs to be Multipied by -1
  Test1 = RotateThroughAxis(A1,Axis,alpha)
  # if Angle3D(Test1,B1) < tol: # Andrer test Bitte
    # alpha = -alpha

  return [Axis,alpha]



# Could probably be substetudeded with the combinations from itertools
def PearElementMaker(N): # N = Elements to generate unique pears out of
  i = int(0)
  n = int(0)
  A = []
  N = N - 1 # Ausgleich für Zählen bei null Beginnen
  while i < N:
    n = i
    while n < N:
      n=n+1
      # b = str(i)+"x"+str(n)
      b = [i,n]
      A.append(b)
    i=i+1
  return A

def GetKeys(A,B="A"): # A = Dictonary , B = Starting letter of Key
  k = list(A.keys())
  i = 0
  K = []
  while i < len(k):
    # print(k[i])
    if k[i].startswith(B) :
      K.append(k[i])
    i = i + 1
  # print(K)
  return(K)

def GenrateAngles(A,B="D",C=0): # A = Dictonary , C =  0 => radians 1 => Degrees 
  k = GetKeys(A,B)
  ko = PearElementMaker(len(k))
  i = int(0)
  Angles = []
  while len(ko) > i:
    a1 = B + str(ko[i][0])
    b1 = B + str(ko[i][1])
    a = A[a1]["Vector"]
    b = A[b1]["Vector"]
    alpha = Angle3D(a,b,C)
    # print(alpha)
    Angles.append(alpha)
    i = i + 1
  return Angles # Unsorted list of Relavie Angels

def AssoiativeAngles(A,B="D",C=0):  # A = Dictonary ,B = Key Starting Letter, C =  0 => radians 1 => Degrees 
  AssoiativeAngles = {}


# AssoiativeAngles(A=Knot1,B="D",)

def test():
  V1 = [1,2,3]
  V2 = [2,3,4]
  Axis = [2,5,1]
  alpha = 1
  V1p = RotateThroughAxis(V1,Axis,alpha)
  V2p = RotateThroughAxis(V2,Axis,alpha)

  VecAng = FindAxisAngle(V1,V1p,V2,V2p)
  Vec = VecAng[0]
  Angle = VecAng[1]
  T1 = RotateThroughAxis(V1,Vec,Angle)
  T2 = RotateThroughAxis(V2,Vec,Angle)

  print(V1p)
  print(T1)
  print(V2p)
  print(T2)


test()