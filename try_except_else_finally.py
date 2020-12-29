try:
    The code with the exception that you want to catch.If an exception is raised, control flow leaves this block immediately and goes to the except block

except:
    This code is executed only if an exception was raised in the try block.Code executed in this block is just like normal code: if there is an exception, it not be
    automatically caught( and probably stop the program).

else:
    This code is executed only if no exceptions were raised in the try block.