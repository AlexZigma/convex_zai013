from math import sqrt, acos
from sympy import solve, symbols


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other: 'R2Point'):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False

    def __repr__(self):
        return (f'({self.x}, {self.y})')

    def is_inside_cyrcle(self, r):
        return self.dist(R2Point(0, 0)) <= r

    # @staticmethod
    # def dist_to_line(p1: 'R2Point', p2: 'R2Point') -> float:
    #     return 2*abs(R2Point.area(R2Point(0, 0), p1, p2)/p1.dist(p2))

    @staticmethod
    def area_sector(p1: 'R2Point', p2: 'R2Point', r: float) -> float:
        a = (p1.x*p2.x+p1.y*p2.y) / \
            (p1.dist(R2Point(0, 0)) * p2.dist(R2Point(0, 0)))
        alpha = acos(round(a, 8))
        return (alpha*r**2)/2 * (-1 if R2Point(0, 0).is_light(p1, p2) else 1)

    @staticmethod
    def cross_cyrcle(a: 'R2Point', b: 'R2Point', r: float) -> list:
        x, y = symbols('x, y', real=True)
        x1, y1, x2, y2 = a.x, a.y, b.x, b.y
        sol = solve([(x-x1)*(y2-y1)-(x2-x1)*(y-y1), x**2+y**2-r**2], x, y)
        lst = []
        for s in sol:
            p1, p2 = s[0], s[1]
            if (x1 <= p1 <= x2 or x2 <= p1 <= x1) and\
                    (y1 <= p2 <= y2 or y2 <= p2 <= y1):
                lst.append((p1, p2))

        lst = [R2Point(float(p[0]), float(p[1])) for p in lst]
        lst = sorted(lst, key=lambda x: (x.x, x.y))
        if a.x > b.x or a.x == b.x and a.y > b.y:
            lst = lst[::-1]
        return [a] + lst + [b]

    def area_edge(p1: 'R2Point', p2: 'R2Point', r: float):
        points = R2Point.cross_cyrcle(p1, p2, r)
        area = 0
        for i in range(len(points)-1):
            if (points[i].is_inside_cyrcle(r) and
                    points[i+1].is_inside_cyrcle(r)):
                area += R2Point.area(points[i], points[i+1], R2Point(0, 0))
            else:
                area += R2Point.area_sector(points[i], points[i+1], r)
        return area

    def area_tr_cr(p1, p2, p3, r):
        area = (R2Point.area_edge(p1, p2, r) +
                R2Point.area_edge(p2, p3, r) +
                R2Point.area_edge(p3, p1, r))
        return area

    def area_tr_ring(p1, p2, p3):
        if not p2.is_light(p1, p3):
            p1, p3 = p3, p1
        area = (R2Point.area_tr_cr(p1, p2, p3, 2) -
                R2Point.area_tr_cr(p1, p2, p3, 1))
        return area


if __name__ == "__main__":
    # x = R2Point(1.0, 1.0)
    # print(type(x), x.__dict__)
    # print(x.dist(R2Point(1.0, 0.0)))
    # a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    # print(R2Point.area(a, c, b))
    p1 = R2Point(4, 4)
    p2 = R2Point(-3, 1)
    p3 = R2Point(3, 3)
    r = 1

    # print(R2Point.area_tr_cr(p1, p2, p3, r))
    print(R2Point.area_tr_ring(p1, p3, p2))
    # print(acos(-.2))
    # print(R2Point.area_edge(p1, p2, 2))
    # print(R2Point.area_sector(R2Point(0, 2), p3, 2))
    # print(R2Point.area_tr_ring(p1, p2, p3))
    # [print(x) for x in R2Point.cross_cyrcle(p2, p1, r)]
