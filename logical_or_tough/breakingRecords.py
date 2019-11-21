#score = [3, 4, 21, 36, 10, 28, 35, 5, 24, 42]
score = [10, 5, 20, 20, 4, 5, 2, 25, 1]
no_of_matches = len(score)

highest_break_count = 0
least_worst_count = 0

highest_score = score[0]
least_score = score[0]

for i in range(no_of_matches):
    if score[i]>highest_score:
        highest_score = score[i]
        highest_break_count+=1
    if score[i]<least_score:
        least_score = score[i]
        least_worst_count+=1
print(highest_break_count, least_worst_count)
