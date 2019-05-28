class Edge :
    def __init__(self, a=None, b=None, c=None, face=None,pointFrom=None, nextE=None, prevE=None, twin=None):
        self.pointFrom = pointFrom
        self.face = face
        self.nextE = nextE
        self.prevE = prevE
        self.twin = twin
        self.a = a
        self.b = b
        self.c = c
