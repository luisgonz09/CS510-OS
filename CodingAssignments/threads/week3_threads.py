"""
A multithreaded program template.
"""

import threading

def functionOne():
    print('Function One is running')

def functionTwo():
    print('Function Two is running')

def functionThree():
    print('Function Three is running')

def main():
    """
    Entry point of the program:  Create, start and join threads
    """

    #Build thread objects that map to distinct functions
    one_thread = threading.Thread(
        target=functionOne,
        name="one-thread"
    )

    two_thread = threading.Thread(
        target=functionTwo,
        name="two-thread"
    )

    three_thread = threading.Thread(
        target=functionThree,
        name="three-thread"
    )

    #Start threads concurrently
    one_thread.start()
    two_thread.start()
    three_thread.start()

    #Wait for all threads to finish execution
    one_thread.join()
    two_thread.join()
    three_thread.join()

if __name__ == "__main__":
    main()
