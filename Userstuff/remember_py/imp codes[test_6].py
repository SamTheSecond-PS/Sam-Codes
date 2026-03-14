numbers = [5,2,5,2,2,]
for number in numbers:
    output = ''
    for count in range(number):
        output += 'L'
    print(output)


names = ['john','smith','Sam','sarah','laurel']
names[0]='jon'#replacing a name in the list with another
print(names[1:4])#printing part of the list

numbers = [1,2,3,4,5]
max = numbers[0]
for number in numbers:
    if number > max:
        max = number
print(max)#how to find largest number in a list.

matrix = [
    [1,2,3],#how to make a matrix
    [4,5,6],
    [7,8,9]
]
print(matrix[0][1])#printing a part of the matrix
for row in matrix:
    for item in row:
        print(item)#printing all the items in the list in a vertical(_____) way

numbers = [1,2,3,4,5]
numbers.append(20)#used to enter a number at the last of the list[or name]
print(numbers)

numbers = [1,2,3,4,5]
numbers.insert(0, 10)#first num. which place to enter the number,second number-
#what object to enter
print(numbers)

numbers = [1,2,3,4,5]
numbers.remove(5)#to remove a number from the list
print(numbers)

numbers = [1,2,3,4,5]
numbers.clear()#to clear[remove] the whole list
print(numbers)

numbers = [1,2,3,4,5]
numbers.pop()#to remove the last number from the list
print(numbers)

numbers = [1,2,3,4,5]
print(numbers.index(3))#to show the first appearance of the number

numbers = [1,2,3,4,5]
print(50 in numbers)#to check if a number is in the list,and shoes true or false as result

numbers = [1,2,3,4,5,5]
print(numbers.count(5))#to show how much time a number has appeared on the list

numbers = [1,2,3,4,5]
numbers.sort()#to sort the list in ascending order
print(numbers)

numbers = [1,2,3,4,5]
numbers.sort()
numbers.reverse()#gives the list in descending order.
print(numbers)

numbers = [1,2,3,4,5]
numbers2 = numbers.copy()#copies the list
numbers2.append(6)
print(numbers2)

dup = [1,2,3,3,4,5,5,6,7]
unique = []
for number in dup:
    if number not in unique:
        unique.append(number)
print(unique)#to remove the duplicates and only put one of the number in the list

