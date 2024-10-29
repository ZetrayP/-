import math


class Shape:
    def area(self):
        raise NotImplementedError("Should be overridden by subclasses")
    
    def perimeter(self):
        raise NotImplementedError("Should be overridden by subclasses")
    
    def compare_area(self, other):
        if self.area() > other.area():
            return "This shape has a larger area."
        elif self.area() < other.area():
            return "This shape has a smaller area."
        else:
            return "Both shapes have the same area."
        
    def compare_perimeter(self, other):
        if self.perimeter() > other.perimeter():
            return "This shape has a larger perimeter."
        elif self.perimeter() < other.perimeter():
            return "This shape has a smaller perimeter."
        else:
            return "Both shapes have the same perimeter."


class Square(Shape):
    def __init__(self, side):
        self.side = side
        
    def area(self):
        return self.side ** 2
    
    def perimeter(self):
        return 4 * self.side


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        
    def area(self):
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def perimeter(self):
        return self.a + self.b + self.c


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
        
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius


square = Square(4)
rectangle = Rectangle(4, 5)
triangle = Triangle(3,4,5)
circle = Circle(3)

print(square.area())
print(circle.area())
print(square.compare_area(circle))

print(triangle.area())
print(square.compare_area(triangle))

print(square.perimeter())
print(circle.perimeter())
print(square.compare_perimeter(circle))

print(rectangle.perimeter())
print(square.compare_perimeter(rectangle))