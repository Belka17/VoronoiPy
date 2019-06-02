import math
from point import Point



class Edge :
    def __init__(self, a=None, b=None, c=None, face1=None, face2=None,pointFrom=None, pointTo=None, vectorX=None, vectorY = None):

        self.pointFrom = pointFrom
        self.pointTo = pointTo
        self.face1 = face1
        self.face2 = face2

        self.a = a
        self.b = b
        self.c = c

        self.vectorX = vectorX
        self.vectorY = vectorY

    def draw(self, plt, d):
        delta = 0.04
        if not self.pointFrom and not self.pointTo:
            return
        if self.pointTo and self.pointFrom:
            d = 6
            # x_curr = self.pointFrom.x
            #
            # if self.b != 0:
            #
            #     if self.pointTo.x < self.pointFrom.x:
            #         delta = -delta
            #     while abs(x_curr - self.pointTo.x) > 0.1 :
            #         y_curr = -(self.c + self.a*x_curr )/ self.b
            #         plt.scatter(x_curr, y_curr, s=1)
            #         x_curr += delta
            #     return
            # else:
            #     y_curr = min(self.pointFrom.y, self.pointTo.y)
            #     y_max = max(self.pointFrom.y, self.pointTo.y)
            #     while abs(y_max - y_curr) > 0.1:
            #         plt.scatter(x_curr, y_curr, s=1)
            #         y_curr += delta
            #     return

        x = 0
        y = 0
        if self.pointFrom:
            x = self.pointFrom.x
            y = self.pointFrom.y
        if self.pointTo:
            x = self.pointTo.x
            y = self.pointTo.y

        x_end = 3*self.vectorX + x
        if x_end < x:
            delta = - delta

        while abs(x_end - x) > 0.05:
            y = -(self.c + self.a*x )/ self.b
            plt.scatter(x, y, s=1)
            x += delta


    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow((x1 - x2),2) + math.pow((y1 - y2), 2))

    def __eq__(self, other):
        return (self.face1 == other.face1 and self.face2 == other.face2) or (self.face1 == other.face2 and self.face2 == other.face1)

    @staticmethod
    def findIntersectionPoint(line, edge):
        if abs(edge.a * line.b - edge.b * line.a) < 0.000001:
            return None
        y = (edge.c * line.a / edge.a - line.c) / (line.b - (line.a * edge.b / edge.a))
        x = -(edge.c + edge.b * y) / edge.a
        p = Point(x, y)
        return p




