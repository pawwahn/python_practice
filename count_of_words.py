str = 'as asjd dgfij dfg sg reigerg wergio g wf fw wf wjwfjclwpqw pqor ava  wpor wf wf wel qeorig rgj '

wordList = str.split()

print("Words:",len(wordList)) # prints number of words in the file.

a_words = 0

count = 0
for a_words in wordList:
    if a_words[0]=='a':
        count = count+1
        print(a_words, "start with the letter 'a'.")
print("total count of words that are found with a are: {}".format(count))