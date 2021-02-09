import os
from multiprocessing import Process, current_process

def square(number):
    result = number * number
    process_id = os.getpid()
    print(f'The process id {process_id} is for the number {number} and its result is {result}')



if __name__ == '__main__':
    processes = []
    numbers = [1, 2, 3, 4, 5, 6, 7]

    for number in numbers:
        process = Process(target=square, args=(number,))
        processes.append(process)
        process.start()