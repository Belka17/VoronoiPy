from edge import Edge
from point import Point
from diagrama import Diagrama
from vertex import Vertex


def isLeft(a, b, c):
     return ((b.X - a.X)*(c.Y - a.Y) - (b.Y - a.Y)*(c.X - a.X)) > 0


def split(points, indexStrart, indexEnd):
    if indexEnd - indexStrart == 1 :
        d = Diagrama()

        x1 = points[indexStrart]
        x2 = points[indexEnd]

        y_center = (x1.y + x2.y)/2
        x_center = (x1.x + x2.x)/2

        e1 = Edge()
        e2 = Edge()

        k_otrezka = (x2.x - x1.x)/(x2.y - x1.y);

        b_line =  y_center + k_otrezka*x_center

        e1.a = 1
        e1.b = k_otrezka
        e1.c = -b_line

        e2.a = 1
        e2.b = k_otrezka
        e2.c = -b_line

        e1.face = x1
        e2.face = x2

        v1 = Vertex(points[indexStrart], e1)
        v2 = Vertex(points[indexStrart], e2)
        d.vertexes.append(v1)
        d.vertexes.append(v2)

        d.convexHull.append(x1)
        d.convexHull.append(x2)

        d.edges(e1)
        d.edges(e2)

        return d
    if indexEnd == indexStrart :
        d = Diagrama()
        x = points[indexStrart]
        v = Vertex(x)

        d.convexHull.append(v)
        return d
    else :
        d1 = split(points, indexStrart, indexStrart + (indexEnd - indexStrart) // 2)
        d2 = split(points, indexStrart + (indexEnd - indexStrart) // 2 + 1, indexEnd )
        return Diagrama.unite(d1, d2)



def main():
    points = []

    points.append(Point(3,3))
    points.append(Point(5,5))
    points.append(Point(3,3))
    points.append(Point(5,6))
    points.append(Point(7,6))
    points.append(Point(7,9))
    split(points, 0 , len(points) - 1)


if __name__ == '__main__':
    main()