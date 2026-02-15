# Tested how to import Used CodeX since it is not the logic part of my code, it is just to make it work 

from pathlib import Path
import sys

# Support running this file directly (python App/dev_tools/test.py)
# and as a module inside the App package.
if __package__ is None or __package__ == "":
    project_root = Path(__file__).resolve().parents[2]
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    from App.utils.ChatGBTs_utils import print_list
    from App.KnotLogic import KnotToID2 as TestKnotToID
    from App.dev_tools.dev_helper import LoadKnot
else:
    from ..utils.ChatGBTs_utils import print_list
    from ..KnotLogic import KnotToID2 as TestKnotToID
    from ..dev_tools.dev_helper import LoadKnot

import random


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

def Test2():
    '''
    
    '''
    pass



if __name__ == "__main__" :
    Test1()
