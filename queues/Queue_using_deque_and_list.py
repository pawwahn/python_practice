from collections import deque

queue = deque(['a','b','c'])
print("type is :",type(queue))
print(queue)
queue.append('d')
print(queue)
queue.append('e')
print(queue)
print("pop-->",queue.pop())
print(queue)
print("popleft-->",queue.popleft())     # popleft is available only in deque library
print(queue)
queue.insert(0,'1')
print(queue)