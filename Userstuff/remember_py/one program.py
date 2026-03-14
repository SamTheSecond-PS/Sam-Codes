from collections import deque
from array import array
from sys import getsizeof
from pprint import pprint

items = [
    ("product1", 10),
    ("product2", 9),
    ("product3", 12)
]

prices = list(map(lambda item: item[1] > 10, items))
print(prices)

list1 = [1, 2, 3]
list2 = [3, 2, 1]

z = zip(list1, list2)
print(z)
print("confirmed")#
queue = deque([])
queue.append(1)
queue.append(2)
queue.append(3)
queue.popleft()
print(queue)

numbers = array('i', [1, 2, 3])
numbers.append(4)

numbers = [1 ,1 ,2, 3, 4]
first = set(numbers)
second = {1, 5}
print(first | second)
print(first & second)

point = dict(x=1, y=2)

print(*numbers)
print("_____________")
sentence = "This is a common interview question"
char_freq = {}
for char in sentence:
    if char in char_freq:
        char_freq[char] += 1
    else:
        char_freq[char] = 1
pprint(sorted(char_freq.items(), key=lambda x: x[1], reverse=True))
