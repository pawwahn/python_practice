import re
import traceback
def checkEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    try:
        print('Valid')
        return bool(re.search(regex, email))
    except:
        print("not valid")
        return False

checkEmail('pav123d_ededd33_9eed.ddan@outloeejdddjjfok.commdddmm')