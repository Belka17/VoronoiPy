class Vertex:
    def __init__(self, point=None, edge=None,cw_next=None,ccw_next=None):
        self.point = point
        self.edges = []
        if edge:
            self.edges.append(edge)
        self.cw_next = cw_next
        self.ccw_next = ccw_next

    def __eq__(self, other):
        return self.point == other.point
