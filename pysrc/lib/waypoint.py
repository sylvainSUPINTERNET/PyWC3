from ..std.index import *
from .cyclist import *
from ..std.unit import *
from .math2d import *
from ..std.timer import *
from .particle import *
class Waypoint2(Vector2,Cyclist):
    range = 32
    def __init__(self,x,y,temp=False):
        Vector2.__init__(self,x,y)
        Cyclist.__init__(self)
    def reached(self,obj):
        if abs(obj.x - self.x) < Waypoint2.range and abs(obj.y - self.y) < Waypoint2.range:
            return True
        return False
class Waypoint3(Vector3,Cyclist):
    range = 32
    def __init__(self,x,y,z,temp=False):
        Vector3.__init__(self,x,y,z)
        Cyclist.__init__(self)
    def reached(self,obj):
        if len(obj.position-self) <= Waypoint3.range:
            return True
        return False

class WaypointParticle(Particle):
    def __init__(self,obj,velocity):
        self.speed = velocity
        Particle.__init__(self,obj,Vector3(0,0,0))
        self.t = Timer()
        self.t.data = self
        self.t.start(0.0, WaypointParticle._timeout)

    def add_waypoint(self,wp):
        if self.waypoint == None:
            self.waypoint = wp
        else:
            self.waypoint.next = wp
        return self

    def add_waypoints(self,*wps):
        for wp in wps:
            if self.waypoint == None:
                self.waypoint = wp
            else:
                self.waypoint.next = wp
        return self

    @staticmethod
    def _timeout():
        self = Timer.get_expired().data
        self.waypoint = self.waypoint.next
        self.go_to()

    def go_to(self,wp=None):
        if wp == None: wp = self.waypoint
        dv = (wp-self.position)
        time = len(dv)/self.speed
        dv = dv/time
        self.update_velocity(dv.x,dv.y,dv.z)
        self.t.start(time,WaypointParticle._timeout)


    def destroy(self,hard=False):
        self.t.destroy()
        self.t = None
        Particle.destroy(self)
        node = self.waypoint
        while node != None and node.next != node:
            node = node.next
            node.prev.destroy()
        if node != None:
            node.destroy()



class WaypointUnit(Unit,Cyclist):
    period = 0.05
    _start = None
    def __init__(self,playerid,unitid=0,x=0.0,y=0.0,face=0.0,skinid=0):
        Unit.__init__(self,playerid,unitid,x,y,face,skinid)
        Cyclist.__init__(self)
        self.waypoint = None
        if WaypointUnit._start == None:
            WaypointUnit._start = self

    def add_waypoint(self,wp):
        if self.waypoint == None:
            self.waypoint = wp
        else:
            self.waypoint.next = wp
        return self

    def add_waypoints(self,*wps):
        for wp in wps:
            if self.waypoint == None:
                self.waypoint = wp
            else:
                self.waypoint.next = wp
        return self

    def go_to(self,wp=None):
        if wp == None: wp = self.waypoint
        self.order("move",wp.x,wp.y)

    def check(self):
        if self.waypoint != None:
            if self.current_order == OrderId("idle"):
                self.go_to()
            if self.waypoint.reached(self):
                self.waypoint = self.waypoint.next
                self.go_to()

    def destroy(self,hard=False):
        if (WaypointUnit._start == self):
            WaypointUnit._start = self._n
        self.exclude()
        if (WaypointUnit._start == self):
            WaypointUnit._start = None
        Unit.destroy(self,hard)

    @staticmethod
    def _period():
        node = WaypointUnit._start
        while node != None:
            nnode = node.next
            # try/except blocks leak memory due to anonymous functions, change at some point
            try: node.check()
            except: print(Error)
            node = nnode
            if node == WaypointUnit._start or WaypointUnit._start == None: break
        Timer.get_expired().restart()

    @staticmethod
    def _init():
        WaypointUnit._group = CreateGroup()
        WaypointUnit.timer = Timer()
        WaypointUnit.timer.start(WaypointUnit.period, WaypointUnit._period)

AddScriptHook(WaypointUnit._init,MAIN_BEFORE)

