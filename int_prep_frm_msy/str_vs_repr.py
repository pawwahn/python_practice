x = 4
print(repr(x))
print(type(repr(x)))
print(str(repr(x)))
print(type(str(repr(x))))


print("------------")
y = 'name'
print(repr(y))  # 'name'    -- you will see the quotes
print(type(repr(y)))
print(str(y))   # name      -- you can not see the quotes


print(type(repr(y)))

a = 'name'
str_a = str(a)
print(str_a)
rep_a = repr(a)
print(rep_a)
print(str_a == rep_a)