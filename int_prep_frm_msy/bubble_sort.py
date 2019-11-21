A = [1,4,2,1,2,8]
lnt = len(A)    #4
print(lnt)


def bubbly_sort(A):
    for i in range(lnt):
        print("---------------")
        print("value of i is {}".format(i))
        for j in range(lnt-1):
            print("value of j is {}".format(j))
            if A[j] > A[j+1]:
                print("value of A[j] is {}".format(A[j]))
                print("value of A[j+1] is {}".format(A[j+1]))
                A[j],A[j+1] = A[j+1],A[j]
                print(A)
            else:
                print("failed condition-- {}".format(A))
    print(A)

bubbly_sort(A)