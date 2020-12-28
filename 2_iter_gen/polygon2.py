import math
import numbers

class Polygon():
    def __init__(self, edges, circumradius):
        if edges < 3 or circumradius <= 0:
            raise ValueError('Polygon can not be constructed from passed data.')
        self.edges = edges                             #n
        self.circumradius = circumradius               #R
        self._in_angle = None
        self._edge_length = None
        self._apothem = None
        self._area = None
        self._pol_perimeter = None

    #goal 1
    def __repr__(self):
        return f'Polygon(n={self.edges}, R={self.circumradius})'

    def __eq__(self, other):
        if isinstance(other, Polygon):
            return self.edges == other.edges and self.circumradius == other.circumradius

    def __gt__(self, other):
        if isinstance(other, Polygon):
            if self.edges == None:
                return self.edges
            return self.edges > other.edges
    
    # main properties
    @property
    def edges(self):
        return self._edges

    @property
    def circumradius(self):
        return self._circumradius

    @property
    def vertices(self): #variant atribute for edges
        return self.edges

    #main properties setters
    @edges.setter # if we set new value for instance attribute, calculated properties must be recalculated (None)
    def edges(self, edges):
        self._edges = edges
        self._in_angle = None
        self._edge_length = None
        self._apothem = None
        self._area = None
        self._pol_perimeter = None

    @circumradius.setter
    def circumradius(self, circumradius):
        self._circumradius = circumradius
        self._in_angle = None
        self._edge_length = None
        self._apothem = None
        self._area = None
        self._pol_perimeter = None

    @vertices.setter #unused
    def vertices(self, edges):
        self._edges = edges
        self._in_angle = None
    
    #calculated properties (lazy implementation)
    @property
    def in_angle(self):
        if self._in_angle is None: # can be 'is' also '==' - singleton object
            self._in_angle = (self._edges - 2) * 180 / self._edges
        return self._in_angle

    @property
    def edge_length(self): #s
        if self._edge_length == None:
            self._edge_length = 2 * self._circumradius * math.sin(math.pi / self._edges)
        return self._edge_length

    @property
    def apothem(self): #a
        if self._apothem == None:
            self._apothem = self._circumradius * math.cos(math.pi / self._edges)
        return self._apothem

    @property
    def area(self):
        if self._area == None:
            self._area = 0.5 * self._edges * self.edge_length * self.apothem
        return self._area

    @property
    def pol_perimeter(self):
        if self._pol_perimeter == None:
            self._pol_perimeter = self.edges * self.edge_length
        return self._pol_perimeter




    #goal 2
class Polygons():
    def __init__(self, edges):
        if edges < 3:
            raise ValueError('Polygon can not be constructed from passed data.')
        self.edges = edges
        self.circumradius = 10
        self._highest_area_per = None
    
    def __iter__(self):
        return self.PolygonsIterator(self._edges, self.circumradius)  #edges determines length of iterator
    
    @property
    def edges(self):
        return self._edges
    
    @edges.setter
    def edges(self, edges):
        self._edges = edges
        self._highest_area_per = None
    
    @property
    def highest_area_per(self): #may be implemented by sorted() function
        if self._highest_area_per == None: # lazy implementation
            x = 0
            for polygon in self.PolygonsIterator(self._edges, self.circumradius): #created polygons iterator for searching highest area / perimeter ratio
                ratio = polygon.area / polygon.pol_perimeter
                if ratio > x: # if ratio is bigger than previous value, it is stored and polygon is saved to property
                    x = ratio 
                    self._highest_area_per = polygon
        return self._highest_area_per 

    class PolygonsIterator():
        def __init__(self, length, circumradius):
            if length < 3: #somebody can call PolygonsIterator directly, thus check of input has to be performed
                raise ValueError('Polygon can not be constructed from passed data.')
            self.circumradius = circumradius
            self.length = length
            self.i = 3

        def __iter__(self):
            return self

        def __next__(self):
            if self.i > self.length:
                raise StopIteration
            else:
                result = Polygon(self.i, self.circumradius)
                self.i += 1
                return result

#project 1
plg = Polygon(10, 8)
plg2 = Polygon(8, 7)

#print(plg.edges)
#print(plg.num_vertices)
#print(plg.in_angle)
#print(plg.edge_length)
#print(plg.apothem)
#print(plg.area)
#print(plg.pol_perimeter)
#print(plg2 < plg)

#poly = Polygons(8)
#y = poly.highest_area_per # funkcia vracia Triedu, z ktorej som odvodil inštanciu
#print(y.in_angle)
#print(len(poly))


#project 2a - create lazy calculated properties

#print(plg.pol_perimeter)
#print(plg.pol_perimeter)

#plg.edges = 25

#print(plg.pol_perimeter)
#print(plg.pol_perimeter)

#project 2b - refactor Polygons into an iterable

poly = Polygons(8)

print(poly.highest_area_per)
print(poly.highest_area_per) #stored by lazy evaluation not calc again
print(poly.highest_area_per)

poly = Polygons(9)
po = iter(poly)
for _ in range(5):
    print(next(po))

print(list(poly)) # in this point exhausted

print(poly.highest_area_per)
print(poly.highest_area_per)




def test_polygon(): #test obtained from resources deep dive pt. 2 project 1 solution
    abs_tol = 0.001
    rel_tol = 0.001
    
    try:
        p = Polygon(2, 0)
        assert False, ('Creating a Polygon with 2 sides: '
                       ' Exception expected, not received')
    except ValueError:
        pass
                       
    n = 3
    R = 1
    p = Polygon(n, R)
    assert str(p) == 'Polygon(n=3, R=1)', f'actual: {str(p)}'
    assert p.vertices == n, (f'actual: {p.vertices},'
                                   f' expected: {n}')
    assert p.edges == n, f'actual: {p.edges}, expected: {n}'
    assert p.circumradius == R, f'actual: {p.circumradius}, expected: {n}'
    assert p.in_angle == 60, (f'actual: {p.in_angle},'
                                    ' expected: 60')
    n = 4
    R = 1
    p = Polygon(n, R)
    assert p.in_angle == 90, (f'actual: {p.in_angle}, '
                                    ' expected: 90')
    assert math.isclose(p.area, 2, 
                        rel_tol=abs_tol, 
                        abs_tol=abs_tol), (f'actual: {p.area},'
                                           ' expected: 2.0')
    
    assert math.isclose(p.edge_length, math.sqrt(2),
                       rel_tol=rel_tol,
                       abs_tol=abs_tol), (f'actual: {p.edge_length},'
                                          f' expected: {math.sqrt(2)}')
    
    assert math.isclose(p.pol_perimeter, 4 * math.sqrt(2),
                       rel_tol=rel_tol,
                       abs_tol=abs_tol), (f'actual: {p.pol_perimeter},'
                                          f' expected: {4 * math.sqrt(2)}')
    
    assert math.isclose(p.apothem, 0.707,
                       rel_tol=rel_tol,
                       abs_tol=abs_tol), (f'actual: {p.pol_perimeter},'
                                          ' expected: 0.707')
    p = Polygon(6, 2)
    assert math.isclose(p.edge_length, 2,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.apothem, 1.73205,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.area, 10.3923,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.pol_perimeter, 12,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.in_angle, 120,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    
    p = Polygon(12, 3)
    assert math.isclose(p.edge_length, 1.55291,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.apothem, 2.89778,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.area, 27,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.pol_perimeter, 18.635,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.in_angle, 150,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    
    p1 = Polygon(3, 10)
    p2 = Polygon(10, 10)
    p3 = Polygon(15, 10)
    p4 = Polygon(15, 100)
    p5 = Polygon(15, 100)
    
    assert p2 > p1
    assert p2 < p3
    assert p3 != p4
    assert p1 != p4
    assert p4 == p5

#test_polygon()