from edge import Edge
from point import Point
from diagrama import Diagrama
from vertex import Vertex


def isLeft(a, b, c):
     return ((b.X - a.X)*(c.Y - a.Y) - (b.Y - a.Y)*(c.X - a.X)) > 0


def split(points, indexStrart, indexEnd):
    if indexEnd - indexStrart == 1 :
        d = Diagrama()

        if points[indexStrart].x < points[indexEnd].x:
            x1 = points[indexStrart]
            x2 = points[indexEnd]
        if points[indexStrart].x == points[indexEnd].x:
            if points[indexStrart].y < points[indexEnd].y:
                x1 = points[indexStrart]
                x2 = points[indexEnd]
            else :
                x2 = points[indexStrart]
                x1 = points[indexEnd]
        else :
            print("x1:")
            print(points[indexStrart].x)
            print(points[indexStrart].y)
            print("x2:")
            print(points[indexEnd].x)
            print(points[indexEnd].y)

        y_center = (x1.y + x2.y)/2
        x_center = (x1.x + x2.x)/2

        a_line = x2.y - x1.y
        b_line = -(x2.x - x1.x)
        """c_line = x1.y(x2.x - x1.x) - x1.x(x2.y - x1.y)"""

        a_perp = -b_line
        b_perp = a_line
        c_perp = -b_perp*y_center - a_perp*x_center

        v1 = Vertex(x1)
        v2 = Vertex(x2)

        v1.cw_next = v2
        v1.ccw_next = v2
        v2.ccw_next = v1
        v2.cw_next = v1

        d.vertexes.append(v1)
        d.vertexes.append(v2)

        e1 = Edge(a_perp, b_perp, c_perp, v1, v2)

        d.convexHull.append(v1)
        d.convexHull.append(v2)

        v1.edges.append(e1)
        v2.edges.append(e1)

        d.edges.append(e1)

        return d

    if indexEnd == indexStrart:
        d = Diagrama()
        x = points[indexStrart]
        v = Vertex(x)

        d.convexHull.append(v)
        d.vertexes.append(v)
        return d
    else :
        d1 = split(points, indexStrart, indexStrart + (indexEnd - indexStrart) // 2)
        d2 = split(points, indexStrart + (indexEnd - indexStrart) // 2 + 1, indexEnd )
        return Diagrama.unite(d1, d2)



def main():
    points = []

    points.append(Point(1,6))
    points.append(Point(3,3))
    points.append(Point(4,4))
    points.append(Point(5,7))
    points.append(Point(6,2))
    points.append(Point(8,9))
    points.append(Point(9,12))
    points.append(Point(11,3))

    #points.append(Point(1,4))
    #points.append(Point(5,4))
    #points.append(Point(7,6))
    #points.append(Point(8,1))
    d = split(points, 0 , len(points) - 1)
    d.Paint()


if __name__ == '__main__':
    main()