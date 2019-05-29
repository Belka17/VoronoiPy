class Vertex:
    def __init__(self, point=None, edge=None,cw_next=None,ccw_next=None):
        self.point = point
        self.edge = edge
        self.cw_next = cw_next
        self.ccw_next = ccw_next