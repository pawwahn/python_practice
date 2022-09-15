# Python program to
# demonstrate queue implementation
# using list

# Initializing a queue
queue = []

# Adding elements to the queue
queue.append('a')
print(queue)
queue.append('b')
print(queue)
queue.append('c')

print("Initial queue")
print(queue)

# Removing elements from the queue
print("\nElements dequeued from queue")
print(queue.pop(0))
print(queue)
print(queue.pop(0))
print(queue.pop(0))
print(queue)

#print(queue.pop(0))    # can not remove elements from an empty list and it throws error

print("\nQueue after removing elements")
print(queue)

# Uncommenting print(queue.pop(0))
# will raise and IndexError
# as the queue is now empty
