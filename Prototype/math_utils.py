import math

T1=[1,2,3]
T2=[4,5,6]

#Could use the General defintion with the sum
def DotP(Vector1,Vector2): # A =[a1,a2,a3] B=[b1,b2,b3]
    dot = Vector1[0]*Vector2[0]+Vector1[1]*Vector2[1]+Vector1[2]*Vector2[2]
    return dot

# print(DotP(T1,T2))

def CrossP(Vector1,Vector2): # A =[a1,a2,a3] B=[b1,b2,b3]
    cross = [ 
            Vector1[1]*Vector2[2] - Vector1[2]*Vector2[1],
            Vector1[2]*Vector2[0] - Vector1[0]*Vector2[2],
            Vector1[0]*Vector2[1] - Vector1[1]*Vector2[0]
            ]
    return cross

# print(CrossP(T1,T2))

def Scale(Vector,Scalar): # A = [X,Y,Z] B = n
    scaled = [
            Vector[0]*Scalar,
            Vector[1]*Scalar,
            Vector[2]*Scalar
            ]
    return scaled

def Add(Vector1,Vector2): # A = [a1,a2,a3] B = [b1,b2,b3]
    added = [
        Vector1[0]+Vector2[0],
        Vector1[1]+Vector2[1],
        Vector1[2]+Vector2[2]
    ]
    return added

def OrthoPro(Point,Normal,R=[0,0,0]): #P = [X,Y,Z] , Point to Projekt N = [n1,n2,n3] , Normal of Plane R=[x,y,z] ,
    a = DotP(Add(Point,Scale(R,-1)),Normal)
    b = DotP(Normal,Normal)
    c = Scale(Normal,a/b)
    Projected = Add(Point,Scale(c,-1))
    return Projected

# print(OrthoPro(T1,T2))

def VectorLenth(Vector): # A = [x,y,z]
  a = math.sqrt(pow(Vector[0],2)+pow(Vector[1],2)+pow(Vector[2],2))
  return a

def Norm(Vector): # A = [X,Y,Z]
   return Scale(Vector,1/VectorLenth(Vector))

def Angle3D(Vector1,Vector2,InDeg=False): # A = [x,y,z] , B = [x,y,z] , c = 0 => radians 1 => Degrees
  s = DotP(Vector1,Vector2)
  a = math.acos(s/(VectorLenth(Vector1)*VectorLenth(Vector2)))
  if InDeg is True:
    a = math.degrees(a)
  return a

#Source: https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
def RotateThroughAxis(Point,Axis,Angle): # P = [X,Y,Z] , Point K = [X,Y,Z] , alpha = Angle
   Axis = Norm(Axis) # This is Really Important
   a = Scale(Point,math.cos(Angle))
   b = Scale(CrossP(Axis,Point),math.sin(Angle))
   c = Scale(Axis,DotP(Axis,Point)*(1-math.cos(Angle)))
   d = Add(a,b)
   roteted = Add(d,c)
   return roteted

def IsOppesite(Vector1,Vector2,tol=1e-7):
    #  if VectorLenth(Add(Vector1,Scale(Vector2,-1))) < tol:
   if abs(Angle3D(Vector1,Vector2) - math.pi) < tol:
      return True
   else:
      return False

if __name__ == "__main__":
  def test():
    V1 = [1,2,3]
    V2 = [2,3,4]
    Axis = [2,3,1]
    alpha = 10
    V1p = RotateThroughAxis(V1,Axis,alpha)
    V2p = RotateThroughAxis(V2,Axis,alpha)

    print(V1)
    print(V2)
    print(Axis)
    print(alpha)
    print(V1p)
    print(V2p)
    # print(math.sin(math.pi))
    # print(Angle3D(V1,V2))
    # print(Angle3D(V1p,V2p))
    # print(abs(Angle3D(V1,V2)-math.pi))
    # print(IsOppesite(V1,V2))
  test()
  