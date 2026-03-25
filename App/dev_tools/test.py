# Tested how to import Used CodeX since it is not the logic part of my code, it is just to make it work 

from pathlib import Path
import sys
import FreeCAD as App

# Support running this file directly (python App/dev_tools/test.py)
# and as a module inside the App package.
if __package__ is None or __package__ == "":
    project_root = Path(__file__).resolve().parents[2]
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    from App.utils.ChatGBTs_utils import (timer)
    from App.KnotLogic import KnotToID as TestKnotToID
    from App.dev_tools.dev_helper import (
         LoadKnot,
         SaveKnots,
		)
else:
    from ..utils.ChatGBTs_utils import (timer)
    from ..KnotLogic import KnotToID as TestKnotToID
    from ..dev_tools.dev_helper import LoadKnot

import random

def TrickyKnots():
	Knot1 = [
         
	]

	Ks = [
    	Knot1,
	]
	SaveKnots(Ks,"App/dev_tools/TrickyKnots.json")

	pass

@timer
def Test1():
    '''
    Test the Propety that KnotID should be Order Indiependet
    A + B + C = B + A + C
    '''
    Knot1 = LoadKnot(0)
    Knot1Shuffeld = LoadKnot(0) #Apperently copying does not work So I load the same Test data every time
    random.shuffle(Knot1Shuffeld)
    # print_list(Knot1)
    # print(Knot1Shuffeld)

    Knot1ID = TestKnotToID(Knot1)
    # print_list(Knot1Shuffeld)
    Knot1ShuffeldID = TestKnotToID(Knot1Shuffeld)

    if Knot1ID == Knot1ShuffeldID:
        print("Test passed")
    else:
        print("Test Failed")
        for i in range(len(Knot1ID)):
            print(f"item{i}{Knot1ID[i]}")
            print(f"item{i}{Knot1ShuffeldID[i]}")

@timer
def Test2():
    '''
    Test an edge case: Knot Sum Angels are all equal => no Change of order after Sorting
    This Test Uses Rotation as deciding Factor
    '''
    Knot1 = [
	{
		"Direction": App.Vector(1,0,0)	,
		"Offset": App.Vector(0,0,0),
		"Type": "x"				,
		"Rotation":10				, 
		"Nsym":4	
	},
	{
		"Direction": App.Vector(0,1,0)	,
		"Offset": App.Vector(0,0,0),
		"Type": "x"				,
		"Rotation":20				,
		"Nsym":4	
	},
	{
		"Direction": App.Vector(0,0,1),
		"Offset": App.Vector(0,0,0),
		"Type": "x"				,
		"Rotation":30				,
		"Nsym":4	
	}
]
    
    Knot2 = [
	{
		"Direction": App.Vector(0,1,0)	,
		"Offset": App.Vector(0,0,0),
		"Type": "x"				,
		"Rotation":20				, 
		"Nsym":4	
	},
	{
		"Direction": App.Vector(1,0,0)	,
		"Offset": App.Vector(0,0,0),
		"Type": "x"				,
		"Rotation": 10				,
		"Nsym":4	
	},
	{
		"Direction": App.Vector(0,0,1),
		"Offset": App.Vector(0,0,0),
		"Type": "x"				,
		"Rotation":30				,
		"Nsym":4	
	}
]
    
    Knot1ID = TestKnotToID(Knot1)
    Knot2ID = TestKnotToID(Knot2)

    if Knot1ID == Knot2ID:
        print("Test passed")
    else:
        print("Test Failed")
        for i in range(len(Knot1ID)):
            print(f"item{i}{Knot1ID[i]}")
            print(f"item{i}{Knot2ID[i]}")
    pass

@timer
def Test3():
    '''
    Test an edge case: Knot Sum Angels are all equal => no Change of order after Sorting
    This Test Uses Type as deciding Factor
    '''
    Knot1 = [
	{
		"Direction": App.Vector(1,0,0)	,
		"Offset": App.Vector(0,0,0),
		"Type": "A"				,
		"Rotation":0				, 
		"Nsym":4	
	},
	{
		"Direction": App.Vector(0,1,0)	,
		"Offset": App.Vector(0,0,0),
		"Type": "B"				,
		"Rotation":0				,
		"Nsym":4	
	},
	{
		"Direction": App.Vector(0,0,1),
		"Offset": App.Vector(0,0,0),
		"Type": "C"				,
		"Rotation":0				,
		"Nsym":4	
	}
]
    
    Knot2 = [
	{
		"Direction": App.Vector(0,1,0)	,
		"Offset": App.Vector(0,0,0),
		"Type": "B"				,
		"Rotation":0				, 
		"Nsym":4	
	},
	{
		"Direction": App.Vector(1,0,0)	,
		"Offset": App.Vector(0,0,0),
		"Type": "A"				,
		"Rotation": 0				,
		"Nsym":4	
	},
	{
		"Direction": App.Vector(0,0,1),
		"Offset": App.Vector(0,0,0),
		"Type": "C"				,
		"Rotation":0				,
		"Nsym":4	
	}
]
    
    Knot1ID = TestKnotToID(Knot1)
    Knot2ID = TestKnotToID(Knot2)

    if Knot1ID == Knot2ID:
        print("Test passed")
    else:
        print("Test Failed")
        for i in range(len(Knot1ID)):
            print(f"item{i}{Knot1ID[i]}")
            print(f"item{i}{Knot2ID[i]}")
    pass

@timer
def Test4():
    '''
    Test an edge case: Knot Sum Angels are all equal => no Change of order after Sorting
    This Test Uses Type and Rotation as deciding Factor
    '''
    Knot1 = [
	{
		"Direction": App.Vector(1,0,0)	,
		"Offset": App.Vector(0,10,10),
		"Type": "A"				,
		"Rotation":10				, 
		"Nsym":False	
	},
	{
		"Direction": App.Vector(0,1,0)	,
		"Offset": App.Vector(0,0,0),
		"Type": "B"				,
		"Rotation":30				,
		"Nsym":4	
	},
	{
		"Direction": App.Vector(0,0,1),
		"Offset": App.Vector(0,0,0),
		"Type": "C"				,
		"Rotation":0				,
		"Nsym":4	
	}
]
    
    Knot2 = [
	{
		"Direction": App.Vector(0,1,0)	,
		"Offset": App.Vector(0,0,0),
		"Type": "B"				,
		"Rotation":-330				, 
		"Nsym":4	
	},
	{
		"Direction": App.Vector(1,0,0)	,
		"Offset": App.Vector(0,10,10),
		"Type": "A"				,
		"Rotation": -370				,
		"Nsym":	False
	},
	{
		"Direction": App.Vector(0,0,1),
		"Offset": App.Vector(0,0,0),
		"Type": "C"				,
		"Rotation":0				,
		"Nsym":4	
	}
]
    
    Knot1ID = TestKnotToID(Knot1)
    Knot2ID = TestKnotToID(Knot2)

    if Knot1ID == Knot2ID:
        print("Test passed")
    else:
        print("Test Failed")
        for i in range(len(Knot1ID)):
            print(f"item{i}{Knot1ID[i]}")
            print(f"item{i}{Knot2ID[i]}")

@timer
def Test5():
	'''
	Test for list Length of 1
	'''
	Knot1 = [
		{
			"Direction": App.Vector(1,2,5),
			"Offset": App.Vector(10,0,0),
			"Type": "x",
			"Rotation": 10,
			"Nsym": 4,
		},
	]
	
	try:
		TestKnotToID(Knot1)
		print("Test passed")
	except Exception:
		print("Test Failed | edge case of only 1 Profile is not handeld")
	
@timer
def Test6():
	'''
	Test for list Length of 2
	'''
	Knot1 = [
		{
			"Direction": App.Vector(1,2,5),
			"Offset": App.Vector(10,0,0),
			"Type": "x",
			"Rotation": 10,
			"Nsym": 4,
		},
        {
            "Direction": App.Vector(0,2,6),
			"Offset": App.Vector(0,5,0),
			"Type": "x",
			"Rotation": 30,
			"Nsym": 4,
		}
	]
	
	try:
		TestKnotToID(Knot1)
		print("Test passed")
	except Exception:
		print("Test Failed | edge case of only 2 Profile is not handeld")


if __name__ == "__main__" :
    Test1()
    Test2()
    Test3()
    Test4()
    Test5()
    Test6()
