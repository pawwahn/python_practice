def fast (items= []):
    items.append (1)
    return items

print(fast ())     #[1]
print(fast ())     #[1,1]