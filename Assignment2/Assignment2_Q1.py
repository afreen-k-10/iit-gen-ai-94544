#Exercise 1: Create a math_utils module with functions for area calculations
import math
def area_circle(r):
    return math.pi*r*r
def area_square(len):
    return len*len
def area_rectangle(len, br):
    return len * br

if __name__=="__main__":
    print("Area of Circle : ", area_circle(10))
    print("Area of Square : ", area_square(10))
    print("Area of Rectangle : ", area_rectangle(10, 5))