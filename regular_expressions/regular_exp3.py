# find all the words of 'inform' in the string
import re

str = "count num of words with the word inform and informs to the team regarding the 'inform' word count information"

k = re.findall('inform', str)

print k
print len(k)