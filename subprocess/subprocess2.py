# for pinging

import subprocess
host = 'www.google.com'
p = subprocess.Popen(['ping', '-c 2', host],stdout=subprocess.PIPE,shell=True)
output = p.communicate()[0]