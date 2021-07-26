def conv(st):
    try:
        return int(st)
    except ValueError:  # If you get a ValueError
        return float(st)


l='10'

b = conv(l.strip(" \n").split(" ")[0])
print(b)
