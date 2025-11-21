import math
import random
import json


#Helper funktion to generate Test data could be in a diffrent file
def GenerateData(A=1,B=4,C = "20x20",D = "DummyData.json" ): # A = Number of Knots , B = Direktions in Knots 
  def GenerateVectors(A=3):
    V = []
    for i in range(A):
      V.append(random.randrange(-100,100,1))
    return V
  jknots = {}
  for n in range(A):
    knot = {}
    for i in range(B):
        Vec = GenerateVectors()
        Direction = {
          "Profilerype" : C ,
          "Vector" : Vec
        }
        knot.update({f"D{i}":Direction})
       # print(Direction)
    # print(corner)
    jknots.update({f"Knot{n}" : knot})
  Data = json.dumps(jknots, sort_keys=False, indent=2)
  with open(D, "w") as f:
    f.write(Data)

GenerateData(A=1000)

def LoadData(A="DummyData.json",B=0): # A= file to load from, B = corner numer
  with open(A,"r") as f:
    data = json.load(f)
    data = data[f"Knot{B}"]
  return data

