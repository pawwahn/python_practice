a = [1,2,1,2,2,1,1]     # 1 can form 2 pairs as there r 4 count, 2 can form 1 pair as there are 3 count
unique_list = []
total_pairs_count = 0


for i in a:
    if i not in unique_list:
        unique_list.append(i)
        cnt = a.count(i)
        #print("---------count of {} is {}".format(i,cnt))


        if cnt%2 == 0:
            pair_cnt = int(cnt/2)
            total_pairs_count = total_pairs_count+pair_cnt
            #print("Even pairs count is --> {}".format(pair_cnt))
        else:
            pair_cnt = int((cnt-1)/2)
            print("odd pairs count is --> {}".format(pair_cnt))
            total_pairs_count = total_pairs_count + pair_cnt
#return total_pairs_count
print(total_pairs_count)