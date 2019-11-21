arr = [900, 940, 950, 1100, 1500, 1800]
dep = [910, 1200, 1120, 1130, 1900, 2000]

sorted_arr = sorted(arr)
sorted_dep = sorted(dep)

# print(sorted_arr)
# print(sorted_dep)

sorted_arr.extend(sorted_dep)

new_sort = sorted(sorted_arr)
plat_needed = 0
check_for_highest_platform = []
print(new_sort)
for i in new_sort:
    if i in arr:
        plat_needed+=1
        check_for_highest_platform.append(plat_needed)
    else:
        plat_needed-=1
        check_for_highest_platform.append(plat_needed)
print(check_for_highest_platform)
print(max(check_for_highest_platform))