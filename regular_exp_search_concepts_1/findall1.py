import re
content = """This method either returns None
 (if the pattern doesn’t match), or a re.MatchObject that 
 contains information about the matching part of the string. 
 This method stops after the first match, so this is best suited 
 for testing a regular expression more than extracting data."""

search_word = 'match'
search_words_list = re.findall(search_word,content)
print(search_words_list)