service_dict = [
    {'a':1, 'b':2},
    {'c':2, 'b':4},
]

twitter = {'e':5, 'f':6}

get_cluster_name = 'function_name()'

need_twitter = ['05-2', '06-1']

if '04-1' in need_twitter:
    print("===")
    service_dict.append(twitter)

print(service_dict)


test = {'a':1, 'b':2, 'c':['exception sent', 'No']}
if 'c' in test:
    print("key present")
    print(test['c'])