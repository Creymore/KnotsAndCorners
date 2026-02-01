# Utilities from ChatGBT that are ment to help during Devolpment 
# I wanted to seperate the code from ChatGBT from mine because of clarity

import FreeCAD as App

# from ChatGBT
def print_dict(d, indent=0):
    for key, value in d.items():
        print(" " * indent + str(key) + ":")
        if isinstance(value, dict):
            print_dict(value, indent + 4)
        else:
            print(" " * (indent + 4) + str(value))

def convert_vectors(data):
    """
    Recursively convert App.Vector(x, y, z) to [x, y, z] in any nested structure.
    """
    if isinstance(data, dict):
        return {k: convert_vectors(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [convert_vectors(v) for v in data]
    elif hasattr(data, "x") and hasattr(data, "y") and hasattr(data, "z"):
        # likely an App.Vector
        return [data.x, data.y, data.z]
    else:
        return data

def convert_lists_to_vectors(data):
    """
    Recursively convert [x, y, z] lists back into App.Vector(x, y, z)
    if and only if they look like coordinate triplets.
    """
    if isinstance(data, dict):
        return {k: convert_lists_to_vectors(v) for k, v in data.items()}

    elif isinstance(data, list) and len(data) == 3 \
         and all(isinstance(n, (int, float)) for n in data):
        return App.Vector(*data)

    elif isinstance(data, list):
        return [convert_lists_to_vectors(v) for v in data]

    else:
        return data



def globalPlacement(obj):
    P = obj.Placement
    parent = obj.getParentGeoFeatureGroup()

    while parent:
        P = parent.Placement * P
        parent = parent.getParentGeoFeatureGroup()

    return P

def transformPoint(point, obj_from, obj_to):
    P_from = globalPlacement(obj_from)
    P_to   = globalPlacement(obj_to)

    return P_to.inverse().multVec(
        P_from.multVec(point)
    )

