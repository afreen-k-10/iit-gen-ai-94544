import arithmetic
from arithmetic import add
from arithmetic import sub

import geometry
from geometry import calc_rect_area
from geometry import calc_rect_peri

a=int(input("Enter a : "))
b=int(input("Enter b : "))
print(calc_rect_area(a,b))

a=int(input("Enter a : "))
b=int(input("Enter b : "))
print(calc_rect_peri(a,b))


print ("Hello world!!")

a=int(input("Enter a : "))
b=int(input("Enter b : "))
print(add(a,b))

a=int(input("Enter a : "))
b=int(input("Enter b : "))
print(sub(a,b))