num=input("Enter numbers in the list:")
list=num.split(',')

count_even=0
count_odd=0
for numbers in list:
    print(numbers)
    if int(numbers)%2==0:
         count_even+=1
    else:
         count_odd+=1
print("The total of even numbers is:",count_even)
print("The total of odd numbers is:",count_odd)