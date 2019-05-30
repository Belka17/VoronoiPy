import math


class Edge :
    def __init__(self, a=None, b=None, c=None, face1=None, face2=None,pointFrom=None, pointTo=None):

        self.pointFrom = pointFrom
        self.pointTo = pointTo
        self.face1 = face1
        self.face2 = face2

        self.a = a
        self.b = b
        self.c = c

    def draw(self, plt):
        if self.pointTo and self.pointFrom:
            x_curr = self.pointFrom.x
            delta = 0.05
            if self.pointTo.x < self.pointFrom.x:
                delta = -delta
            while abs(x_curr - self.pointTo.x) > 0.1 :
                y_curr = -(self.c + self.a*x_curr )/ self.b
                plt.scatter(x_curr, y_curr, s=1)
                x_curr += delta
            return
        if self.pointFrom:
            x = self.pointFrom.x
        if self.pointTo:
            x = self.pointTo.x

        delta1 = 0.1
        delta2 = -delta1
        x_1 = x + delta1
        x_2 = x + delta2
        y_1 = -(self.c + self.a*x_1 )/ self.b
        y_2 = -(self.c + self.a*x_2 )/ self.b
        if self.distance(x_1, y_1, self.face1.point.x, self.face1.point.y) > self.distance(x_2, y_2, self.face1.point.x, self.face1.point.y):
            delta = delta2
        else:
            delta = delta1

        for i in range(0,70):
            y =  -(self.c + self.a*x )/ self.b
            plt.scatter(x, y, s=1)
            x = x + delta
        t = 5






    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow((x1 - x2),2) + math.pow((y1 - y2), 2))




