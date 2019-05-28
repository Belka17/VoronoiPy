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

        e1 = Edge()
        e2 = Edge()

        if x2.y - x1.y != 0:
            k_otrezka = (x2.x - x1.x)/(x2.y - x1.y)
            b_line = y_center + k_otrezka * x_center
        else:
            k_otrezka = 0
            b_line = x_center




        e1.a = 1
        e1.b = k_otrezka
        e1.c = -b_line

        e2.a = 1
        e2.b = k_otrezka
        e2.c = -b_line

        e1.face = x1
        e2.face = x2

        v1 = Vertex(x1, e1)
        v2 = Vertex(x2, e2, v1, v1)
        v1.cw_next = v2
        v1.ccw_next = v2
        d.vertexes.append(v1)
        d.vertexes.append(v2)

        d.convexHull.append(v1)
        d.convexHull.append(v2)

        d.edges.append(e1)
        d.edges.append(e2)

        return d
    if indexEnd == indexStrart :
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

    points.append(Point(1,4))
    points.append(Point(5,4))
    points.append(Point(7,6))
    points.append(Point(8,1))
    split(points, 0 , len(points) - 1)


if __name__ == '__main__':
    main()