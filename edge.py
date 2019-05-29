class Edge :
    def __init__(self, a=None, b=None, c=None, face1=None, face2=None,pointFrom=None, pointTo=None):

        self.pointFrom = pointFrom
        self.pointTo = pointTo
        self.face1 = face1
        self.face2 = face2

        self.a = a
        self.b = b
        self.c = c
