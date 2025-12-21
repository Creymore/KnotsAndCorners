import FreeCAD as App
import os
import hashlib

from dev_helper import loadBASEPATH


'''
This uses the Os (Windows/Linux/Mac) as a database
for the Knots. Probarbly not the ideal solution.
The idea is to have a two leveled system.
DataBase
-> 000001 ... 100000
-> -> 00001 ... 
10.000 Knots should be enouth
Save
    Hash
    Modulo
    Go in folder
    Handel collition
        compare document in folder
        if match put in folder
        if not check next folder
'''
def SaveKnotID(KnotID,BASEPATH):
    Pos = hash(KnotID)


    pass


def LoadKnotID(KnotID,BASEPATH):

    pass

if __name__ == "__main__":
    BASEPATH = loadBASEPATH()
    BASEPATH = f"{BASEPATH}/DataBase"



# test = "Test word"
# print(test)
# htest = hash(test)
# print(htest)
# mod = htest % 10000
# print(mod)