dc = {'aa':'apple', 'bb':'ball and bat', 'cc':'cat'}
z = 'biggline here'
dc['aa'] = z[0:5]
strng = "<a>aa</a><b>bb</b><c>cc</c>"
new_strng = ""


for k in dc.keys():
    new_strng = strng.replace(k, dc[k])
    strng = new_strng

print new_strng


# new_strng = strng.replace('aa', dc['aa'])
# new_strng = new_strng.replace('bb', dc['bb'])
# new_strng = new_strng.replace('cc', dc['cc'])
print(strng)
# print new_strng