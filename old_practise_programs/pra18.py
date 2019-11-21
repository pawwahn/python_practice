import sys
 
def trace_calls(frame, event, arg):
    # The 'call' event occurs before a function gets executed.
    if event != 'call':
        return
    # Next, inspect the frame data and print information.
    print 'Function name=%s, line num=%s' % (frame.f_code.co_name, frame.f_lineno)
    return
 
def demo2():
    print 'in demo2()'
 
def demo1():
    print 'in demo1()'
    demo2()
 
sys.settrace(trace_calls)
demo1()