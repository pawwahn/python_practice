import re
content = """This method either returns None
 (if the pattern doesn’t match), or a re.MatchObject that 
 contains information about the matching part of the string. 
 This method stops after the first match, so this is best suited 
 for testing a regular expression more than extracting data."""

search_word = 'match'
search_word_list=[]
search_word_positions = re.finditer(search_word, content)
print(search_word_positions)
for i in search_word_positions:
    search_word_list.append(i.span())
print(search_word_list)