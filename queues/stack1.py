import queue
# In stack, LIFO(Last In - First Out), the recently added element will be removed from the stack
L = queue.LifoQueue(maxsize=5)
print(L.qsize())    # 0 as there are no elements dat r added tot he stack

L.put(10)
L.put(20)
L.put(30)
#print("is stack full ?:",L.full())
L.put(40)
print("queue size is:",L.qsize())
print("removed element is :",L.get())
print("queue size is:",L.qsize())
print("queue size is:",L.qsize())
print("is empty ?:",L.empty())

print(L.get())
print("queue size is:",L.qsize())