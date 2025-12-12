import calculator
import greet
import geometry
n1=int(input("Enter first number:"))
n2=int(input("Enter second number:"))
calculator.add(n1,n2)
calculator.subtract(n1,n2)
calculator.multiply(n1,n2)
calculator.divide(n1,n2)
name=input("Enter your name:")
greet.greet(name)
length=int(input("Enter length of rectangle:"))
breadth=int(input("Enter breadth of rectangle:"))
geometry.area(length,breadth)
geometry.perimeter(length,breadth)

