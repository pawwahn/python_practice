# import subprocess
# process = subprocess.Popen(['ls','-l'] , stdout=subprocess.PIPE)
# process.communicate()


def sampleDecorator(func):
    def addingFunction():
        print("This is the added text to the actual function.")
        func()
    return addingFunction
@sampleDecorator
def actualFunction():
    print("This is the actual function.")

actualFunction()