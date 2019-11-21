# We have one candle of height 1, one candle of height 2, and two candles of height 3.
# Your niece only blows out the tallest candles, meaning the candles where height=3.
# Because there are  such candles, we print 2 on a new line.

a = [1,2,1,4,2,1,2,5,4,5]

size = len(a)
print(size)

max_value = max(a)
print(max_value)
no_of_max_values = a.count(max_value)
print(no_of_max_values)

