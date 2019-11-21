import subprocess
process = subprocess.Popen(['ls','-l'] , stdout=subprocess.PIPE)
process.communicate()