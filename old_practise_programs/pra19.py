def testgen(index):
  weekdays = ['sun','mon','tue','wed','thu','fri','sat']
  yield weekdays[index]
  yield weekdays[index+1]
  yield weekdays[index+2]
 
day = testgen(0)
print day
print next(day)