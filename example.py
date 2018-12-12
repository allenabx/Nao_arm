import ctypes
import math

# declare the return type of Kinematics
class Pos(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float)
    ]

# map angle to radian
def ang2rad(ang):
    if ang == 0:
        return 0
    else:
        return math.pi/180*ang


# get target pos using the angel
def getPos(want_Ang):
    lib = ctypes.cdll.LoadLibrary('../release/base.so')  # load c++ library as lib

    # init the joint angles of nao
    num_angles = 24
    angles = (ctypes.c_float*num_angles)()
    for i in range(num_angles):
        angles[i] = 0

    # declare the angles of right arm
    arm0 = 18
    for i in range(0, 4):
        angles[arm0 + i] = ang2rad(want_Ang[i])

    lib.Kinematics.restype = Pos
    pos = lib.Kinematics(angles)

    return [pos.x, pos.y, pos.z]


