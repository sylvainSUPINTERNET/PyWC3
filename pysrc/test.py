from df.commonj import *
from df.test import *
from std.index import *
from lib.click_plane import *
from lib.unitphysics import *

#
# class testc:
#     o = None
#     def __new__(cls):
#         if testc.o == None:
#             testc.o = object.__new__()
#         return testc.o
#
# def c():
#     for i in range(100):
#         testc()
#
#
# def test():
#     TimerStart(CreateTimer(),0.01,True,c)

class FloatingPlatform(Box):
    def __init__(self,x,y,z):
        Box.__init__(self, x-64, y-64, z-80, x+64, y+64, z)
        self.clickplane = ClickPlane(x-64, y-64, x+64, y+64, z)
        self.fx = Effect(x,y,z,r"Doodads\\Cinematic\\FootSwitch\\FootSwitch.mdl")
        # self.fx.clear_sub_animations()
        # self.fx.add_sub_animation(SUBANIM_TYPE_ALTERNATE_EX)
        self.fx.animate(ANIM_TYPE_DEATH)


def test():
    offset = [576,0,140]
    mult = [128,128,35]
    lst = [
        Vector3(0, 0, 0),
        Vector3(0, 1, 1),
        Vector3(0, 2, 2),
        Vector3(-1, 2, 3),
        Vector3(-2, 2, 4),
        Vector3(-2, 1, 5),
        Vector3(-2, 0, 6),
        Vector3(-1, 0, 7),
        Vector3(0, 0, 8),
    ]
    for v in lst:
        Particle.collidables.append(FloatingPlatform(v.x*mult[0]+offset[0],v.y*mult[1]+offset[1],v.z*mult[2]+offset[2]))
    for i in range(2):
        PhysicsUnit(0,'hfoo', 0,0)
    for i in range(2):
        PhysicsUnit(1,'hfoo', 0,0)

AddScriptHook(test,MAIN_AFTER)
