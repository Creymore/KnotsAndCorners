import FreeCAD as App
import os
import hashlib
from utils import isFCfile
import random

from dev_helper import loadBASEPATH


'''
This uses the Os (Windows/Linux/Mac) as a database
for the Knots. Probarbly not the ideal solution.
The idea is to have a two leveled system.
DataBase
-> 00001 ... 10000
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

#Check if the name already exist
#Somehow give that info to the user about needing an diffrent name
def SaveFCfile(file,path):

    pass

# Loads all Valid Knot files in a direktory/folder
def LoadFCfiles(path):

    pass

# The Function should check for Vaild Path DONE, Valid file formate DONE, Valid "Knot" in Part in file
def ReadKnotID(path): # path of file
    # print(f"Read{path}")
    if not os.path.exists(path): # check Valid Path
        return False
    if not isFCfile(path):
        return False
    doc = App.open(path)
    mypart = doc.getObject("Part") #Ideal case what if name is not "Part"
    KnotID = mypart.KnotID
    return KnotID

# This function adds a file with the KnotID. Helper function for testing and devolpment
def AddFileWithID(KnotID,path,name="DefaultKnotID"):
    initalname = f"R{str(random.randrange(0,100))}"
    doc = App.newDocument(initalname)                   # The Work aroud initial name, Somehow if the function is run in a loop,
                                                        # each file gets the KnotID of the first element
    mypart = doc.addObject('App::Part','Part')
    mypart.addProperty("App::PropertyString", "KnotID", "KnotInformation", "This is the Knot ID")
    mypart.KnotID = KnotID
    mypart.setEditorMode("KnotID",1) # 1 => Read only mode
    # print(KnotID)
    doc.recompute()
    path = f"{path}/{name}"
    App.getDocument(initalname).saveAs(path)
    App.closeDocument(initalname) # Important do not delete
    print(f"New default file was Created ad: {path}")

#default for N is 10000 because 
def findPos(KnotID,N=10000):
    KnotID = KnotID.encode("utf-8")
    Pos = hashlib.sha256(KnotID).hexdigest()
    Pos = int(Pos,32)
    Pos = Pos % N
    Pos = str(Pos).zfill(len(str(N)))
    # Pos = "01000" #to debug, test collition
    return Pos

def SearchValidPaths(KnotID,BASEPATH,Mode="Save"): # Mode = "Save" => Valid path to save in | Mode = "Load" => Valid path to Load
    '''
    Searches for a Valid path to load from
    Searches or creates for a Valid path to Save in
    '''
    Pos = findPos(KnotID)
    path = f"{BASEPATH}/{Pos}"
    ValidPath = []
    if not os.path.exists(path) and Mode == "Save":
        os.mkdir(path)
    if not os.path.exists(path):
        return(ValidPath)
    folders = os.listdir(path)
    for folder in folders:
        SubPath = f"{path}/{folder}"
        if not os.path.isdir(SubPath):
            continue
        files = os.listdir(SubPath)
        for file in files:
            filepath = f"{SubPath}/{file}"
            if ReadKnotID(filepath) == KnotID:
                ValidPath.append(SubPath)
        if len(files) == 0 and len(ValidPath) == 0 and Mode == "Save":
            ValidPath.append(SubPath)
    if len(ValidPath) == 0:
        newpath = f"{path}/{str(len(os.listdir(path))).zfill(5)}" # zfill maybe not enouth ???
        if not os.path.exists(newpath) and Mode == "Save":
            os.mkdir(newpath)
            print(f"new Path was Created ad: {newpath}")
            ValidPath.append(newpath)
            # AddFileWithID(KnotID,newpath) #Adds a file with the KnotID Probarly should check 
        elif Mode == "Save":
            print(f"The Path {newpath} already exist, without files")
    if len(ValidPath) > 1 :
        print("There is more then one Valid Path, Something is wrong")
    return(ValidPath)


def SaveKnotWithID(KnotID,BASEPATH): # BASEPATH is the "DataBase" path
    path = SearchValidPaths(KnotID,BASEPATH,Mode="Save")
    path = path[0]
    # print(path)
    # print(KnotID)
    AddFileWithID(KnotID=KnotID,path=path)
    return path


def LoadKnotID(KnotID,BASEPATH):

    pass


if __name__ == "__main__":
    def test(BASEPATH):
        test1 = "String"
        # AddFileWithID(test1,BASEPATH,name="test1")
        SaveKnotWithID(test1,BASEPATH)
        test2 = f"fString"
        # AddFileWithID(test2,BASEPATH,name="test2")
        SaveKnotWithID(test2,BASEPATH)
        i = 10
        test3 = f"fStringi{i}"
        # AddFileWithID(test3,BASEPATH,name="test3")
        SaveKnotWithID(test3,BASEPATH)

        print(SearchValidPaths(test1,BASEPATH,"Load"))
        print(SearchValidPaths(test2,BASEPATH,"Load"))
        print(SearchValidPaths(test3,BASEPATH,"Load"))

    def test2():
        i=0
        while i<1000:
            name = f"Test{i}"
            V1 = str(SaveKnotWithID(name,BASEPATH))
            V2 = str(SearchValidPaths(name,BASEPATH,"Load")[0])
            # print(V1)
            # print(V2)
            if V1 == V2:
                print(f"Succes{i}")
            i=i+1

    BASEPATH = loadBASEPATH()
    BASEPATH = f"{BASEPATH}/DataBase"
    test(BASEPATH)
    