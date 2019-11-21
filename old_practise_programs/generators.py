def remote_control():
    yield  "HBO"
    yield  "AXN"
    yield  "CNN"

itr = remote_control()
print itr       #   generator object
print next(itr)
print next(itr)
print next(itr)
#print next(itr)