# Count of index pairs with equal elements in an array
# Given an array of n elements. The task is to count the total number of indices (i, j) such that arr[i] = arr[j] and i != j
#
# Examples :
#
# Input : arr[] = {1, 1, 2}
# Output : 1
# As arr[0] = arr[1], the pair of indices is (0, 1)
#
# Input : arr[] = {1, 1, 1}
# Output : 3
# As arr[0] = arr[1], the pair of indices is (0, 1),
# (0, 2) and (1, 2)
#
# Input : arr[] = {1, 2, 3}
# Output : 0


def countPairs(arr, n):
    ans = 0

    # for each index i and j
    for i in range(0, n):
        for j in range(i + 1, n):

            # finding the index
            # with same value but
            # different index.
            if (arr[i] == arr[j]):
                ans += 1
    return ans