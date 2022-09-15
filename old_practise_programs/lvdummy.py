a = 10
b = None

if a in ['', ' ', None, 'None', 'NULL', 'Null'] or b in ['', ' ', None, 'None', 'NULL', 'Null']:
    print("False")
else:
    print("True")