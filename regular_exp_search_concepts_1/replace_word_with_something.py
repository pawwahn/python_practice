import re
content = """This method either returns None
 (if the pattern doesn’t match), or a re.MatchObject that 
 contains information about the matching part of the string. 
 This method stops after the first match, so this is best suited 
 for testing a regular expression more than extracting data."""

replace_word = 'match'
content = re.sub(replace_word,'\n MATCH', content)
print(content)