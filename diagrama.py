from unittest import mock
from point import Point
from edge import Edge
from vertex import Vertex
import math
import matplotlib.pyplot as plt


def isLeft(a, b, c):
    return ((b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)) > 0


def checkIntersectForBorders(edge, point):
    if not edge.pointTo and not edge.pointTo:
        return point
    if edge.pointFrom and edge.pointTo:
        min_x = min(edge.pointTo.x, edge.pointFrom.x)
        max_x = min(edge.pointTo.x, edge.pointFrom.x)
        if point.x > min_x and point.x < max_x:
            return point
        else:
            return None
    if edge.pointTo:
        p = edge.pointTo
    else:
        p = edge.pointFrom
    v_x = point.x - p.x
    lamda = v_x/edge.vectorX
    if lamda > 0:
        return point
    else:
        return None


class Diagrama:
    def __init__(self):
        self.edges = []
        self.vertexes = []
        self.convexHull = []

    @staticmethod
    def direction(p, q, qnext):
        return (q.x - p.x) * (qnext.x - p.x) + (q.y - p.y) * (
                qnext.y - p.y)

    @staticmethod
    def pointPosition(p, q, qnext):
        t1 = qnext.point.x - p.point.x
        t2 = qnext.point.y - p.point.y
        d1 = q.point.x - p.point.x
        d2 = q.point.y - p.point.y
        return d1 * t2 - d2 * t1

    @staticmethod
    def convexHull(d1, d2):
        p = max(d1.convexHull, key=lambda vertex: vertex.point.x)

        # get the leftmost poitn of right convex hull
        if len(d2.convexHull) != 1:
            q = min(d2.convexHull, key=lambda vertex: vertex.point.x)
        else:
            q = d2.convexHull[0]

        # make copies of p and q
        cp_p = p
        cp_q = q

        # raise the bridge pq to the uper tangent
        prev_p = None
        prev_q = None
        while (True):
            prev_p = p
            prev_q = q
            if q.cw_next:
                # move p clockwise as long as it makes left turn
                # take care of coliniarity
                while Diagrama.pointPosition(p, q, q.cw_next) >= 0:
                    q = q.cw_next
            if p.ccw_next:
                # move p as long as it makes right turn
                while Diagrama.pointPosition(q, p, p.ccw_next) <= 0:
                    p = p.ccw_next

            if p == prev_p and q == prev_q:
                break

        # lower the bridge cp_p cp_q to the lower tangent
        prev_p = None
        prev_q = None
        while (True):
            prev_p = cp_p
            prev_q = cp_q
            if cp_q.ccw_next:
                # move q as long as it makes right turn
                while Diagrama.pointPosition(cp_p, cp_q, cp_q.ccw_next) <= 0:
                    cp_q = cp_q.ccw_next
            if cp_p.cw_next:
                # move p as long as it makes left turn
                while Diagrama.pointPosition(cp_q, cp_p, cp_p.cw_next) >= 0:
                    cp_p = cp_p.cw_next
            if cp_p == prev_p and cp_q == prev_q:
                break

        # remove all other points
        p.cw_next = q
        q.ccw_next = p

        cp_p.ccw_next = cp_q
        cp_q.cw_next = cp_p

        # final result
        result = []
        start = p
        while (True):
            result.append(p)
            p = p.ccw_next

            if p == start:
                break

        return result, p, q, cp_p, cp_q

    @staticmethod
    def unite(d1, d2):
        d = Diagrama()
        cH, p, q, cp_p, cp_q = Diagrama.convexHull(d1, d2)
        d.convexHull.extend(cH)
        d.vertexes.extend(d1.vertexes)
        d.vertexes.extend(d2.vertexes)
        d.edges.extend(d2.edges)
        d.edges.extend(d1.edges)
        flag = False

        while not (p.point == cp_p.point and q.point == cp_q.point):

            possibleEdges = Diagrama.getPossibleEdges(p, q)
            points, line = Diagrama.getIntersections(possibleEdges, p, q)
            e = Edge(line.a, line.b, line.c, p)
            e.face1 = d.getVertex(p.point.x, p.point.y)
            e.face2 = d.getVertex(q.point.x, q.point.y)
            e.face1.edges.append(e)
            e.face2.edges.append(e)
            if flag:
                e.pointFrom = nextPoint

            if flag:
                nextPoint = Diagrama.getNextPointFromAllIntersections(points, nextPoint)
            else:
                nextPoint = Diagrama.getNextPointFromAllIntersections(points)
                y = nextPoint.y + 1
                x = -(e.c + e.b * y) / e.a
                e.vectorX = x - nextPoint.x
                e.vectorY = y - nextPoint.y
                flag = True

            e.pointTo = Point(nextPoint.x, nextPoint.y)
            d.edges.append(e)

            y_h = nextPoint.y + 1
            y_l = nextPoint.y - 1
            e_x = -(e.c + e.b * y_h) / e.a
            pE = Point(e_x, y_h)

            if nextPoint.edge in d1.edges:
                if nextPoint.edge.pointFrom and nextPoint.edge.pointTo:
                    if isLeft(pE, nextPoint, nextPoint.edge.pointFrom):
                        nextPoint.edge.pointFrom = nextPoint.x
                    if isLeft(pE, nextPoint, nextPoint.edge.pointTo):
                        nextPoint.edge.pointTo = nextPoint.x
                        # if verticaly
                if not nextPoint.edge.pointFrom and not nextPoint.edge.pointTo:
                    nextPoint.edge.pointFrom = Point(nextPoint.x, nextPoint.y)

                    x_h = -(nextPoint.edge.c + nextPoint.edge.b * y_h) / nextPoint.edge.a
                    x_l = -(nextPoint.edge.c + nextPoint.edge.b * y_l) / nextPoint.edge.a
                    pH = Point(x_h, y_h)
                    pL = Point(x_l, y_l)

                    if isLeft(pE, nextPoint, pH):
                        nextPoint.edge.vectorX = x_l - nextPoint.x
                        nextPoint.edge.vectorY = y_l - nextPoint.y
                    else:
                        nextPoint.edge.vectorX = x_h - nextPoint.x
                        nextPoint.edge.vectorY = y_h - nextPoint.y

                else:

                    if nextPoint.edge.pointFrom:
                        if isLeft(pE, nextPoint, nextPoint.edge.pointFrom):
                            nextPoint.edge.pointFrom = Point(nextPoint.x, nextPoint.y)
                        else:
                            nextPoint.edge.pointTo = Point(nextPoint.x, nextPoint.y)
                    else:
                        if nextPoint.edge.pointTo:
                            if isLeft(pE, nextPoint, nextPoint.edge.pointTo):
                                nextPoint.edge.pointTo = Point(nextPoint.x, nextPoint.y)
                            else:
                                nextPoint.edge.pointFrom = Point(nextPoint.x, nextPoint.y)
            else:
                if nextPoint.edge.pointFrom and nextPoint.edge.pointTo:
                    if isLeft(pE, nextPoint, nextPoint.edge.pointFrom):
                        nextPoint.edge.pointTo = nextPoint.x
                    if isLeft(pE, nextPoint, nextPoint.edge.pointTo):
                        nextPoint.edge.pointFrom = nextPoint.x
                        # if verticaly
                if not nextPoint.edge.pointFrom and not nextPoint.edge.pointTo:
                    nextPoint.edge.pointFrom = Point(nextPoint.x, nextPoint.y)
                    y_h = nextPoint.y + 1
                    y_l = nextPoint.y - 1
                    e_x = -(e.c + e.b * y_h) / e.a
                    x_h = -(nextPoint.edge.c + nextPoint.edge.b * y_h) / nextPoint.edge.a
                    x_l = -(nextPoint.edge.c + nextPoint.edge.b * y_l) / nextPoint.edge.a
                    pH = Point(x_h, y_h)
                    pL = Point(x_l, y_l)
                    pE = Point(e_x, y_h)
                    if isLeft(pE, nextPoint, pL):
                        nextPoint.edge.vectorX = x_l - nextPoint.x
                        nextPoint.edge.vectorY = y_l - nextPoint.y
                    else:
                        nextPoint.edge.vectorX = x_h - nextPoint.x
                        nextPoint.edge.vectorY = y_h - nextPoint.y

                else:

                    if nextPoint.edge.pointFrom:
                        if isLeft(pE, nextPoint, nextPoint.edge.pointFrom):
                            nextPoint.edge.pointTo = Point(nextPoint.x, nextPoint.y)
                        else:
                            nextPoint.edge.pointFrom = Point(nextPoint.x, nextPoint.y)
                    else:
                        if nextPoint.edge.pointTo:
                            if isLeft(pE, nextPoint, nextPoint.edge.pointTo):
                                nextPoint.edge.pointFrom = Point(nextPoint.x, nextPoint.y)
                            else:
                                nextPoint.edge.pointTo = Point(nextPoint.x, nextPoint.y)

            if nextPoint.face1 == p:
                p = nextPoint.face2
                continue
            if nextPoint.face2 == p:
                p = nextPoint.face1
                continue
            if nextPoint.face1 == q:
                q = nextPoint.face2
                continue
            if nextPoint.face2 == q:
                q = nextPoint.face1
                continue

        e = Edge()
        e.a, e.b, e.c = Diagrama.getLineEquition(p, q)
        e.pointFrom = nextPoint
        e.face1 = d.getVertex(p.point.x, p.point.y)
        e.face2 = d.getVertex(q.point.x, q.point.y)
        e.face1.edges.append(e)
        e.face2.edges.append(e)
        d.edges.append(e)
        y = nextPoint.y - 1
        x = -(e.c + e.b * y) / e.a
        e.vectorX = x - nextPoint.x
        e.vectorY = y - nextPoint.y

        d.Paint()
        return d

    @staticmethod
    def distance(x1, y1, x2, y2):
        return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))

    @staticmethod
    def getPossibleEdges(p, q):
        possibleEdges = []
        possibleEdges.extend(p.edges)
        possibleEdges.extend(q.edges)
        return possibleEdges

    @staticmethod
    def getIntersections(possibleEdges, p, q):
        points = []

        line = mock.Mock()
        line.a, line.b, line.c = Diagrama.getLineEquition(p, q)

        for x in possibleEdges:
            p = Diagrama.findIntersectionPoint(line, x)
            p = checkIntersectForBorders(x, p)
            if p:
                p.face1 = x.face1
                p.face2 = x.face2
                p.edge = x
                points.append(p)

        return points, line

    @staticmethod
    def getNextPointFromAllIntersections(intersections, pointFrom=""):
        if pointFrom:
            intersections.sort(key=lambda point: point.y, reverse=True)
            for x in intersections:
                if x.y <= pointFrom.y and x != pointFrom:
                    return x

        else:
            p = max(intersections, key=lambda point: point.y)
            return p

    @staticmethod
    def findIntersectionPoint(line, edge):
        if abs(edge.a * line.b - edge.b * line.a) < 0.000001:
            return None
        y = (edge.c * line.a / edge.a - line.c) / (line.b - (line.a * edge.b / edge.a))
        x = -(edge.c + edge.b * y) / edge.a
        p = Point(x, y)
        return p

    @staticmethod
    def getLineEquition(p, q):
        x_center = (p.point.x + q.point.x) / 2
        y_center = (p.point.y + q.point.y) / 2

        a_line = q.point.y - p.point.y
        b_line = -(q.point.x - p.point.x)
        """c_line = x1.y(x2.x - x1.x) - x1.x(x2.y - x1.y)"""

        a_perp = -b_line
        b_perp = a_line
        c_perp = -b_perp * y_center - a_perp * x_center

        return a_perp, b_perp, c_perp

    def getVertex(self, x, y):
        v = Vertex(Point(x, y))
        for x in self.vertexes:
            if x == v:
                return x

    def Paint(self):
        for x in self.vertexes:
            plt.scatter(x.point.x, x.point.y, s=10)

        for y in self.edges:
            y.draw(plt, self)

        plt.show()
