import queue

L = queue.Queue(maxsize=5)
print("Queue size before putting the values is :",L.qsize())

# data is inserted into the Queue by using put()
L.put(10)
L.put(20)
print("Queue size after putting few values is :",L.qsize())
L.put(30)
L.put(40)
print("is queue full ?? :",L.full())
L.put(50)
#L.put(60)    # queue size is 5 defined above, but u r adding element beyond its size. this is Overflow
print("Queue size is : ",L.qsize())
#print(L)
print("is queue full ?? :",L.full())

# data is extracted into the Queue by using get()
print(L.get())
print(L.get())
print(L.get())
print(L.get())
print(L.get())
#print(L.get()) # queue size is 5. u have removed 5 elements by using get(), so queue is empty. but
#still u r tryimg to remove elements from empty queue. This is underflow.
print("Queue size is : ",L.qsize())
print("is queue empty ??:",L.empty())