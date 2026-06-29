'''
This program demonstrates how a semaphore limits how
many threads can enter a shared section at once.

File out the part with # TODO
'''

import multiprocessing
import time
import random

#set number of max processes that can run at a time
max_concurrrentprocesses = 4
#set total number of processes being run
total_processes = 10

#initialize semaphore
semaphore = multiprocessing.Semaphore(max_concurrrentprocesses)

#create time function to display current time on call
def current_time():
    curr_time = time.localtime()
    current_time = time.strftime("%H:%M:%S", curr_time)
    return current_time

#create function that would use semaphor to manage processess
def processing(process_id):
    print(f"{current_time()} [WAIT] Process {process_id} is waiting for semaphore")

    # Semaphore controls access to this critical section
    with semaphore:

        print(f"{current_time()} [ACQUIRE] Process {process_id} has acquired semaphore")

        # Simulate process execution time
        sleep_time = random.randint(1, 3)

        print(f"{current_time()} [RUNNING] Process {process_id} is running for {sleep_time} seconds")

        time.sleep(sleep_time)

        print(f"{current_time()} [COMPLETE] Process {process_id} has completed work")

    print(f"{current_time()} [RELEASE] Process {process_id} has released semaphore")

if __name__ == "__main__":
    #print how many processes the semaphore will run at one time
    print("Semaphore has been initialized with the value of:", max_concurrrentprocesses)

    #create multiprocess list to store all processes
    multiprocess = []

    for i in range(total_processes):
        m = multiprocessing.Process(target=processing, args=(i,))
        multiprocess.append(m)
        m.start()

    #loop through each process in the list to join in order to wait for each process to finish before printing all done statement
    for m in multiprocess:
        m.join()

    print("All processes are done!")