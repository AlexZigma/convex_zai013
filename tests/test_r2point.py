from pytest import approx
from math import sqrt, pi
from r2point import R2Point


class TestR2Point:

    # Расстояние от точки до самой себя равно нулю
    def test_dist1(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(1.0, 1.0)) == approx(0.0)

    # Расстояние между двумя различными точками положительно
    def test_dist2(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(1.0, 0.0)) == approx(1.0)

    def test_dist3(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(0.0, 0.0)) == approx(sqrt(2.0))

    # Площадь треугольника равна нулю, если все вершины совпадают
    def test_area1(self):
        a = R2Point(1.0, 1.0)
        assert R2Point.area(a, a, a) == approx(0.0)

    # Площадь треугольника равна нулю, если все вершины лежат на одной прямой
    def test_area2(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 1.0), R2Point(2.0, 2.0)
        assert R2Point.area(a, b, c) == approx(0.0)

    # Площадь треугольника положительна при обходе вершин против часовой
    # стрелки
    def test_area3(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
        assert R2Point.area(a, b, c) > 0.0

    # Площадь треугольника отрицательна при обходе вершин по часовой стрелке
    def test_area4(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
        assert R2Point.area(a, c, b) < 0.0

    # Точки могут лежать внутри и вне "стандартного" прямоугольника с
    # противопложными вершинами (0,0) и (2,1)
    def test_is_inside1(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 0.5).is_inside(a, b) is True

    def test_is_inside2(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 0.5).is_inside(b, a) is True

    def test_is_inside3(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 1.5).is_inside(a, b) is False

    # Ребро [(0,0), (1,0)] может быть освещено или нет из определённой точки
    def test_is_light1(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(0.5, 0.0).is_light(a, b) is False

    def test_is_light2(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(2.0, 0.0).is_light(a, b) is True

    def test_is_light3(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(0.5, 0.5).is_light(a, b) is False

    def test_is_light4(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(0.5, -0.5).is_light(a, b) is True

    def test_is_inside_cyrcle_1(self):
        a = R2Point(0, 0)
        r = 1
        assert a.is_inside_cyrcle(r) is True

    def test_is_inside_cyrcle_2(self):
        a = R2Point(1, 1)
        r = 1
        assert a.is_inside_cyrcle(r) is False

    def test_is_inside_cyrcle_3(self):
        a = R2Point(1, 1)
        r = 2
        assert a.is_inside_cyrcle(r) is True

    def test_area_sector_1(self):
        a, b = R2Point(-1, 0), R2Point(1, 0)
        r = 1
        assert R2Point.area_sector(a, b, r) == approx(pi/2)

    def test_area_sector_2(self):
        a, b = R2Point(0, 1), R2Point(1, 0)
        r = 1
        assert R2Point.area_sector(a, b, r) == approx(-pi/4)

    def test_area_sector_3(self):
        a, b = R2Point(0, 1), R2Point(0, 2)
        r = 1
        assert R2Point.area_sector(a, b, r) == 0

    def test_cross_cyrcle_1(self):
        a, b = R2Point(-2, 0), R2Point(2, 0)
        r = 1
        assert R2Point.cross_cyrcle(a, b, r) == [a, R2Point(-1, 0),
                                                 R2Point(1, 0), b]

    def test_cross_cyrcle_2(self):
        a, b = R2Point(0, 0), R2Point(2, 0)
        r = 1
        assert R2Point.cross_cyrcle(a, b, r) == [a, R2Point(1, 0), b]

    def test_cross_cyrcle_3(self):
        a, b = R2Point(0, 0), R2Point(0.5, 0)
        r = 1
        assert R2Point.cross_cyrcle(a, b, r) == [a, b]

    def test_cross_cyrcle_4(self):
        a, b = R2Point(0, 0), R2Point(0.5, 0)
        r = 1
        assert R2Point.cross_cyrcle(b, a, r) == [b, a]

    def test_area_edge_1(self):
        a, b = R2Point(1, 1), R2Point(-1, 1)
        r = 1
        assert R2Point.area_edge(a, b, r) == approx(pi/4)

    def test_area_edge_2(self):
        a, b = R2Point(-1, 0), R2Point(1, 0)
        r = 1
        assert R2Point.area_edge(a, b, r) == approx(0)

    def test_area_tr_cr_1(self):
        a, b, c = R2Point(0, 0), R2Point(2, 0), R2Point(0, 2)
        r = 1
        assert R2Point.area_tr_cr(a, b, c, r) == pi/4

    def test_area_tr_ring_1(self):
        a, b, c = R2Point(0, 0), R2Point(0, 3), R2Point(3, 0)
        assert R2Point.area_tr_ring(a, b, c) == approx((pi*4-pi)/4)

        # python -B -m pytest -p no:cacheprovider tests
# python -B -m pytest -p no:cacheprovider --cov=. .\tests\test_r2point.py
#   --cov-report=html
